def func(x):
    if not isinstance(x, int):     
        if type(x) == bool:
            return "subsumed conflict"
    return None