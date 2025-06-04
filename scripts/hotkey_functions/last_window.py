import win32gui
from typing import Callable
from scripts.window_manipulation.foreground import send_to_foreground_hwnd

last_window_hwnd : int|None = None

def focus_last_window() -> None:
    global last_window_hwnd
    if(last_window_hwnd is None):
        return
    
    hwnd = win32gui.GetForegroundWindow()
    send_to_foreground_hwnd(last_window_hwnd)
    last_window_hwnd = hwnd

def set_last_window(hotkey_func: Callable[[], None]) -> None:
    global last_window_hwnd
    last_window_hwnd = win32gui.GetForegroundWindow()
    hotkey_func()