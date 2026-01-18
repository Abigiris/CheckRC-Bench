from functools import wraps
from typing import Callable


def wrapper(*args, **kwargs):
    if len(args) > 0:
        if isinstance(args[0], expected_type):
            return (args, kwargs)
        elif not isinstance(args[0], expected_type):  # branch redundancy 
            raise TypeError(f"Expected {expected_type}")
    return (args, kwargs)