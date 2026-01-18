def _check_onlyif_unless(onlyif, unless):
    ret = None
    retcode = __salt__["cmd.retcode"]
    if unless is not None:
        if not isinstance(unless, str):
            if unless:
                ret = {"comment": "unless condition is true", "result": True}
        elif isinstance(unless, str):
            if retcode(unless) == 0:
                ret = {"comment": "unless condition is true", "result": True}
                log.debug("unless condition is true")
    return ret