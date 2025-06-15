from scripts import config_loader
from typing import Callable
from pynput import keyboard

_shortcuts = config_loader.get_hotkeys()
_hotkeys: dict[str, Callable[[], None]] = {}
_hotkey_listener: keyboard.GlobalHotKeys|None = None

def register_hotkey(hotkey_name: str, func: Callable[[], None]) -> None:
    if(hotkey_name not in _shortcuts.keys()):
        raise Exception(f"\"{hotkey_name}\" is not registered in the config file.")

    hotkey = _shortcuts[hotkey_name]

    if hotkey is False:
        return

    _hotkeys[hotkey] = func

def register_hotkey_raw(hotkey: str, func: Callable[[], None]) -> None:
    _hotkeys[hotkey] = func

def start_hotkey_listener() -> None:
    global _hotkey_listener
    _hotkey_listener = keyboard.GlobalHotKeys(_hotkeys)
    _hotkey_listener.start()

def stop_hotkey_listener() -> None:
    global _hotkey_listener

    if _hotkey_listener is None:
        raise Exception("No hotkey listener to stop.")

    _hotkey_listener.stop()
