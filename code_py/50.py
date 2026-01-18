def func(x):
    if not isinstance(x, bool): 
        return "ok"
    elif type(x) != int:
        return "subsumed redundancy"
    return None