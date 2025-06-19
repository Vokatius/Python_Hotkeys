from scripts import logger
from scripts import hotkey_registration as _
from scripts import system_tray
from scripts import launch_listener
from scripts import key_interceptor
import AppOpener

logger.write_entry("Starting shortkeys")
logger.write_entry("Initializing AppOpener")
AppOpener.mklist(output=False)

logger.write_entry("Initializing Launch Listener")
launch_listener.start_listener()

logger.write_entry("Initializing Key Interceptor")
key_interceptor.start_interceptor()

def _shutdown() -> None:
    logger.write_entry("Shutting down key interceptor")
    key_interceptor.stop_interceptor()

    logger.write_entry("Shutting down launch listener")
    launch_listener.stop_listener()
    
    logger.write_entry("Shutdown complete")

logger.write_entry("Starting System Tray")
system_tray.start_system_tray(lambda _: _shutdown())