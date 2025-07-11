# SOURCE:
# https://docs.microsoft.com/en-us/windows/win32/inputdev/virtual-key-codes

VK_CODES: dict[str, int] = {
    "LBUTTON":          0x01, # Left mouse button"
    "RBUTTON":          0x02, # Right mouse button"
    "CANCEL":           0x03, # Control-break processing"
    "MBUTTON":          0x04, # Middle mouse button"
    "XBUTTON1":         0x05, # X1 mouse button"
    "XBUTTON2":         0x06, # X2 mouse button"
    "BACK":             0x08, # Backspace key"
    "TAB":              0x09, # Tab key"
    "CLEAR":            0x0C, # Clear key"
    "RETURN":           0x0D, # Enter key"
    "SHIFT":            0x10, # Shift key"
    "CONTROL":          0x11, # Ctrl key"
    "MENU":             0x12, # Alt key"
    "PAUSE":            0x13, # Pause key"
    "CAPITAL":          0x14, # Caps lock key"
    "KANA":             0x15, # IME Kana mode"
    "HANGUL":           0x15, # IME Hangul mode"
    "IME_ON":           0x16, # IME On"
    "JUNJA":            0x17, # IME Junja mode"
    "FINAL":            0x18, # IME final mode"
    "HANJA":            0x19, # IME Hanja mode"
    "KANJI":            0x19, # IME Kanji mode"
    "IME_OFF":          0x1A, # IME Off"
    "ESCAPE":           0x1B, # Esc key"
    "CONVERT":          0x1C, # IME convert"
    "NONCONVERT":       0x1D, # IME nonconvert"
    "ACCEPT":           0x1E, # IME accept"
    "MODECHANGE":       0x1F, # IME mode change request"
    "SPACE":            0x20, # Spacebar key"
    "PRIOR":            0x21, # Page up key"
    "NEXT":             0x22, # Page down key"
    "END":              0x23, # End key"
    "HOME":             0x24, # Home key"
    "LEFT":             0x25, # Left arrow key"
    "UP":               0x26, # Up arrow key"
    "RIGHT":            0x27, # Right arrow key"
    "DOWN":             0x28, # Down arrow key"
    "SELECT":           0x29, # Select key"
    "PRINT":            0x2A, # Print key"
    "EXECUTE":          0x2B, # Execute key"
    "SNAPSHOT":         0x2C, # Print screen key"
    "INSERT":           0x2D, # Insert key"
    "DELETE":           0x2E, # Delete key"
    "HELP":             0x2F, # Help key"
    "LWIN":             0x5B, # Left Windows logo key"
    "RWIN":             0x5C, # Right Windows logo key"
    "APPS":             0x5D, # Application key"
    "SLEEP":            0x5F, # Computer Sleep key"
    "NUMPAD0":          0x60, # Numeric keypad 0 key"
    "NUMPAD1":          0x61, # Numeric keypad 1 key"
    "NUMPAD2":          0x62, # Numeric keypad 2 key"
    "NUMPAD3":          0x63, # Numeric keypad 3 key"
    "NUMPAD4":          0x64, # Numeric keypad 4 key"
    "NUMPAD5":          0x65, # Numeric keypad 5 key"
    "NUMPAD6":          0x66, # Numeric keypad 6 key"
    "NUMPAD7":          0x67, # Numeric keypad 7 key"
    "NUMPAD8":          0x68, # Numeric keypad 8 key"
    "NUMPAD9":          0x69, # Numeric keypad 9 key"
    "MULTIPLY":         0x6A, # Multiply key"
    "ADD":              0x6B, # Add key"
    "SEPARATOR":        0x6C, # Separator key"
    "SUBTRACT":         0x6D, # Subtract key"
    "DECIMAL":          0x6E, # Decimal key"
    "DIVIDE":           0x6F, # Divide key"
    "F1":               0x70, # F1 key"
    "F2":               0x71, # F2 key"
    "F3":               0x72, # F3 key"
    "F4":               0x73, # F4 key"
    "F5":               0x74, # F5 key"
    "F6":               0x75, # F6 key"
    "F7":               0x76, # F7 key"
    "F8":               0x77, # F8 key"
    "F9":               0x78, # F9 key"
    "F10":              0x79, # F10 key"
    "F11":              0x7A, # F11 key"
    "F12":              0x7B, # F12 key"
    "F13":              0x7C, # F13 key"
    "F14":              0x7D, # F14 key"
    "F15":              0x7E, # F15 key"
    "F16":              0x7F, # F16 key"
    "F17":              0x80, # F17 key"
    "F18":              0x81, # F18 key"
    "F19":              0x82, # F19 key"
    "F20":              0x83, # F20 key"
    "F21":              0x84, # F21 key"
    "F22":              0x85, # F22 key"
    "F23":              0x86, # F23 key"
    "F24":              0x87, # F24 key"
    "NUMLOCK":          0x90, # Num lock key"
    "SCROLL":           0x91, # Scroll lock key"
    "LSHIFT":           0xA0, # Left Shift key"
    "RSHIFT":           0xA1, # Right Shift key"
    "LCONTROL":         0xA2, # Left Ctrl key"
    "RCONTROL":         0xA3, # Right Ctrl key"
    "LMENU":            0xA4, # Left Alt key"
    "RMENU":            0xA5, # Right Alt key"
    "BROWSER_BACK":     0xA6, # Browser Back key"
    "BROWSER_FORWARD":  0xA7, # Browser Forward key"
    "BROWSER_REFRESH":  0xA8, # Browser Refresh key"
    "BROWSER_STOP":     0xA9, # Browser Stop key"
    "BROWSER_SEARCH":   0xAA, # Browser Search key"
    "BROWSER_FAVORITES": 0xAB, # Browser Favorites key"
    "BROWSER_HOME":     0xAC, # Browser Start and Home key"
    "VOLUME_MUTE":      0xAD, # Volume Mute key"
    "VOLUME_DOWN":      0xAE, # Volume Down key"
    "VOLUME_UP":        0xAF, # Volume Up key"
    "MEDIA_NEXT_TRACK": 0xB0, # Next Track key"
    "MEDIA_PREV_TRACK": 0xB1, # Previous Track key"
    "MEDIA_STOP":       0xB2, # Stop Media key"
    "MEDIA_PLAY_PAUSE": 0xB3, # Play/Pause Media key"
    "LAUNCH_MAIL":      0xB4, # Start Mail key"
    "LAUNCH_MEDIA_SELECT": 0xB5, # Select Media key"
    "LAUNCH_APP1":      0xB6, # Start Application 1 key"
    "LAUNCH_APP2":      0xB7, # Start Application 2 key"
    "OEM_1":            0xBA, # Miscellaneous (US ;:) key"
    "OEM_PLUS":         0xBB, # Plus ('+') key"
    "OEM_COMMA":        0xBC, # Comma (',') key"
    "OEM_MINUS":        0xBD, # Minus ('-') key"
    "OEM_PERIOD":       0xBE, # Period ('.') key"
    "OEM_2":            0xBF, # Miscellaneous (US /?) key"
    "OEM_3":            0xC0, # Miscellaneous (US "~) key"
    "OEM_4":            0xDB, # Miscellaneous (US [{) key"
    "OEM_5":            0xDC, # Miscellaneous (US \\|) key"
    "OEM_6":            0xDD, # Miscellaneous (US ]}) key"
    "OEM_7":            0xDE, # Miscellaneous (US '\\\") key"
    "OEM_8":            0xDF, # Miscellaneous (OEM 8) key"
    "OEM_102":          0xE2, # Miscellaneous (<>) or (\\|) key"
    "PROCESSKEY":       0xE5, # IME PROCESS key"
    "PACKET":           0xE7, # Pass Unicode characters as keystrokes"
    "ATTN":             0xF6, # Attn key"
    "CRSEL":            0xF7, # CrSel key"
    "EXSEL":            0xF8, # ExSel key"
    "EREOF":            0xF9, # Erase EOF key"
    "PLAY":             0xFA, # Play key"
    "ZOOM":             0xFB, # Zoom key"
    "NONAME":           0xFC, # Reserved"
    "PA1":              0xFD, # PA1 key"
    "OEM_CLEAR":        0xFE, # Clear key"
    "0":                0x30, #0 key
    "1":                0x31, #1 key
    "2":                0x32, #2 key
    "3":                0x33, #3 key
    "4":                0x34, #4 key
    "5":                0x35, #5 key
    "6":                0x36, #6 key
    "7":                0x37, #7 key
    "8":                0x38, #8 key
    "9":                0x39, #9 key
    "A":                0x41, #A key
    "B":                0x42, #B key
    "C":                0x43, #C key
    "D":                0x44, #D key
    "E":                0x45, #E key
    "F":                0x46, #F key
    "G":                0x47, #G key
    "H":                0x48, #H key
    "I":                0x49, #I key
    "J":                0x4A, #J key
    "K":                0x4B, #K key
    "L":                0x4C, #L key
    "M":                0x4D, #M key
    "N":                0x4E, #N key
    "O":                0x4F, #O key
    "P":                0x50, #P key
    "Q":                0x51, #Q key
    "R":                0x52, #R key
    "S":                0x53, #S key
    "T":                0x54, #T key
    "U":                0x55, #U key
    "V":                0x56, #V key
    "W":                0x57, #W key
    "X":                0x58, #X key
    "Y":                0x59, #Y key
    "Z":                0x5A #Z key
}

CONFIG_STR_TO_VK: dict[str, int]= {
    "<alt>":             VK_CODES["MENU"],
    "<alt_l>":           VK_CODES["LMENU"],
    "<alt_r>":           VK_CODES["RMENU"],
    "<alt_gr>":          VK_CODES["RMENU"],
    "<backspace>":       VK_CODES["BACK"],
    "<caps_lock>":       VK_CODES["CAPITAL"],
    "<cmd>":             VK_CODES["LWIN"],
    "<cmd_l>":           VK_CODES["LWIN"],
    "<cmd_r>":           VK_CODES["RWIN"],
    "<ctrl>":            VK_CODES["CONTROL"],
    "<ctrl_l>":          VK_CODES["LCONTROL"],
    "<ctrl_r>":          VK_CODES["RCONTROL"],
    "<delete>":          VK_CODES["DELETE"],
    "<down>":            VK_CODES["DOWN"],
    "<end>":             VK_CODES["END"],
    "<enter>":           VK_CODES["RETURN"],
    "<esc>":             VK_CODES["ESCAPE"],
    **{f"<f{i}>":         VK_CODES[f"F{i}"] for i in range(1, 21)},
    "<home>":            VK_CODES["HOME"],
    "<insert>":          VK_CODES["INSERT"],
    "<left>":            VK_CODES["LEFT"],
    "<menu>":            VK_CODES["APPS"],
    "<media_play_pause>":VK_CODES["MEDIA_PLAY_PAUSE"],
    "<media_previous>":  VK_CODES["MEDIA_PREV_TRACK"],
    "<media_next>":      VK_CODES["MEDIA_NEXT_TRACK"],
    "<media_volume_down>":VK_CODES["VOLUME_DOWN"],
    "<media_volume_mute>":VK_CODES["VOLUME_MUTE"],
    "<media_volume_up>": VK_CODES["VOLUME_UP"],
    "<num_lock>":        VK_CODES["NUMLOCK"],
    **{f"<num_{i}>":      VK_CODES[f"NUMPAD{i}"] for i in range(10)},
    "<page_down>":       VK_CODES["NEXT"],   
    "<page_up>":         VK_CODES["PRIOR"],
    "<pause>":           VK_CODES["PAUSE"],
    "<print_screen>":    VK_CODES["SNAPSHOT"],
    "<right>":           VK_CODES["RIGHT"],
    "<scroll_lock>":     VK_CODES["SCROLL"],
    "<shift>":           VK_CODES["SHIFT"],
    "<shift_l>":         VK_CODES["LSHIFT"],
    "<shift_r>":         VK_CODES["RSHIFT"],
    "<space>":           VK_CODES["SPACE"],
    "<tab>":             VK_CODES["TAB"],
    "<up>":              VK_CODES["UP"],
}

