from infi.systray import SysTrayIcon
from scripts import config_loader
from typing import Callable
import subprocess

SCRIPT_NAME = config_loader.get_script_name()
ICON_PATH = "public/icon.ico"

systray: SysTrayIcon | None = None

def start_system_tray(on_quit: Callable[[SysTrayIcon], None]) -> None:
    menu_options = (
        (SCRIPT_NAME, None, lambda _: None),
        ("Icon from Justin's 16x16 Icon Pack", None, lambda _: subprocess.run(["explorer", "https://zeromatrix.itch.io/rpgiab-icons"])),
        ("Edit Config", None, lambda _: subprocess.run(["notepad.exe", "config.toml"]))
    )

    global systray
    systray = SysTrayIcon(
        ICON_PATH, 
        SCRIPT_NAME,
        menu_options,
        on_quit=on_quit)
    systray.start()

def stop_system_tray() -> None:
    global systray
    
    if(systray is None):
        raise Exception("System tray not started")

    systray.shutdown()