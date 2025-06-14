from scripts import config_loader
from typing import Callable
import keyboard

_shortcuts = config_loader.get_hotkeys()
_hotkeys: dict[str, Callable[[], None]] = {}

def register_hotkey(hotkey_name: str, func: Callable[[], None]) -> None:
    if(hotkey_name not in _shortcuts.keys()):
        raise Exception(f"\"{hotkey_name}\" is not registered in the config file.")

    hotkey = _shortcuts[hotkey_name]
    _hotkeys[hotkey] = func

def register_hotkey_raw(hotkey: str, func: Callable[[], None]) -> None:
    _hotkeys[hotkey] = func

def start_hotkey_listener() -> None:
    for (hotkey, func) in _hotkeys.items():
        keyboard.add_hotkey(hotkey=hotkey, callback=func)

def stop_hotkey_listener() -> None:
    keyboard.unhook_all()
    keyboard.remove_all_hotkeys()
