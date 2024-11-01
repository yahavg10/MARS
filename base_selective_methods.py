import inspect
from typing import NoReturn

import redis

from PipelineExecutor import toolbox
from orchestrator.orchestrator import Orchestrator

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

pipeline_fn = lambda self, proc_orchestrator, kwargs: \
    self.toolbox["process_by_existence"](
        proc_orchestrator,
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
def setup_toolbox(orchestrator: Orchestrator) -> NoReturn:
    for name, func in inspect.getmembers(toolbox, inspect.isfunction):
        orchestrator.pipeline_executor.toolbox.setdefault(name, func)
