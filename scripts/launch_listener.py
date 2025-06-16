from scripts.window_manipulation import open_program
from scripts.hotkey_functions import workspace
from scripts import config_loader
from scripts.logger import write_entry, LogLevel
from threading import Thread
from ctypes import wintypes
from pyvda import AppView, get_apps_by_z_order
from typing import Any
import threading
import psutil
import ctypes
import time

# Event contants see:
# https://learn.microsoft.com/en-us/windows/win32/winauto/event-constants
_EVENT_OBJECT_SHOW    = 0x8002
_EVENT_OBJECT_DESTROY = 0x8001
_WINEVENT_OUTOFCONTEXT= 0x0000
_OBJID_WINDOW         = 0x00000000
_WM_QUIT              = 0x0012

_HOME_APPS: dict[str, int] = config_loader.get_home_apps()

_opened_programs: set[int] = set()

_message_thread: threading.Thread|None = None

_hook_create: Any = None
_hook_destroy: Any = None

WinEventProcType = ctypes.WINFUNCTYPE(
    None, wintypes.HANDLE, wintypes.DWORD, wintypes.HWND,
          wintypes.LONG, wintypes.LONG, wintypes.DWORD, wintypes.DWORD
)

@WinEventProcType
def _on_window_event(hWinEventHook, event, hwnd, idObject, idChild, nan, _):
    if event == _EVENT_OBJECT_DESTROY:
        pid = wintypes.DWORD()
        ctypes.windll.user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))

        global _opened_programs
        if pid.value in _opened_programs:
            write_entry(f"CLOSED - HWND: {hwnd}")
            _opened_programs.remove(pid.value)
    
        return

    if event == _EVENT_OBJECT_SHOW and idObject == _OBJID_WINDOW:
        finder_thread = Thread(target=_find_window_thread_func, args=(hwnd,), daemon=True)
        finder_thread.start()


def _find_window_thread_func(hwnd: int) ->  None:
    app: AppView|None = None

    for _ in range(50):
        try:
            app =  AppView(hwnd)

            pid = wintypes.DWORD()
            ctypes.windll.user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))

            if open_program.get_app_id(app.app_id) is None:
                name = "UNKNOWN"
                try:
                    name = psutil.Process(pid.value).name().lower()
                except psutil.NoSuchProcess:
                    pass

                write_entry(f"UNKNOWN APP - HWND: {hwnd} - PID: {pid.value} - Executable: {name}", LogLevel.WARNING)

            global _opened_programs
            if(pid.value in _opened_programs):
                return

            _opened_programs.add(pid.value)

            break

        except: 
            write_entry(f"Error finding window with HWND: {hwnd}", LogLevel.DEBUG)

        time.sleep(0.1)

    if app is None:
        write_entry(f"Could not open window with HWND: {hwnd}", LogLevel.VERBOSE)
        return
    
    app_id = str(open_program.get_app_id(app.app_id))
    write_entry(f"OPENED - HWND: {hwnd}, Name: {app_id}")
    
    if  app_id not in _HOME_APPS.keys():
        return

    home_workspace = _HOME_APPS[app_id]
    write_entry(f"Moving program {app_id} to home workspace {home_workspace}")
    workspace.goto_workspace_with_program(home_workspace, app)


def _message_thread_func() -> None:
    global _hook_create
    global _hook_destroy

    write_entry("Creating create hook...")
    _hook_create = ctypes.windll.user32.SetWinEventHook(
        _EVENT_OBJECT_SHOW, _EVENT_OBJECT_SHOW, 0,
        _on_window_event, 0, 0, _WINEVENT_OUTOFCONTEXT
    )
    if _hook_create is None:
        raise ctypes.WinError()
    
    write_entry("Creating destroy hook...")
    _hook_destroy = ctypes.windll.user32.SetWinEventHook(
        _EVENT_OBJECT_DESTROY, _EVENT_OBJECT_SHOW, 0,
        _on_window_event, 0, 0, _WINEVENT_OUTOFCONTEXT
    )
    if _hook_destroy is None:
        raise ctypes.WinError()

    msg = wintypes.MSG()
    while ctypes.windll.user32.GetMessageA(ctypes.byref(msg), 0, 0, 0) != 0:
        ctypes.windll.user32.TranslateMessage(ctypes.byref(msg))
        ctypes.windll.user32.DispatchMessageA(ctypes.byref(msg))
    write_entry(f"MESSAGE THREAD EXECUTION FINISHED.")

def start_listener() -> None:
    global _opened_programs
    global _message_thread

    write_entry("Starting listener...")
    for app in get_apps_by_z_order(current_desktop=False):
        pid = wintypes.DWORD()
        ctypes.windll.user32.GetWindowThreadProcessId(app.hwnd, ctypes.byref(pid))
        if pid.value not in _opened_programs:
            _opened_programs.add(pid.value)

    write_entry("Starting message thread...")
    _message_thread = threading.Thread(target=_message_thread_func, daemon=True)
    _message_thread.start()
    write_entry("Started all!")

def stop_listener() -> None:
    global _message_thread
    global _hook_create
    global _hook_destroy

    write_entry("Stopping hooks...")
    ctypes.windll.user32.UnhookWinEvent(_hook_create)
    ctypes.windll.user32.UnhookWinEvent(_hook_destroy)

    write_entry("Stopping message thread...")
    if _message_thread is None or _message_thread.native_id is None:
        write_entry("Thread not accessible")
        return
    
    thread_id = _message_thread.native_id
    ctypes.windll.user32.PostThreadMessageW(thread_id, _WM_QUIT, 0,0)
    write_entry("All stopped!")