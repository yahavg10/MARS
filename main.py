from typing import NoReturn

import yaml

from base_selective_methods import setup_toolbox, file_sender_function, process_handler_function, \
    database_delete_function, database_fetch_function, database_store_function, database_class
from config_models.app_model import AppConfig
from handling.handler_builder import HandlerBuilder
from processoring.toolbox import scan_existing_files
from utils.logger_utils import setup_custom_logger
from utils.observe import create_observer, start_observer


def configure_handler_builder() -> NoReturn:
    builder = HandlerBuilder()
    return (
        builder
            .with_configuration(AppConfig, yaml.safe_load)
            .with_database(
            database_class=database_class,
            store_fn=database_store_function,
            fetch_fn=database_fetch_function,
            delete_fn=database_delete_function,
        )
            .with_sender(file_sender_function)
            .with_processor(process_handler_function)
            .build()
    )


def main() -> NoReturn:
    handler = configure_handler_builder()
    setup_toolbox(handler)

    setup_custom_logger(handler.configuration.logger)

    observer = create_observer(handler=handler,
                               folder_to_monitor=handler.configuration.components.processor["folder_path"])
    start_observer(observer)
    # scan_existing_files(handler)


if __name__ == "__main__":
    main()
