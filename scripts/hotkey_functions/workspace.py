from pyvda import VirtualDesktop, get_virtual_desktops, AppView
from scripts import config_loader
from scripts.window_manipulation import open_program
from scripts.logger import write_entry, LogLevel
from scripts.window_manipulation.open_program import get_app_id

_workspace_names = config_loader.get_workspace_names()
_last_workspace: VirtualDesktop|None = None

def _get_workspace(num: int) -> VirtualDesktop:
    if num > len(get_virtual_desktops()):
        for i in range(num - len(get_virtual_desktops())):
            VirtualDesktop.create()

    target: VirtualDesktop|None = None
    for i in range(len(get_virtual_desktops())):
        desktop = get_virtual_desktops()[i]

        VirtualDesktop.rename(desktop, _workspace_names[desktop.number])
    
        if desktop.number == num:
            target = desktop
            break

    if target is None:
        raise Exception("Workspace not found")
    
    return target

def goto_workspace(workspace_num: int, app_id: str|None = None) -> None:
    write_entry(f"Going to workspace {workspace_num}")      
    global _last_workspace
    _last_workspace = VirtualDesktop.current()
    VirtualDesktop.go(_get_workspace(workspace_num))

    if app_id is not None and not open_program.is_default_open(app_id, workspace_num):
        write_entry(f"Opening default app {app_id} in workspace {workspace_num}")
        open_program.open_app(app_id)

def toggle_pin_window() -> None:
    current_window = AppView.current()

    if current_window.is_pinned():
        write_entry(f"Unpinning window {get_app_id(current_window.app_id)}...")
        current_window.unpin()
    else:
        write_entry(f"Pinning window {get_app_id(current_window.app_id)}...")
        current_window.pin()
def goto_previous_workspace() -> None:
    write_entry("Going to previous workspace...")
    global _last_workspace
    if _last_workspace is None:
        return
    
    cur = VirtualDesktop.current()
    VirtualDesktop.go(_last_workspace)
    _last_workspace = cur

def move_program_to_workspace(workspace_num: int) -> None:
    target = _get_workspace(workspace_num)
    window = AppView.current()
    write_entry(f"Moving program {get_app_id(window.app_id)} to workspace {workspace_num}")

    window.move(target)

def goto_workspace_with_program(workspace_num: int) -> None:
    move_program_to_workspace(workspace_num)
    goto_workspace(workspace_num)