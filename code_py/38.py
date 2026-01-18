def func(x):
    if type(x) != bool: 
        return "ok"
    elif not isinstance(x, int):
        return "subsumed conflict"
    return None