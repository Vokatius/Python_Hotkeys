#
#   Adds <num_0> to <num_9> as valid modifiers in the `HotKey.parse` method
#
#   Originally pynput does not recognize these keys.
#
#   This patch works by abusing the try except of the 'parse's internal 'parse(s)' function,
#   where a unkown key is is tried to be parsed literally as a vk code, before rasing a ValueError.
#
#   The '_event_to_key' method of the 'Listener' class is also overridden beacuse it sets the
#   '_PLATFORM_EXTENSIONS' in a way that differs for keys registered virtually and prevents comparisons 
#   to succeed. This patch fixes this, by overriding all properties of the '_PLATFORM_EXTENSIONS' to NONE,
#   for all numpad keys.
#   I think this safe as all other keys I watched also have only NONE as their '_PLATFORM_EXTENSIONS',
#

from scripts.window_manipulation.virtual_key_codes import VK_CODES
from pynput.keyboard import HotKey, KeyCode
from pynput.keyboard._win32 import Listener, Key as winKey, KeyCode as winKeyCode
from functools import wraps
from typing import Any

_BASE_PARSE = HotKey.parse
_BASE_EQ = KeyCode.__eq__
_BASE_CONVERTER = Listener._event_to_key

_HOTKEYS: dict[str, int] = {
    '<num_0>': VK_CODES['NUMPAD0'],
    '<num_1>': VK_CODES['NUMPAD1'],
    '<num_2>': VK_CODES['NUMPAD2'],
    '<num_3>': VK_CODES['NUMPAD3'],
    '<num_4>': VK_CODES['NUMPAD4'],
    '<num_5>': VK_CODES['NUMPAD5'],
    '<num_6>': VK_CODES['NUMPAD6'],
    '<num_7>': VK_CODES['NUMPAD7'],
    '<num_8>': VK_CODES['NUMPAD8'],
    '<num_9>': VK_CODES['NUMPAD9'],
}
@staticmethod
@wraps(_BASE_PARSE)
def _parse_wrapper(keys: str) -> list[KeyCode]:
    if '<num_' in keys:
        for (literal, code) in _HOTKEYS.items():
            keys = keys.replace(literal, f'<{code}>')

    return _BASE_PARSE(keys)

HotKey.parse = _parse_wrapper

@wraps(_BASE_CONVERTER)
def _convert_wrapper(self: Listener, msg: Any, vk: int|None) -> (winKey | winKeyCode):
    key_res = _BASE_CONVERTER(self, msg, vk)

    if type(key_res) == winKeyCode and key_res.vk in _HOTKEYS.values():
        for f in winKeyCode._PLATFORM_EXTENSIONS:
            setattr(key_res, f, None)

    return key_res

Listener._event_to_key = _convert_wrapper