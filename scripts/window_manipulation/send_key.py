from scripts.logger import write_entry, LogLevel
import ctypes
import time

def press_key(key_code: int) -> None:
    ctypes.windll.user32.keybd_event(key_code, 0, 0, 0)

def release_key(key_code: int) -> None:
    ctypes.windll.user32.keybd_event(key_code, 0, 2, 0)

def send_key(key_code: int, sleep_seconds: float|None = None) -> None:
    write_entry(f"Key {key_code} press")
    press_key(key_code)

    write_entry(f"Key {key_code} press sleeping for {sleep_seconds} seconds")
    if(sleep_seconds is not None):
        time.sleep(sleep_seconds)

    write_entry(f"Key {key_code} releasing")
    release_key(key_code)

def send_shortcut(shortcut: list[int], sleep_seconds: float|None = None) -> None:
    write_entry(f"Shortcut {shortcut} press")
    for key_code in shortcut:
        press_key(key_code)

    write_entry(f"Shortcut {shortcut} press sleeping for {sleep_seconds} seconds")
    if(sleep_seconds is not None):
        time.sleep(sleep_seconds)

    write_entry(f"Shortcut {shortcut} releasing")
    for key_code in shortcut:
        release_key(key_code)
