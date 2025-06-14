# Custom Hotkey Manager

## Description

This project provides custom hotkeys for windows. It includes a system tray icon and a hotkey listener to handle user interactions.

## Installation

1. Clone the repository to your local machine.
2. Ensure you have Python installed (preferably version 3.6 or later).
3. Install the required dependencies:

   ```sh
   pip install -r requirements.txt
   ```

## Configuration

The configuration is managed in `config.toml`. You can customize hotkeys and other settings as needed.

- **General**: Contains general settings.
- **Hotkeys**: Define custom key bindings for various actions.
- **Applications**: Specify which application should use the custom hotkeys.
- **Workspaces**: Specifiy bindings to access virtual desktops with default programs

Example:

```toml
[general]
title = 'Custom Hotkeys'

[hotkeys]
focus_web_browser = '<alt>+t'
open_web_tab = '<ctrl>+<space>'
goto_previous = '<cmd>+z'

[applications]
web_browser = 'edge'

[workspace_shortcuts]
modifiers = 'alt'
goto_workpace_1 = '1'
goto_workpace_2 = '2'

[workspace_programs]
workspace_1_open = 'web_browser'
workspace_2_open = false
```

## Usage

1. Start the script to launch the system tray icon and hotkey listener:

   ```sh
   python ./shortkeys.py
   ```

2. The system tray icon will appear in your taskbar, allowing you to access configuration options and stop the script.

3. Open the system tray options to change the `config.toml` and restart the script.

4. Press the custom hotkeys as defined in `config.toml`.

## Adding New Shortcuts

To add a new shortcut, follow these steps:

1. Open the `config.toml` file.
2. Add a new key-value pair under the `[hotkeys]` section. The key is the name of the shortcut, and the value is the hotkey combination.

   ```toml
   [hotkeys]
   my_new_shortcut = '<ctrl>+<alt>+n'
   ```

3. Add your corresponding function in the `scripts/hotkey_functions/` directory either in a file or an exisiting one.

4. In the `scripts/hotkey_registration.py` file, append your new shortcut using `register_hotkey`<br>
   I would recommend to use a lambda function that wraps your new function with `last_window.set_last_window` to ensure that the last active window gets saved in case you change window focus.<br>

   ```python
   register_hotkey('my_new_shortcut', lambda: last_window.set_last_window(my_file.function))
   ```

5. Restart the script for the changes to take effect.

## Predefined Functions

### foreground.py
The `foreground.py` module provides functions to bring a window to the foreground.

>  ```python
>  send_to_foreground_name(name: str, callback: Callable[[], None]|None = None) -> None
> ```
> Brings a window with the specified name to the foreground. If a callback function is provided, it will be executed after the window is brought to the foreground.

> ```python
> send_to_foreground_hwnd(hwnd: int) -> None
> ```
> Brings a window with the specified handle to the foreground.

> ```python 
> is_foreground(hwnd: int) -> bool
> ```
> Checks if the window with the specified handle is currently in the foreground.

### send_key.py
The `send_key.py` module provides functions to simulate key presses and shortcuts.

> ```python 
> press_key(key_code: int) -> None
> ```
> Simulates a key press.

> ```python 
> release_key(key_code: int) -> None
> ```
> Simulates a key release.

> ```python 
> send_key(key_code: int, sleep: float|None = None) -> None
> ```
> Simulates a single key press and release. If a sleep duration is provided, the function will pause for that amount of time before releasing the key.

> ```python 
> send_shortcut(shortcut: list[int], sleep: float|None = None) -> None
> ```
>  Simulates a sequence of key presses and releases to form a shortcut. If a sleep duration is provided, the function will pause for that amount of time after each key press.

### `open_program.py`
The `open_program.py` module makes it easy to launch programs and determine whether they’re already running on a given virtual desktop.

> ```python
> open_app(app_id: str) -> None
> ```
> Launches the application using `app_id`. App ids can be found inside `app_data.json` after running the script for the first time

> ```python
> open_app_if_closed(app_id: str) -> None
> ```
> Opens the application only if it is not already running, preventing duplicate instances.

> ```python
> is_program_open(app_id: str, only_curr_workspace: bool = True) -> bool
> ```
> Returns **True** if a window for `app_id` is open. By default it checks only the current virtual desktop; set `only_curr_workspace=False` to scan every workspace.

> ```python
> is_default_open(app_id: str, workspace_num: int) -> bool
> ```
> Determines whether the default application of workspace_num is open. Ignores pinned instances of the default application if set in the `config.toml` file.

> ```python
> get_app_id(ptr: int | None) -> str | None
> ```
> Converts a raw pointer from the Windows API into an `app_id` string. Returns `None` if `ptr` itself is `None`. Used translate `AppView.appId` pointer.

### `workspace.py`
The `workspace.py` module provides helpers for Windows Virtual Desktops—jump between workspaces, pin or unpin windows, shuffle apps around, and hop back to the previous desktop.

> ```python
> goto_workspace(workspace_num: int, app_id: str | None = None) -> None
> ```
> Switches to `workspace_num`, remembers where you came from, and—if you pass an `app_id`—launches that application there (unless it is already open).

> ```python
> toggle_pin_window() -> None
> ```
> Toggles the current window’s pin status. Pinning makes it visible on every desktop; unpinning confines it to a single desktop.

> ```python
> goto_previous_workspace() -> None
> ```
> Jumps back to the workspace you were on before the last switch.

> ```python
> move_program_to_workspace(workspace_num: int) -> None
> ```
> Moves the active window to `workspace_num` without changing your own view.

> ```python
> goto_workspace_with_program(workspace_num: int) -> None
> ```
> Combines two steps: first shifts the current window to `workspace_num`, then immediately switches to that desktop.

These functions can be used to create custom hotkey actions in your script.
