from ctypes import wintypes
from scripts.win_api.event_codes import WinEvent, WinEventFlags, WinObjectIdentifiers
from scripts.win_api.common import get_tick_count
from typing import Callable
from scripts.logger import write_entry
import ctypes
from datetime import datetime

WinEventProcType = ctypes.WINFUNCTYPE(
    None, wintypes.HANDLE, wintypes.DWORD, wintypes.HWND,
          wintypes.LONG, wintypes.LONG, wintypes.DWORD, wintypes.DWORD
)

def create_window_hook(
            eventMin: WinEvent, 
            eventMax: WinEvent, 
            hmodWinEventProc: wintypes.HANDLE|None, 
            pfnWinEventProc: Callable,
            idProcess: wintypes.DWORD|None,
            idThread: wintypes.DWORD|None,
            dwFlags: WinEventFlags
        ) -> wintypes.HANDLE:
    """Create a new WinEventHook. For more details see: https://learn.microsoft.com/en-gb/windows/win32/api/winuser/nf-winuser-setwineventhook"""

    write_entry(f"Creating raw hook with event range {eventMin}-{eventMax} and callback {pfnWinEventProc}")

    if not isinstance(pfnWinEventProc, WinEventProcType):
        raise TypeError(f"pfnWinEventProc must be a callable of type {WinEventProcType.__name__}")

    idProcess = wintypes.DWORD(0) if idProcess is None else idProcess
    idThread = wintypes.DWORD(0) if idThread is None else idThread

    hook = ctypes.windll.user32.SetWinEventHook(
        eventMin, eventMax, hmodWinEventProc,
        pfnWinEventProc, idProcess, idThread, dwFlags
    )

    if not hook:
        raise ctypes.WinError()
    
    return hook

def create_simple_window_hook(
            eventMin: WinEvent, 
            eventMax: WinEvent, 
            pfnWinEventProc: Callable,
        ) -> wintypes.HANDLE:
    """Create a simple WinEventHook. For more details about pfnWinEventProc see: https://learn.microsoft.com/en-us/windows/win32/api/winuser/nc-winuser-wineventproc"""
    return create_window_hook(eventMin, eventMax, None, pfnWinEventProc, None, None, WinEventFlags.OUT_OF_CONTEXT)

def create_WinEventProcType(callback: Callable[[WinEvent, int, WinObjectIdentifiers|int, int, int, datetime], None]):
    """
    Create a callback function that can be used with window hooks.

    callback(event: WinEvent, hwnd: int, object_id: WinObjectIdentifiers|int, child_id: int, thread_id: int, event_time: datetime) -> None

    callback parameters:
    - event: WinEvent                       = The event that occurred
    - hwnd: int                             = The hwnd of the event source
    - object_id: WinObjectIdentifiers|int   = The object identifier
    - child_id: int                         = The child_id
    - thread_id: int                        = The thread_id of the event source
    - event_time: datetime                  = The time the event occurred.
    """

    @WinEventProcType
    def ret(hWinEventHook: wintypes.HANDLE, event: wintypes.DWORD, hwnd: wintypes.HWND, idObject: wintypes.LONG, idChild: wintypes.LONG, idEventThread: wintypes.DWORD, dwmsEventTime: wintypes.DWORD):
        int_idObject = int(idObject)
        enum_idObject: WinObjectIdentifiers|None = None

        try: enum_idObject = WinObjectIdentifiers(int_idObject)
        except: pass
        
        pass_idObject = int_idObject if enum_idObject is None else enum_idObject

        offset = (int(dwmsEventTime) - get_tick_count())/1000
        timestamp = datetime.now().timestamp()
        event_time = datetime.fromtimestamp(timestamp + offset)        

        callback(WinEvent(int(event)), int(hwnd), pass_idObject, int(idChild), int(idEventThread), event_time)

    return ret

def drop_win_hook(hook_handle: wintypes.HANDLE) -> None:
    """Unhooks a WinEventHook handle"""
    ctypes.windll.user32.UnhookWinEvent(hook_handle)