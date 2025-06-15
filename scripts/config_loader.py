import tomllib
from collections import namedtuple
from typing import Any

def _get_config() -> dict[str, dict[str, Any]]:
    with open('config.toml', "rb") as config_pointer:
        config = tomllib.load(config_pointer)
    return config

CONFIG = _get_config()

def get_script_name() -> str:
    return  CONFIG['general']['title']

def get_hotkeys() -> dict[str, str]:
    return  CONFIG['hotkeys']

def get_applications() -> dict[str, str]:
    return  CONFIG['applications']

def get_workspace_keys() -> dict[int, str]:
    workspaces: dict[int, str] = {}
    for (key, hotkey) in  CONFIG['workspace_shortcuts'].items():
        if(key == 'modifiers'):
            continue

        workspace_num = int(key.split('_')[2])
        workspaces[workspace_num] = hotkey

    return workspaces

def get_workspace_hotkeys() -> dict[int, str]:
    modifiers =  CONFIG['workspace_shortcuts']['modifiers']

    workspaces: dict[int, str] = {}
    for (num, hotkey) in get_workspace_keys().items():
        workspaces[num] = f"{modifiers}+{hotkey}"

    return workspaces

def get_workspace_programs() -> dict[int, str]:
    workspaces: dict[int, str] = {}
    for (key, hotkey) in  CONFIG['workspace_programs'].items():
        workspace_num = int(key.split('_')[1])
        workspaces[workspace_num] = hotkey

    return workspaces

def get_workspace_names() -> dict[int, str]:
    workspaces: dict[int, str] = {}
    for (key, name) in  CONFIG['workspace_names'].items():
        workspace_num = int(key.split('_')[1])
        workspaces[workspace_num] = name

    return workspaces

Workspace_config = namedtuple('Workspace_config', ['hotkey', 'program', 'name', 'number'])
def get_workspace_config() -> dict[int, Workspace_config]:
    hotkeys = get_workspace_hotkeys()
    programs = get_workspace_programs()
    names = get_workspace_names()

    workspaces: dict[int, Workspace_config] = {}

    for i in range(len(hotkeys)):
        workspaces[i+1] = Workspace_config(hotkey=hotkeys[i+1], program=programs[i+1], name=names[i+1], number=i+1)

    return workspaces