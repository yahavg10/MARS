from typing import Optional, NoReturn

from watchdog.events import FileSystemEventHandler

from PipelineExecutor.pipelineExecutor import PipelineExecutor
from communication.sender import Sender
from config_models.app_model import AppConfig
from data_managment.database import Database


class Orchestrator(FileSystemEventHandler):
    def __init__(self, pipeline_executor: Optional[PipelineExecutor], database: Optional[Database],
                 sender: Optional[Sender],
                 configuration: Optional[AppConfig]) -> NoReturn:
        self.configuration = configuration
        self.pipeline_executor = pipeline_executor
        self.database = database
        self.sender = sender

    def on_created(self, event) -> NoReturn:
        self.pipeline_executor.strategy_pool.pool.submit(self.pipeline_executor.process,
                                                         kwargs={'event_type': event.event_type,
                                                                 'src_path': event.src_path})
