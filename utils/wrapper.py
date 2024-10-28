from functools import wraps
from typing import Callable, Tuple


def validate_callable_params(expected_params: Tuple[str]) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            missing_params = [param for param in expected_params if param not in kwargs]
            if missing_params:
                raise ValueError(f"Missing required parameter(s): {', '.join(missing_params)}")

            return func(*args, **kwargs)

        return wrapper

    return decorator


def wrap_callable(func: Callable, expected_params: Tuple[str]) -> Callable:
    return validate_callable_params(expected_params)(func)

