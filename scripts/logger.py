import logging
import sys
import os
import json
import inspect
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
    if not root.handlers:
        ch = logging.StreamHandler(sys.stdout)
        ch.setFormatter(
            logging.Formatter("%(asctime)s | %(levelname)-8s | %(name)-50s | %(message)s")
        )
        root.addHandler(ch)

        fh = logging.FileHandler(_LOG_FILE, mode="w", encoding="utf-8")
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
        raise RuntimeError("Logger not initialized")
    frame = inspect.currentframe()
    caller_frame = frame.f_back if frame else None
    module_name = None
    if caller_frame:
        module_name = caller_frame.f_globals.get("__name__", "root")
    # Get a logger for that module (handlers attached at root)
    logger = logging.getLogger(module_name)
    lvl = getattr(logging, level.name)
    logger.log(lvl, message, **kwargs)

def _handle_exception(exc_type, exc_value, exc_traceback):
    global _root_logger

    if _root_logger is None:
        raise RuntimeError("Logger not initialized")

    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    _root_logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

if config_loader.get_logging_allowed():
    sys.excepthook = _handle_exception