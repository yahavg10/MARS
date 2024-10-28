import logging
import os
from pathlib import Path
from threading import Timer
from typing import List
from typing import NoReturn

from watchdog.events import FileCreatedEvent

from handling.handler import Handler
from utils.variables_utils import suffixes

logger = logging.getLogger(name="finals_logger")


def cleanup_files(processor, common_name: str, suffix: str,
                  delete_all_occurrences: bool) -> NoReturn:
    delete_files_from_os(common_name, delete_all_occurrences, processor, suffix)
    delete_files_from_db(common_name, processor, suffix)


def delete_files_from_db(common_name: str, processor, suffix: str) -> NoReturn:
    try:
        processor.db_strategy.fetch(common_name) and processor.db_strategy.delete(common_name)
        logger.info(f"Cleaned up file {common_name + suffix}")
    except Exception as e:
        logger.error(f"Error cleaning up files: {str(e)}")


def delete_files_from_os(common_name: str, delete_all_occurrences: bool, processor,
                         suffix: str) -> NoReturn:
    file_path = processor.folder_path + common_name
    if delete_all_occurrences:
        [os.remove(file_path + suffix) for suffix in suffixes if os.path.exists(file_path + suffix)]
    else:
        os.path.exists(file_path + suffix) and os.remove(file_path + suffix)


def schedule_file_removal(processor, common_name: str, suffix: str,
                          delay: int = 30) -> NoReturn:
    logger.info(f"Scheduling removal of {common_name + suffix} in {delay} seconds if no match found.")
    Timer(delay, cleanup_files, args=[processor, common_name, suffix, False]).start()


def determine_part(file_name: str) -> str:
    return next((suffix for suffix in suffixes if suffix in file_name), "unknown_part")


def get_file_paths(folder_path: str) -> List[str]:
    folder = Path(folder_path)
    return [file for file in folder.iterdir() if file.is_file()]


def get_file_name(event) -> str:
    return os.path.basename(event.src_path) \
        if isinstance(event, FileCreatedEvent) \
        else os.path.basename(event.replace('\\', '/'))


def get_common_name(file_name: str) -> str:
    common_name = file_name.replace(next((suffix for suffix in suffixes if suffix in file_name), ""), "") \
        .replace(".jpg", "") \
        .replace(".txt", "")
    return common_name


fetch = lambda handler, common_name, suffix: (
    handler.sender.send_request(handler.configuration.components.sender["api_url"],
                                handler.configuration.components.processor["folder_path"], common_name),
    cleanup_files(handler.processor, common_name, suffix, True)
)

store = lambda handler, common_name, suffix: (
    handler.database.store(kwargs={"key": common_name,
                                   "expiry": handler.configuration.components.processor["expiry_delay"],
                                   "value": f"{handler.configuration.components.processor['folder_path']}/{common_name}{suffix}"}),
    schedule_file_removal(handler.processor, common_name, suffix,
                          handler.configuration.components.processor['expiry_delay'])
)


def scan_existing_files(handler) -> NoReturn:
    folder_path = handler.configuration.components.processor["folder_path"]

    def is_valid_file(file_name: str) -> bool:
        fpath = os.path.join(folder_path, file_name)
        if os.path.isfile(fpath):
            return True
        else:
            logger.warning(f"File failed filter (not a file): {file_path}")
            return False

    valid_files = filter(is_valid_file, os.listdir(folder_path))

    for valid_file in valid_files:
        file_path = os.path.join(folder_path, valid_file)
        logger.info(f"Processing file: {file_path}")
        handler.processor.strategy_pool.pool.submit(handler.processor.process,
                                                    kwargs={'event_type': None, 'src_path': file_path})


def process_by_existence(handler: Handler, common_name: str, suffix: str) -> NoReturn:
    exists_in_db = handler.database.db_instance.get(common_name)
    if exists_in_db:
        fetch(handler, common_name, suffix)
    else:
        store(handler, common_name, suffix)


