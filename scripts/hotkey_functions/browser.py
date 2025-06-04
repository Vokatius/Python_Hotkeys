from scripts.window_manipulation.foreground import send_to_foreground_name
from scripts.window_manipulation.virtual_key_codes import VK_CODES
from scripts.window_manipulation import send_key
from scripts import config_loader

browser = config_loader.get_applications()['web_browser']

def focus_browser() -> None:
    send_to_foreground_name(browser)

def open_new_tab() -> None:
    send_to_foreground_name(browser, lambda: send_key.send_shortcut([VK_CODES['CONTROL'], VK_CODES['T']]))