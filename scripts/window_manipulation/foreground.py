from scripts.window_manipulation.virtual_key_codes import VK_CODES
from scripts.window_manipulation import send_key
from typing import Callable

import win32gui
import time

def send_to_foreground_name(name: str, callback: Callable[[], None]|None = None) -> None:
    def cb(hwnd: int) -> None:
        window_name = win32gui.GetWindowText(hwnd)
        if name.lower() not in window_name.lower():
            return
        
        _set_foreground(hwnd)
        _ensure_foreground(hwnd)

        if(callback is not None):
            callback()
                  
    win32gui.EnumWindows(lambda hwnd, _: cb(hwnd), None)

def send_to_foreground_hwnd(hwnd: int) -> None:        
    _set_foreground(hwnd)
    _ensure_foreground(hwnd)

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
    except:
        pass
