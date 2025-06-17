import logging
import sys
import os
import time
import json
import inspect
import threading
from datetime import datetime
from scripts import config_loader
from scripts.log_levels import LogLevel

_LOG_DIR = os.path.join(os.path.dirname(__file__), "logs")
os.makedirs(_LOG_DIR, exist_ok=True)

_LOG_FILE = os.path.join(_LOG_DIR, f"{datetime.now():%Y-%m-%d_%H-%M-%S}.json")

_DISABLED_LEVELS = config_loader.get_disabled_log_levels()

class JSON_Formatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "timestamp": datetime.utcfromtimestamp(record.created).isoformat() + "Z",
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
        }
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        return json.dumps(payload, ensure_ascii=False)

def _setup_logger(level: LogLevel = LogLevel.INFO) -> logging.Logger|None:
    """
    Configure root logger ONCE: console handler + JSON file handler.
    """
    if not config_loader.get_logging_allowed():
        return None

    root = logging.getLogger()
    root.setLevel(getattr(logging, level.name))
    
    if root.handlers:
        root.handlers.clear()

    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(
        logging.Formatter("%(asctime)s | %(levelname)-8s | %(name)-50s | %(message)s")
    )
    root.addHandler(ch)

    fh = logging.FileHandler(_LOG_FILE, mode="a", encoding="utf-8")
    fh.setFormatter(JSON_Formatter())
    root.addHandler(fh)
    
    return root

_root_logger: logging.Logger|None = _setup_logger()

def write_entry(message: str, level: LogLevel = LogLevel.INFO, **kwargs):
    """
    Universal log function:
      • message: your log text
      • level: LogLevel enum
      • kwargs: passed to logger.log (e.g. exc_info=True)
    """
    global _root_logger

    if not config_loader.get_logging_allowed() or level in _DISABLED_LEVELS:
        return
    if _root_logger is None:
        _root_logger = _setup_logger()
        
    if _root_logger is None:
        raise RuntimeError("Logger not initialized")
        
    frame = inspect.currentframe()
    caller_frame = frame.f_back if frame else None
    module_name = None
    if caller_frame:
        module_name = caller_frame.f_globals.get("__name__", "root")

    logger = logging.getLogger(module_name)
    lvl = getattr(logging, level.name)
    logger.log(lvl, message, **kwargs)

def _handle_exception(exc_type, exc_value, exc_traceback):
    """Handle uncaught exceptions"""
    global _root_logger
    
    print(f"EXCEPTION HANDLER CALLED: {exc_type.__name__}: {exc_value}")
    
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    try:
        if not config_loader.get_logging_allowed():
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return

        if _root_logger is None:
            _root_logger = _setup_logger()
            
        if _root_logger is None:
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return

        _root_logger.critical("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

        for handler in _root_logger.handlers:
            handler.flush()
        
    except Exception as log_error:
        print(f"Error while logging thread exception: {log_error}")
        sys.__excepthook__(exc_type, exc_value, exc_traceback)

    finally:
        time.sleep(0.5)
        os._exit(1)

def thread_excepthook(args):
    """Handle uncaught exceptions in threads"""
    global _root_logger

    print(f"THREAD EXCEPTION HANDLER CALLED: {args.exc_type.__name__}: {args.exc_value}")
    
    if issubclass(args.exc_type, KeyboardInterrupt):
        return

    try:
        if not config_loader.get_logging_allowed():
            return

        if _root_logger is None:
            _root_logger = _setup_logger()
            
        if _root_logger is None:
            return

        _root_logger.critical(f"Uncaught exception in thread {args.thread.name!r}", 
                            exc_info=(args.exc_type, args.exc_value, args.exc_traceback))

        for handler in _root_logger.handlers:
            handler.flush()
        
    except Exception as log_error:
        print(f"Error while logging thread exception: {log_error}")

    finally:
        time.sleep(0.5)
        os._exit(1)

sys.excepthook = _handle_exception
threading.excepthook = thread_excepthook