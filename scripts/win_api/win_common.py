import ctypes
import psutil
from ctypes import wintypes

_GET_TICK_COUNT = ctypes.windll.kernel32.GetTickCount64
_GET_TICK_COUNT.restype = ctypes.c_ulonglong

def get_tick_count() -> int:
    """ Returns the current system tick count. """
    return _GET_TICK_COUNT()

def get_pid(hwnd: int) -> int:
    pid = wintypes.DWORD()
    ctypes.windll.user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
    return pid.value

def get_name(pid: int) -> str|None:
    try:
        return psutil.Process(pid).name().lower()
    except psutil.NoSuchProcess:
        return None