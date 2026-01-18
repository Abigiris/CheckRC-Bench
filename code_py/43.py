def func(x):
    if type(x) == bool:     
        if not isinstance(x, int):
            return "subsumed redundancy"
    return None