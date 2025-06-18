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
    
def get_module_handle(module : wintypes.LPCWSTR|None = None) -> wintypes.HANDLE|None:
    """ Returns the handle of a module. If module is None, returns the handle of the current process. """
    return ctypes.windll.kernel32.GetModuleHandleW(module)