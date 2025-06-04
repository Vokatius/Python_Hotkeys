import tomllib

def get_config() -> dict[str, dict[str, str]]:
    with open('config.toml', "rb") as config_pointer:
        config = tomllib.load(config_pointer)

    return config

def get_script_name() -> str:
    return get_config()['general']['title']

def get_hotkeys() -> dict[str, str]:
    return get_config()['hotkeys']

def get_applications() -> dict[str, str]:
    return get_config()['applications']