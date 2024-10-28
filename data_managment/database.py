from typing import Callable, Dict, NoReturn, Any

from utils.wrapper import wrap_callable


class Database:
    toolbox: Dict[str, Callable] = {}

    def __init__(self, database_class, store_fn: Callable, fetch_fn: Callable, delete_fn: Callable,
                 database_class_args) -> NoReturn:
        self.db_instance = database_class(**database_class_args)
        self.store_fn = wrap_callable(store_fn, ())
        self.fetch_fn = wrap_callable(fetch_fn, ())
        self.delete_fn = wrap_callable(delete_fn, ())

    def store(self, **kwargs) -> NoReturn:
        self.store_fn(self.db_instance, kwargs)

    def fetch(self, **kwargs) -> Any:
        self.fetch_fn(self.db_instance, kwargs)

    def delete(self, **kwargs) -> NoReturn:
        self.delete_fn(self.db_instance, kwargs)
