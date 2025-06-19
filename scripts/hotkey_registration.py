from scripts.hotkey_functions import browser, last_window, workspace
from scripts import config_loader
from scripts.key_interceptor import register_hotkey, register_hotkey_raw

_app_ids = config_loader.get_applications()
for (num, workspace_conf) in config_loader.get_workspace_config().items():
    if(workspace_conf.program is False): 
        # Passing workspace_conf.number as parameter n to avoid passing by reference
        register_hotkey_raw(workspace_conf.hotkey, lambda n=workspace_conf.number: workspace.goto_workspace(n))
    else:        
        app_id = _app_ids[workspace_conf.program]
        register_hotkey_raw(workspace_conf.hotkey, lambda n=workspace_conf.number, p=app_id: workspace.goto_workspace(n,p))

_modifier_move = config_loader.get_hotkeys()['move_program_to_workspace']
_modifier_goto = config_loader.get_hotkeys()['goto_workspace_with_program']
for (num, workspace_key) in config_loader.get_workspace_keys().items():
    if _modifier_move is not False:
        register_hotkey_raw(f"{_modifier_move}+{workspace_key}", lambda n=num: workspace.move_program_to_workspace(n))
    if _modifier_goto is not False:
        register_hotkey_raw(f"{_modifier_goto}+{workspace_key}", lambda n=num: workspace.goto_workspace_with_program(n))

register_hotkey('goto_previous_program', last_window.focus_last_window)
register_hotkey('open_web_tab', lambda: last_window.set_last_window(browser.open_new_tab))
register_hotkey('query_chatGPT', lambda: last_window.set_last_window(browser.open_chatgpt))
register_hotkey('pin_current_window_toggle', workspace.toggle_pin_window)
register_hotkey('goto_previous_workspace', workspace.goto_previous_workspace)
register_hotkey('move_program_to_home', workspace.move_program_to_home) 