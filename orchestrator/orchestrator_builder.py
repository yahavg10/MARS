import os
from typing import Callable, Optional

from PipelineExecutor.pipelineExecutor import PipelineExecutor
from communication.sender import Sender
from config_models.app_model import AppConfig
from data_managment.database import Database
from orchestrator.orchestrator import Orchestrator


class OrchestratorBuilder:
    def __init__(self):
        self.configuration: Optional[AppConfig] = None
        self._database: Optional[Database] = None
        self._sender: Optional[Sender] = None
        self._pipeline_executor: Optional[PipelineExecutor] = None

    def with_configuration(self, config_model: AppConfig, load_conf_fn: Callable) -> 'OrchestratorBuilder':
        with open(file=os.environ["CONFIG_FILE_PATH"]) as config_file:
            config_data = load_conf_fn(config_file)
        self.configuration = config_model.from_dict(config_data, config_model)
        return self

    def with_database(self, database_class, store_fn: Callable, fetch_fn: Callable,
                      delete_fn: Callable) -> 'OrchestratorBuilder':
        self._database = Database(database_class, store_fn,
                                  fetch_fn,
                                  delete_fn,
                                  self.configuration.components.database)
        return self

    def with_sender(self, create_payload_fn: Callable) -> 'OrchestratorBuilder':
        self._sender = Sender(create_payload_fn)
        return self

    def with_pipeline_executor(self, pipeline_fn: Callable) -> 'OrchestratorBuilder':
        if not self._database or not self._sender:
            raise ValueError("Database and Sender must be set before Processor.")

        temp_orchestrator = Orchestrator(pipeline_executor=None, database=self._database, sender=self._sender,
                                         configuration=self.configuration)

        self._pipeline_executor = PipelineExecutor(pipeline_fn, temp_orchestrator)

        return self

    def build(self) -> Orchestrator:
        orchestrator = Orchestrator(pipeline_executor=self._pipeline_executor, database=self._database,
                                    sender=self._sender,
                                    configuration=self.configuration)
        return orchestrator
