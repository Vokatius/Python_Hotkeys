from scripts import logger
from scripts import hotkey_registration as _
from scripts import pynput_parse_patch as _
from scripts import hotkey_listener, system_tray
from scripts import launch_listener
import AppOpener

logger.write_entry("Starting shortkeys")
logger.write_entry("Initializing AppOpener")
AppOpener.mklist(output=False)

logger.write_entry("Initializing Launch Listener")
launch_listener.start_listener()

logger.write_entry("Initializing Launch Listener")
hotkey_listener.start_hotkey_listener()

def _shutdown() -> None:
    logger.write_entry("Shutting down launch listener")
    launch_listener.stop_listener()

    logger.write_entry("Shutting down hotkey listener")
    hotkey_listener.stop_hotkey_listener()
    
    logger.write_entry("Shutdown complete")

logger.write_entry("Starting System Tray")
system_tray.start_system_tray(lambda _: _shutdown())