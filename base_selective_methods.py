import inspect
from typing import NoReturn

import redis

from handling.handler import Handler
from processoring import toolbox

###################################################################################################
###################################################################################################
#                                    DATABASE FUNCTIONS                                           #
###################################################################################################
###################################################################################################
database_store_function = lambda db_instance, kwargs: db_instance.setex(kwargs["kwargs"]["key"],
                                                                        kwargs["kwargs"]["expiry"],
                                                                        kwargs["kwargs"]["value"])
database_fetch_function = lambda db_instance, kwargs: db_instance.get(kwargs["key"])
database_delete_function = lambda db_instance, kwargs: db_instance.delete(kwargs["kwargs"]["key"])
database_class = redis.Redis

###################################################################################################
###################################################################################################
#                                    PROCESSOR FUNCTIONS                                          #
###################################################################################################
###################################################################################################

process_handler_function = lambda self, proc_handler, kwargs: \
    self.toolbox["process_by_existence"](
        proc_handler,
        self.toolbox["get_common_name"](self.toolbox["get_file_name"](kwargs["kwargs"]["src_path"])),
        self.toolbox["determine_part"](self.toolbox["get_file_name"](kwargs["kwargs"]["src_path"]))
    )

###################################################################################################
###################################################################################################
#                                    SENDER FUNCTIONS                                             #
###################################################################################################
###################################################################################################
file_sender_function = lambda folder_path, common_name, suffixes, file_read_mode: [
    ('files', open(f"{folder_path}/{common_name}{suffix}", file_read_mode))
    for suffix in suffixes
]


###################################################################################################
###################################################################################################
#                                    TOOLBOX INITIAL SETUP                                        #
###################################################################################################
###################################################################################################
def setup_toolbox(handler: Handler) -> NoReturn:
    for name, func in inspect.getmembers(toolbox, inspect.isfunction):
        handler.processor.toolbox.setdefault(name, func)
