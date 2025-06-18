from ctypes import wintypes
from scripts.win_api.event_codes import WinEventMessages
from typing import Callable
import ctypes

def create_listener(
            wMsgFilterMin: WinEventMessages, 
            wMsgFilterMax: WinEventMessages, 
            hwnd: int|None = None
        ) -> Callable[[], None]:
    """ 
    Create a message loop to handle win events. Retuns a function that starts the listener. 
    For more details about the parameters see https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getmessagea

    :param wMsgFilterMin: Minimum event message to filter. Set both wMsgFilterMin & wMsgFilterMax to WM_NULL to listen for all events.
    :param wMsgFilterMax: Maximum event message to filter.
    :param hwnd: window handle to listen for events on. If None, listens for all windows.

    :return: A function that starts the listener.
    """
    
    hwnd = 0 if hwnd is None else hwnd

    def start() -> None:
        """ Starts the listener """
        msg = wintypes.MSG()
        while ctypes.windll.user32.GetMessageA(ctypes.byref(msg), hwnd, wMsgFilterMin, wMsgFilterMax) != 0:
            ctypes.windll.user32.TranslateMessage(ctypes.byref(msg))
            ctypes.windll.user32.DispatchMessageA(ctypes.byref(msg))

    return start

def stop_listener(thread_id: int) -> None:
    """ Stops a message loop by sending a quit message """
    send_message_to_listener(thread_id, WinEventMessages.WM_QUIT)

def send_message_to_listener(
            thread_id: int, 
            msg: WinEventMessages, 
            wParam: wintypes.WPARAM|None = None, 
            lParam: wintypes.LPARAM|None = None
        ) -> None:
    """ Stops a message loop by posting a quit message to the thread with the given ID. """
    wParam = wintypes.WPARAM(0) if wParam is None else wParam
    lParam = wintypes.LPARAM(0) if lParam is None else lParam

    ctypes.windll.user32.PostThreadMessageW(thread_id, msg, wParam, lParam)
