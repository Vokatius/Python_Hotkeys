from pynput import keyboard
from scripts.hotkey_functions import browser, last_window
from scripts import config_loader
from typing import Callable

shortcuts = config_loader.get_hotkeys()

hotkeys: dict[str, Callable[[], None]] = {}

for shortcut_name in shortcuts:
    shortcut_value = shortcuts[shortcut_name]

    match shortcut_name:
        case 'focus_web_browser':
            hotkeys[shortcut_value] = lambda: last_window.set_last_window(browser.focus_browser)

        case 'goto_previous':
            hotkeys[shortcut_value] = last_window.focus_last_window

        case 'open_web_tab':
            hotkeys[shortcut_value] = lambda: last_window.set_last_window(browser.open_new_tab)

hotkeys_thread = keyboard.GlobalHotKeys(hotkeys)

def start_hotkey_listener() -> None:
    hotkeys_thread.start()

def stop_hotkey_listener() -> None:
    hotkeys_thread.stop()
