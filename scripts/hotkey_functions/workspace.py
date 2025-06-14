from pyvda import VirtualDesktop, get_virtual_desktops, AppView
from scripts import config_loader

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

def goto_workspace(workspace_num: int, open_program: str|None = None) -> None:
    if open_program is not None:
        raise NotImplementedError("Open program functionality is not implemented yet.")

    global _last_workspace
    _last_workspace = VirtualDesktop.current()
    VirtualDesktop.go(_get_workspace(workspace_num))

def goto_previous_workspace() -> None:
    global _last_workspace
    if _last_workspace is None:
        return
    
    cur = VirtualDesktop.current()
    VirtualDesktop.go(_last_workspace)
    _last_workspace = cur

def move_program_to_workspace(workspace_num: int) -> None:
    target = _get_workspace(workspace_num)
    window = AppView.current()
    window.move(target)

def goto_workspace_with_program(workspace_num: int) -> None:
    move_program_to_workspace(workspace_num)
    goto_workspace(workspace_num)