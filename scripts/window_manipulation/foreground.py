from scripts.window_manipulation.virtual_key_codes import VK_CODES
from scripts.logger import write_entry, LogLevel
from scripts.window_manipulation import send_key
from scripts.window_manipulation import open_program
from pyvda import get_apps_by_z_order

import win32gui
import time

def send_to_foreground_name(name: str) -> None:
    write_entry(f"Setting foreground window with name {name}")
    hwnd: int|None = None
    for app in get_apps_by_z_order(current_desktop=False):
        app_id = open_program.get_app_id(app.app_id)
        if(app_id != name):
            continue

        hwnd = app.hwnd
        break
    
    if hwnd is None:
        write_entry(f"Could not find window with name {name}", LogLevel.WARNING)
        return
    write_entry(f"Window with name {name} has hwnd {hwnd}")
    send_to_foreground_hwnd(hwnd)

def send_to_foreground_hwnd(hwnd: int) -> None:
    write_entry(f"Setting foreground window to {hwnd}")
    _set_foreground(hwnd)
    _ensure_foreground(hwnd)
    write_entry(f"Setting foreground window to {hwnd}")

def is_foreground(hwnd: int) -> bool:
    return hwnd == win32gui.GetForegroundWindow()

has_send_alt_up = False
# Copies AutoHotKeys foreground handling logic:
# https://www.autohotkey.com/docs/v2/lib/WinActivate.htm#Remarks
def _ensure_foreground(window_hwnd: int) -> None:
    if(is_foreground(window_hwnd)):
        return
    
    global has_send_alt_up
    if(not has_send_alt_up):
        has_send_alt_up = True
        send_key.send_shortcut([VK_CODES['MENU'], VK_CODES['UP']])
        _set_foreground(window_hwnd)

        if(is_foreground(window_hwnd)):
            return
        
        time.sleep(0.01)

    for i in range(6):
        _set_foreground(window_hwnd)
        if(is_foreground(window_hwnd)):
            return
        time.sleep(0.01)

    send_key.send_shortcut([VK_CODES['MENU'], VK_CODES['2']])
    _set_foreground(window_hwnd)

    if(is_foreground(window_hwnd)):
        return

def _set_foreground(hwnd: int) -> None:
    try:
        win32gui.SetForegroundWindow(hwnd)
        write_entry(f"Setting foreground window to {hwnd}: Success")
    except Exception as e:
        write_entry(f"Setting foreground window to {hwnd}: Failed", LogLevel.DEBUG, error=e)
        pass