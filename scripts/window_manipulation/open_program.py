from scripts.logger import write_entry, LogLevel
from pyvda import get_apps_by_z_order
from ctypes import cast, c_wchar_p
from scripts import config_loader
import AppOpener

def open_app(app_id: str) -> None:
    write_entry(f"Opening application {app_id}")
    AppOpener.open(app_id, match_closest=True, output=False)

def open_app_if_closed(app_id: str) -> None:
    write_entry(f"Checking if application {app_id} is closed")
    if is_program_open(app_id):
        write_entry(f"Application {app_id} is already open")
        return
    
    open_app(app_id)

def is_program_open(app_id: str, only_curr_workspace = True) -> bool:
    for app in get_apps_by_z_order(current_desktop=only_curr_workspace):
        if app_id == get_app_id(app.app_id):
            write_entry(f"Application {app_id} is open: True")
            return True

    write_entry(f"Application {app_id} is open: False")
    return False

def is_default_open(app_id: str, workspace_num: int) -> bool:
    for app in get_apps_by_z_order():
        if app_id != get_app_id(app.app_id):
            continue

        ignored_workspaces = config_loader.CONFIG['general']['workspace_ignores_pinned']            
        if workspace_num in ignored_workspaces and app.is_pinned() == False:
            write_entry(f"Application {app_id} is default open on workspace {workspace_num}: True")
            return True

    write_entry(f"Application {app_id} is default open on workspace {workspace_num}: False")
    return False

def get_app_id(ptr: int|None) -> str|None:
    str_ptr = cast(ptr, c_wchar_p) # type: ignore
    return str_ptr.value