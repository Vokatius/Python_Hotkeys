from scripts.window_manipulation import open_program
from scripts.hotkey_functions import workspace
from scripts.win_api.event_codes import WinEvent, WinEventFlags, WinEventMessages, WinObjectIdentifiers
from scripts.win_api import common, win_event_loop, event_listener
from scripts import config_loader
from scripts.logger import write_entry, LogLevel
from threading import Thread
from pyvda import AppView, get_apps_by_z_order
from datetime import datetime
import threading
import time

_HOME_APPS: dict[str, int] = config_loader.get_home_apps()

_opened_programs: set[int] = set()
_message_thread: Thread|None = None

def _on_window_event(event: WinEvent, hwnd: int, object_id: WinObjectIdentifiers|int, child_id: int, thread_id: int, event_time: datetime):
    if event == WinEvent.EVENT_OBJECT_DESTROY:
        pid = common.get_pid(hwnd)

        global _opened_programs
        if pid in _opened_programs:
            write_entry(f"CLOSED - HWND: {hwnd}")
            _opened_programs.remove(pid)
    
        return

    if event == WinEvent.EVENT_OBJECT_SHOW and object_id == WinObjectIdentifiers.OBJID_WINDOW:
        finder_thread = Thread(target=_find_window_thread_func, args=(hwnd,), daemon=True)
        finder_thread.start()

def _find_window_thread_func(hwnd: int) ->  None:
    global _opened_programs
    app: AppView|None = None

    for _ in range(50):
        try:
            app = AppView(hwnd)
            break
        except: 
            write_entry(f"Error finding window with HWND: {hwnd}", LogLevel.DEBUG)
        time.sleep(0.1)

    if app is None:
        write_entry(f"Could not open window with HWND: {hwnd}", LogLevel.VERBOSE)
        return
    
    pid = common.get_pid(app.hwnd)
    app_id = open_program.get_app_id(app.app_id)
    if app_id is None:
        name =  common.get_name(pid)
        name = "UNKNOWN" if name is None else name
        write_entry(f"UNKNOWN APP - HWND: {hwnd} - PID: {pid} - Executable: {name}", LogLevel.WARNING)
        return

    if app_id not in _HOME_APPS.keys():
        return

    if pid in _opened_programs:
        return

    write_entry(f"OPENED - HWND: {hwnd}, Name: {app_id}")
    _opened_programs.add(pid)

    home_workspace = _HOME_APPS[app_id]
    write_entry(f"Moving program {app_id} to home workspace {home_workspace}")
    workspace.goto_workspace_with_program(home_workspace, app)

def _message_thread_func() -> None:
    cb = win_event_loop.create_WinEventProcType(_on_window_event)

    write_entry("Starting hooks...")
    create_handle = win_event_loop.create_simple_window_hook (
        WinEvent.EVENT_OBJECT_SHOW, 
        WinEvent.EVENT_OBJECT_SHOW, 
        cb
    )
    
    destroy_handle = win_event_loop.create_simple_window_hook (
        WinEvent.EVENT_OBJECT_DESTROY, 
        WinEvent.EVENT_OBJECT_DESTROY, 
        cb
    )

    write_entry(f"Created handle: {create_handle}")

    start_listener = event_listener.create_listener (
        WinEventMessages.WM_NULL,
        WinEventMessages.WM_NULL
    )

    write_entry("Starting listener...")
    start_listener()

    write_entry("Stopping hooks...")
    win_event_loop.drop_win_hook(create_handle)
    win_event_loop.drop_win_hook(destroy_handle)

def start_listener() -> None:
    global _opened_programs
    global _message_thread

    write_entry("Starting listener...")
    for app in get_apps_by_z_order(current_desktop=False):
        pid = common.get_pid(app.hwnd)
        if pid not in _opened_programs:
            _opened_programs.add(pid)

    write_entry("Starting message thread...")
    _message_thread = threading.Thread(target=_message_thread_func, daemon=True)
    _message_thread.start()
    write_entry("Started all!")

def stop_listener() -> None:
    global _message_thread

    write_entry("Stopping message thread...")
    if _message_thread is None or _message_thread.native_id is None:
        raise RuntimeError("_message_thread not accessible")
    
    thread_id = _message_thread.native_id
    event_listener.stop_listener(thread_id)
    _message_thread.join(timeout=5.0)
    if _message_thread.is_alive():
        _message_thread = None
        raise RuntimeError(f"Thread {thread_id} did not stop in time")
    
    write_entry("All stopped!")