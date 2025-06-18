from ctypes import wintypes
from scripts.win_api.event_codes import WinEventMessages, LowLevelHook
from scripts.win_api.common import get_module_handle
from typing import Callable, Literal, TypeAlias, NamedTuple, get_args, cast
from scripts.logger import write_entry, LogLevel
import ctypes

# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nc-winuser-hookproc?utm_source=chatgpt.com
LowLevelProcType = ctypes.WINFUNCTYPE(
    ctypes.c_longlong, wintypes.INT, wintypes.WPARAM, wintypes.LPARAM
)

class KBDLLHOOKSTRUCT(ctypes.Structure):
    _fields_ = [
        ("vkCode",    wintypes.DWORD),
        ("scanCode",  wintypes.DWORD),
        ("flags",     wintypes.DWORD),
        ("time",      wintypes.DWORD),
        ("dwExtraInfo", wintypes.ULONG)
    ]

def create_low_level_hook(
        idHook: LowLevelHook,
        lpfn: Callable,
        hmod: wintypes.HINSTANCE|None,
        dwThreadId: wintypes.DWORD|None
    ) -> wintypes.HANDLE:
    """Create a new SetWindowsHookExW hook. For more details see: https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-setwindowshookexw"""

    if not isinstance(lpfn, LowLevelProcType):
        raise TypeError(f"lpfn must be a callable of type '{LowLevelProcType.__name__}'")

    dwThreadId = wintypes.DWORD(0) if dwThreadId is None else dwThreadId


    hook = ctypes.windll.user32.SetWindowsHookExW(
        idHook,
        lpfn,
        hmod,
        dwThreadId
    )

    return hook

def create_global_low_level_hook(        
        idHook: LowLevelHook,
        lpfn: Callable
    ) -> wintypes.HANDLE:
    return create_low_level_hook(idHook, lpfn, get_module_handle(), wintypes.DWORD(0))

def create_LowLevelProcType_Generic(callback: Callable[[int, wintypes.WPARAM, wintypes.LPARAM], bool]):
    """
    Create a callback function that can be used with low-level hooks.
    For more details see: https://learn.microsoft.com/en-us/windows/win32/winmsg/about-hooks

    callback(code: int, wParam: wintypes.WPARAM, lParam: wintypes.LPARAM) -> bool

    callback parameters:
    - code: int                  = Event state code.
    - wParam: wintypes.WPARAM    = The event-specific data
    - lParam: wintypes.LPARAM    = The event-specific data

    callback returns:
    - bool = False to block the event from being passed to other hooks, True otherwise
    """
    @LowLevelProcType
    def ret(code: int, wParam: wintypes.WPARAM, lParam: wintypes.LPARAM) -> ctypes.c_longlong:
        call_next = callback(code, wParam, lParam)

        # Returning 1 blocks the event from being passed to other hooks
        if not call_next: return ctypes.c_longlong(1)

        # https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-callnexthookex
        return ctypes.windll.user32.CallNextHookEx(None, code, wParam, lParam)
    
    return ret

key_status: TypeAlias = Literal[WinEventMessages.WM_KEYDOWN] | Literal[WinEventMessages.WM_KEYUP] | Literal[WinEventMessages.WM_SYSKEYDOWN] | Literal[WinEventMessages.WM_SYSKEYUP]
class key_info(NamedTuple):
    vk_code: int
    scan_code: int
    flags: int
    time: int
    custom: int

def create_LowLevelProcType_KeyboardLL(callback: Callable[[key_status, key_info], bool]):
    """
    Create a callback function that can be used with low-level hooks for keyboard events.
    For more details see: https://learn.microsoft.com/en-us/windows/win32/winmsg/lowlevelkeyboardproc

    callback (
        status: Literal[WinEventMessages.WM_KEYDOWN, WinEventMessages.WM_KEYUP, WinEventMessages.WM_SYSKEYDOWN, WinEventMessages.WM_SYSKEYUP], 
        info: key_info
    ) -> bool

    callback returns:
    - bool = False to block the event from being passed to other hooks, True otherwise
    """
    @LowLevelProcType
    def ret(code: int, wParam: wintypes.WPARAM, lParam: wintypes.LPARAM) -> ctypes.c_longlong:
        if code < 0:
            write_entry(f"LowLevelProcType_KeyboardLL: {code} < 0, calling CallNextHookEx() without processing the event.", LogLevel.DEBUG)
            return ctypes.windll.user32.CallNextHookEx(None, code, wParam, lParam)

        status = WinEventMessages(wParam)
        if not isinstance(status, get_args(key_status)):
            raise ctypes.WinError(descr=f"Invalid status: {status}\nExpected: {get_args(key_status)}")
        
        info_struct = KBDLLHOOKSTRUCT.from_address(int(lParam))
        info_tuple = key_info(
            info_struct.vkCode,
            info_struct.scanCode,
            info_struct.flags,
            info_struct.time,
            info_struct.dwExtraInfo
        )
        
        call_next = callback(cast(key_status, status), info_tuple)

        # Returning 1 blocks the event from being passed to other hooks
        if not call_next: return ctypes.c_longlong(-1)

        # https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-callnexthookex
        return ctypes.windll.user32.CallNextHookEx(None, code, wParam, lParam)
    
    return ret

def drop_low_level_hook(hook_handle: wintypes.HANDLE) -> None:
    """Unhooks a LowLevelProc handle"""
    ctypes.windll.user32.UnhookWindowsHookEx(hook_handle)