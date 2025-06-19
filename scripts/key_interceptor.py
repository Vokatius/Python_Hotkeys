from scripts.win_api import LowLevel_event_loop, event_listener
from scripts.win_api.event_codes import LowLevelHook, WinEvent, WinEventFlags, WinEventMessages, WinObjectIdentifiers
from scripts.win_api.LowLevel_event_loop import key_info, LL_callback_return
from scripts.logger import write_entry, LogLevel
from scripts.win_api.virtual_key_codes import CONFIG_STR_TO_VK, VK_CODES
from typing import Literal, Any, Callable, TypeAlias
from threading import Thread
from scripts import config_loader

_SHORTCUTS = config_loader.get_hotkeys()
_IS_SUPRESS_HOTKEYS = config_loader.get_block_hotkey_presses()
_KEY_SIDES: dict[str, tuple[str|None, str|None]] = {
    'MENU':    ('LMENU',    'RMENU'),    # ALT
    'CONTROL': ('LCONTROL', 'RCONTROL'),
    'SHIFT':   ('LSHIFT',   'RSHIFT'),
    'LWIN':     (None,     'RWIN'),
}

hotkey: TypeAlias = frozenset[int]

_hotkey_funcs: dict[hotkey, Callable[[], None]] = {}
_pressed_keys: set[int] = set()
_interceptor_thread: Thread|None = None

def get_hotkey(hotkey_str: str) -> set[hotkey]:
    """
    Gets a decoded hotkey from a string. 
    Returns a set of frozensets containing the virtual key codes for each possible combination of keys with left and right versions of the key.
    """
    if hotkey_str is False: 
        return
    
    hotkey_list: set[hotkey] = set()

    hk_set: set[int] = set()
    for key in hotkey_str.split("+"):
        if len(key) == 1 or key[0] != "<" or key[-1] != ">":
            hk_set.add(VK_CODES[key.upper()])
        else:
            hk_set.add(CONFIG_STR_TO_VK[key])
    hotkey_list.add(hotkey(hk_set))

    for generic_key, (left_key, right_key) in _KEY_SIDES.items():
        gen_code  = VK_CODES[generic_key]
        if gen_code in hk_set:
            base = hk_set - {gen_code}
            if left_key is not None:
                hotkey_list.add(hotkey(base | {VK_CODES[left_key]}))
            if right_key is not None:
                hotkey_list.add(hotkey(base | {VK_CODES[right_key]}))

    return hotkey_list

def register_hotkey(hotkey_name: str, func: Callable[[], None]) -> None:
    write_entry(f"Registering hotkey {hotkey_name} with function {func.__name__}")
    if(hotkey_name not in _SHORTCUTS.keys()):
        raise Exception(f"\"{hotkey_name}\" is not registered in the config file.")

    hotkey_str = _SHORTCUTS[hotkey_name]

    if hotkey_str is False:
        return

    for key_codes in get_hotkey(hotkey_str):
        _hotkey_funcs[key_codes] = func

    write_entry(f"Registration complete forhotkey {hotkey_name} with function {func.__name__}")

def register_hotkey_raw(hotkey_str: str, func: Callable[[], None]) -> None:
    write_entry(f"Registering raw hotkey {hotkey_str} with function {func.__name__}")
    for key_codes in get_hotkey(hotkey_str):
        _hotkey_funcs[key_codes] = func
    write_entry(f"Registration complete for raw hotkey {hotkey_str} with function {func.__name__}")

def _on_key_up(key_code: int) -> None:
    if key_code in _pressed_keys:
        _pressed_keys.remove(key_code)
    else:
        write_entry(f"{key_code} was reported as RELEASED, but not in internal pressed set!", LogLevel.DEBUG)

def _on_key_down(key_code: int) -> LL_callback_return:
    if key_code not in _pressed_keys:
        _pressed_keys.add(key_code)
    else:
        write_entry(f"{key_code} was reported as PRESSED, but already in internal pressed set!", LogLevel.VERBOSE)

    hotkey_pressed = hotkey(_pressed_keys)

    if hotkey_pressed not in _hotkey_funcs.keys():
        return LL_callback_return.pass_event
    
    write_entry(f"{key_code} intercepted, hotkey {_pressed_keys} found!", LogLevel.INFO)

    if not hotkey_pressed in _hotkey_funcs.keys():
        write_entry(f"Hotkey {hotkey_pressed} has no associated function! - Hotkey functions registered: {_hotkey_funcs.keys()}", LogLevel.WARNING)
        return LL_callback_return.pass_event

    dispatch_hotkey_func = Thread(target=_hotkey_funcs[hotkey_pressed], daemon=True)
    dispatch_hotkey_func.start()

    if _IS_SUPRESS_HOTKEYS:
        return LL_callback_return.block_event
    else:
        return LL_callback_return.pass_event

def _on_keypress (
        status: Literal[WinEventMessages.WM_KEYDOWN, WinEventMessages.WM_KEYUP, WinEventMessages.WM_SYSKEYDOWN, WinEventMessages.WM_SYSKEYUP],
        info: key_info
    ) -> LL_callback_return:

    key: int = info.vk_code

    if status == WinEventMessages.WM_KEYUP or status == WinEventMessages.WM_SYSKEYUP:
        _on_key_up(key)
        return LL_callback_return.pass_event

    return _on_key_down(key)

def _interceptor_thread_func(): 
    cb = LowLevel_event_loop.create_LowLevelProcType_KeyboardLL(_on_keypress)

    write_entry(f"Starting key interceptor hook...")
    hook = LowLevel_event_loop.create_global_low_level_hook(
        LowLevelHook.WH_KEYBOARD_LL,
        cb
    )

    start_listener = event_listener.create_listener(
        WinEventMessages.WM_NULL,
        WinEventMessages.WM_NULL
    )

    write_entry(f"Starting interceptor listener...")
    start_listener()

    write_entry(f"Dropping key interceptor hook...")
    LowLevel_event_loop.drop_low_level_hook(hook)

def start_interceptor() -> None:
    global _interceptor_thread

    _interceptor_thread = Thread(target=_interceptor_thread_func, daemon=True)
    _interceptor_thread.start()

def stop_interceptor() -> None:
    global _interceptor_thread

    write_entry(f"Stopping interceptor thread...")
    if _interceptor_thread is None or _interceptor_thread.native_id is None:
        raise RuntimeError("_interceptor_thread not accessible")
    
    thread_id = _interceptor_thread.native_id
    event_listener.stop_listener(thread_id)
    _interceptor_thread.join(timeout=5.0)
    if _interceptor_thread.is_alive():
        _interceptor_thread = None
        raise RuntimeError(f"Thread {thread_id} did not stop in time")
    
    write_entry("All stopped!")
    
