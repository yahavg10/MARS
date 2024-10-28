import os
from typing import Callable, Optional

from communication.sender import Sender
from config_models.app_model import AppConfig
from data_managment.database import Database
from handling.handler import Handler
from processoring.processor import Processor


class HandlerBuilder:
    def __init__(self):
        self.configuration: Optional[AppConfig] = None
        self._database: Optional[Database] = None
        self._sender: Optional[Sender] = None
        self._processor: Optional[Processor] = None

    def with_configuration(self, config_model: AppConfig, load_conf_fn: Callable) -> 'HandlerBuilder':
        with open(file=os.environ["CONFIG_FILE_PATH"]) as config_file:
            config_data = load_conf_fn(config_file)
        self.configuration = config_model.from_dict(config_data, config_model)
        return self

    def with_database(self, database_class, store_fn: Callable, fetch_fn: Callable,
                      delete_fn: Callable) -> 'HandlerBuilder':
        self._database = Database(database_class, store_fn,
                                  fetch_fn,
                                  delete_fn,
                                  self.configuration.components.database)
        return self

    def with_sender(self, create_payload_fn: Callable) -> 'HandlerBuilder':
        self._sender = Sender(create_payload_fn)
        return self

    def with_processor(self, process_fn: Callable) -> 'HandlerBuilder':
        if not self._database or not self._sender:
            raise ValueError("Database and Sender must be set before Processor.")

        temp_handler = Handler(processor=None, database=self._database, sender=self._sender,
                               configuration=self.configuration)

        self._processor = Processor(process_fn, temp_handler)

        return self

    def build(self) -> Handler:
        handler = Handler(processor=self._processor, database=self._database, sender=self._sender,
                          configuration=self.configuration)
        return handler
