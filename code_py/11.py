def absent(name, onlyif=None, unless=None):
    """
    Ensure that no instances with the specified names exist.

    CAUTION: This is a destructive state, which will search all
    configured cloud providers for the named instance,
    and destroy it.

    name
        The name of the instance to destroy

    onlyif
        Do run the state only if is unless succeed

    unless
        Do not run the state at least unless succeed

    """
    ret = {"name": name, "changes": {}, "result": None, "comment": ""}
    retcode = __salt__["cmd.retcode"]

    if onlyif is not None:
        if not isinstance(onlyif, str):
            if not onlyif:
                return _valid(name, comment="onlyif condition is false")
        elif isinstance(onlyif, str):
            if retcode(onlyif, python_shell=True) != 0:
                return _valid(name, comment="onlyif condition is false")

    if not __salt__["cloud.has_instance"](name=name, provider=None):
        ret["result"] = True
        ret["comment"] = f"Already absent instance {name}"
        return ret

    if __opts__["test"]:
        ret["comment"] = f"Instance {name} needs to be destroyed"
        return ret

    info = __salt__["cloud.destroy"](name)
    if info and "Error" not in info:
        ret["changes"] = info
        ret["result"] = True
        ret["comment"] = f"Destroyed instance {name}"
    elif "Error" in info:
        ret["result"] = False
        ret["comment"] = "Failed to destroy instance {}: {}".format(
            name,
            info["Error"],
        )
    else:
        ret["result"] = False
        ret["comment"] = f"Failed to destroy instance {name}"
    return ret