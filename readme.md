# Custom Hotkey Manager

## Description

This project provides custom hotkeys for windows. It includes a system tray icon and a hotkey listener to handle user interactions.

## Installation

1. Clone the repository to your local machine.
2. Ensure you have Python installed (preferably version 3.6 or later).
3. Install the required dependencies:

   ```sh
   pip install infi.systray pynput pywin32
   ```

## Configuration

The configuration is managed in `config.toml`. You can customize hotkeys and other settings as needed.

- **General**: Contains general settings, currently the title of the tray icon.
- **Hotkeys**: Define custom key bindings for various actions.
- **Applications**: Specify which application should use the custom hotkeys.

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
```

## Usage

1. Start the script to launch the system tray icon and hotkey listener:

   ```sh
   python ./shortkeys.py
   ```

2. The system tray icon will appear in your taskbar, allowing you to access configuration options and stop the script.

3. Press the custom hotkeys as defined in `config.toml`.

## Adding New Shortcuts

To add a new shortcut, follow these steps:

1. Open the `config.toml` file.
2. Add a new key-value pair under the `[hotkeys]` section. The key is the name of the shortcut, and the value is the hotkey combination.

   ```toml
   [hotkeys]
   my_new_shortcut = '<ctrl>+<alt>+n'
   ```

3. In the `scripts/hotkey_listener.py` file, add a new case to the `shortcuts` switch.<br>
   I would recommend to use a lambda function that wraps your new function with `last_window.set_last_window` to ensure that the last active window gets saved in case you change window focus.<br>

   ```python
   for shortcut_name in shortcuts:
    shortcut_value = shortcuts[shortcut_name]

    match shortcut_name:
        
        case # Other cases...

        case 'my_new_shortcut':
            hotkeys[shortcut_value] = lambda: last_window.set_last_window(<ins>my_new_function</ins>)
   ```

4. Add your corresponding function in the `scripts/hotkey_functions/` directory file.

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

These functions can be used to create custom hotkey actions in your script.
