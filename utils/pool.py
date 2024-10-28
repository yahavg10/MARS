from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from typing import Callable, Any


class PoolStrategy:
    def submit(self, fn: Callable, *args, **kwargs) -> Any:
        raise NotImplementedError("Submit method should be implemented.")

    def shutdown(self, wait: bool = True) -> None:
        raise NotImplementedError("Shutdown method should be implemented.")


class PoolFactory:
    @staticmethod
    def create_pool_strategy(pool_type: str, max_workers: int) -> PoolStrategy:
        if pool_type == "multiprocess":
            return ProcessPoolStrategy(max_workers)
        else:
            return ThreadPoolStrategy(max_workers)


class ThreadPoolStrategy(PoolStrategy):
    def __init__(self, max_workers: int):
        self.pool = ThreadPoolExecutor(max_workers=max_workers)

    def submit(self, fn: Callable, *args, **kwargs) -> Any:
        return self.pool.submit(fn, *args, **kwargs)

    def shutdown(self, wait: bool = True) -> None:
        self.pool.shutdown(wait=wait)


class ProcessPoolStrategy(PoolStrategy):
    def __init__(self, max_workers: int):
        self.pool = ProcessPoolExecutor(max_workers=max_workers)

    def submit(self, fn: Callable, *args, **kwargs) -> Any:
        return self.pool.submit(fn, *args, **kwargs)

    def shutdown(self, wait: bool = True) -> None:
        self.pool.shutdown(wait=wait)
