from scripts.window_manipulation.foreground import send_to_foreground_name
from scripts.window_manipulation.virtual_key_codes import VK_CODES
from scripts.window_manipulation import send_key
from scripts.hotkey_functions import workspace
from scripts import config_loader
import time

_COOLDOWN_TIME_MS = 500

_browser = config_loader.get_applications()['web_browser']
_browser_workspace: int|None = None

for ws in config_loader.get_workspace_config().values():
    if ws.program == 'web_browser':
        _browser_workspace = ws.number

def focus_browser() -> None:
    if _browser_workspace is None:
        return
    
    workspace.goto_workspace(_browser_workspace, _browser)
    send_to_foreground_name(_browser)

# TODO: Fix problem of double executing properly
_new_tab_time = 0
def open_new_tab() -> None:
    curtime = time.time_ns()

    global _new_tab_time
    if curtime < _new_tab_time + (_COOLDOWN_TIME_MS * 1000000):
        return

    focus_browser()
    print("Sending shortcut")
    send_key.send_shortcut([VK_CODES['CONTROL'], VK_CODES['T']], 0.05)
    _new_tab_time = curtime

# TODO: Fix problem of double executing properly
_new_chat_time = 0
def open_chatgpt() -> None:
    curtime = time.time_ns()

    global _new_chat_time
    if curtime < _new_chat_time + (_COOLDOWN_TIME_MS * 1000000):
        return

    focus_browser()
    send_key.send_shortcut([VK_CODES['CONTROL'], VK_CODES['T']], 0.05)
    send_key.send_shortcut([VK_CODES['C'], VK_CODES['SPACE']], 0.05)
    _new_chat_time = curtime