import logging
from typing import NoReturn

from watchdog.observers import Observer
from watchdog.observers.api import BaseObserver

logger = logging.getLogger(name="finals_logger")


def create_observer(handler, folder_to_monitor: str) -> BaseObserver:
    observer = Observer()
    observer.schedule(handler, folder_to_monitor, recursive=False)
    return observer if isinstance(folder_to_monitor, str) else TypeError


def start_observer(observer) -> NoReturn:
    try:
        observer.start()
        observer.join()
    except KeyboardInterrupt:
        observer.stop()
        logger.info("Monitoring stopped due to user interruption.")
    except Exception as e:
        observer.stop()
        logger.error(str(e))
