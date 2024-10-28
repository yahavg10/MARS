import logging

from config_models.logger_model import LoggerConfig


def setup_custom_logger(logger_config: LoggerConfig) -> logging.Logger:
    formatter = logging.Formatter(fmt=logger_config.fmt, datefmt=logger_config.datefmt)

    init_logger = logging.getLogger(name=logger_config.logger_name)
    init_logger.level = 1
    for handler_info in logger_config.handlers:
        if handler_info['type'] == "StreamHandler":
            handler = create_handler(handler_info['type'])
        else:
            handler = create_handler(handler_info['type'], filename=handler_info['file_path'])
        handler.setFormatter(formatter)
        handler.setLevel(handler_info['level'])
        init_logger.addHandler(handler)
    return init_logger


def create_handler(handler_name: str, **kwargs) -> logging.Handler:
    handler_mapping = {
        "FileHandler": logging.FileHandler,
        "StreamHandler": logging.StreamHandler,
    }

    handler_class = handler_mapping.get(handler_name)
    if handler_class:
        if handler_name == "StreamHandler":
            kwargs.pop("filename", None)
            return handler_class(**kwargs)
        else:
            return handler_class(**kwargs)
    else:
        raise ValueError("Unsupported handler type")
