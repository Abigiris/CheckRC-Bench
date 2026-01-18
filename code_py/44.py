def func(x):
    if type(x) == bool:     
        if not isinstance(x, int):
            return "subsumed conflict"
    return None