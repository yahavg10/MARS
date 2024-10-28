from typing import Dict, Callable

from utils.pool import PoolFactory
from utils.wrapper import wrap_callable


class PipelineExecutor:
    toolbox: Dict[str, Callable]

    def __init__(self, pipeline_executor_fn: Callable, orchestrator):
        self._process_fn = wrap_callable(pipeline_executor_fn, ())
        self.orchestrator = orchestrator
        self.strategy_pool = PoolFactory.create_pool_strategy(
            orchestrator.configuration.components.pipeline_executor["handling_way"],
            orchestrator.configuration.components.pipeline_executor["max_workers"])
        self.toolbox = {}

    def process(self, **kwargs) -> None:
        self._process_fn(self, self.orchestrator, kwargs)
