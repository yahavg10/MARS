from typing import Dict, Callable

from utils.pool import PoolFactory
from utils.wrapper import wrap_callable


class Processor:
    toolbox: Dict[str, Callable]

    def __init__(self, process_fn: Callable, handler):
        self._process_fn = wrap_callable(process_fn, ())
        self._handler = handler
        self.strategy_pool = PoolFactory.create_pool_strategy(
            handler.configuration.components.processor["handling_way"],
            handler.configuration.components.processor["max_workers"])
        self.toolbox = {}

    def process(self, **kwargs) -> None:
        self._process_fn(self, self._handler, kwargs)
