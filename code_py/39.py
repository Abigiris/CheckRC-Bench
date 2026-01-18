def func(x):
    if isinstance(x, int): 
        return "ok"
    elif type(x) == bool:
        return "subsumed conflict"
    return None