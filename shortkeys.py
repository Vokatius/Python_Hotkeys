from scripts import hotkey_registration as _
from scripts import pynput_parse_patch as _
from scripts import hotkey_listener, system_tray
import AppOpener

AppOpener.mklist(output=False)
hotkey_listener.start_hotkey_listener()
system_tray.start_system_tray(lambda _: hotkey_listener.stop_hotkey_listener())