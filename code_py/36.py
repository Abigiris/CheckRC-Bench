def func(x):
    if type(x) != bool: 
        return "ok"
    elif isinstance(x, int):
        return "subsumed redundancy"
    return None