from typing import NoReturn

import yaml

from PipelineExecutor.toolbox import scan_existing_files
from base_selective_methods import setup_toolbox, file_sender_function, \
    database_delete_function, database_fetch_function, database_store_function, database_class, pipeline_fn
from config_models.app_model import AppConfig
from orchestrator.orchestrator_builder import OrchestratorBuilder
from utils.logger_utils import setup_custom_logger
from utils.observe import create_observer, start_observer


def configure_orchestrator_builder() -> NoReturn:
    builder = OrchestratorBuilder()
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
            .with_pipeline_executor(pipeline_fn)
            .build()
    )


def main() -> NoReturn:
    orchestrator = configure_orchestrator_builder()
    setup_toolbox(orchestrator)

    setup_custom_logger(orchestrator.configuration.logger)

    observer = create_observer(orchestrator=orchestrator,
                               folder_to_monitor=orchestrator.configuration.components.pipeline_executor["folder_path"])

    scan_existing_files(orchestrator)
    start_observer(observer)


if __name__ == "__main__":
    main()
