def func(x):
    if type(x) != int: 
        return "ok"
    elif isinstance(x, bool):
        return "subsumed conflict"
    return None