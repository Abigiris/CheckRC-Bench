def func(x):
    if type(x) != int: 
        return "ok"
    elif not isinstance(x, bool):
        return "subsumed redundancy"
    return None