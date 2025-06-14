from scripts import hotkey_listener, system_tray, hotkey_registration as _

hotkey_listener.start_hotkey_listener()
system_tray.start_system_tray(lambda _: hotkey_listener.stop_hotkey_listener())