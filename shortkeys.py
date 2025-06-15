from scripts import hotkey_listener, system_tray, hotkey_registration as _
import AppOpener

AppOpener.mklist(output=False)
hotkey_listener.start_hotkey_listener()
system_tray.start_system_tray(lambda _: hotkey_listener.stop_hotkey_listener())