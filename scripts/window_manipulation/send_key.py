import ctypes
import time

def press_key(key_code: int) -> None:
    ctypes.windll.user32.keybd_event(key_code, 0, 0, 0)

def release_key(key_code: int) -> None:
    ctypes.windll.user32.keybd_event(key_code, 0, 2, 0)

def send_key(key_code: int, sleep: float|None = None) -> None:
    press_key(key_code)
    if(sleep is not None):
        time.sleep(sleep)
    release_key(key_code)

def send_shortcut(shortcut: list[int], sleep: float|None = None) -> None:
    for key_code in shortcut:
        press_key(key_code)

    if(sleep is not None):
        time.sleep(sleep)

    for key_code in reversed(shortcut):
        release_key(key_code)
