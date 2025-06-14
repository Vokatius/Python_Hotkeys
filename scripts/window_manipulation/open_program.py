from pyvda import get_apps_by_z_order
from ctypes import cast, c_wchar_p
from scripts import config_loader
import AppOpener

def open_app(app_id: str) -> None:
    AppOpener.open(app_id, match_closest=True, output=False)

def open_app_if_closed(app_id: str) -> None:
    if is_program_open(app_id):
        return

    open_app(app_id)

def is_program_open(app_id: str, only_curr_workspace = True) -> bool:
    for app in get_apps_by_z_order(current_desktop=only_curr_workspace):
        if app_id == get_app_id(app.app_id):
            return True

    return False

def is_default_open(app_id: str, workspace_num: int) -> bool:
    for app in get_apps_by_z_order():
        if app_id != get_app_id(app.app_id):
            continue

        ignored_workspaces = config_loader.get_config()['general']['workspace_ignores_pinned']            
        if workspace_num in ignored_workspaces and app.is_pinned() == False:
            return True

    return False

def get_app_id(ptr: int|None) -> str|None:
    str_ptr = cast(ptr, c_wchar_p) # type: ignore
    return str_ptr.value