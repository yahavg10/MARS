from typing import Optional, NoReturn

from watchdog.events import FileSystemEventHandler

from communication.sender import Sender
from config_models.app_model import AppConfig
from data_managment.database import Database
from processoring.processor import Processor


class Handler(FileSystemEventHandler):
    def __init__(self, processor: Optional[Processor], database: Optional[Database], sender: Optional[Sender],
                 configuration: Optional[AppConfig]) -> NoReturn:
        self.configuration = configuration
        self.processor = processor
        self.database = database
        self.sender = sender

    def on_created(self, event) -> NoReturn:
        self.processor.strategy_pool.pool.submit(self.processor.process,
                                                 kwargs={'event_type': event.event_type, 'src_path': event.src_path})
