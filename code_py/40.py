def func(x):
    if not isinstance(x, bool): 
        return "ok"
    elif type(x) == int:
        return "subsumed conflict"
    return None