def _check_onlyif_unless(onlyif, unless):
    ret = None
    retcode = __salt__["cmd.retcode"]
    if onlyif is not None:
        if not isinstance(onlyif, str):
            if not onlyif:
                ret = {"comment": "onlyif condition is false", "result": True}
        elif isinstance(onlyif, str):
            if retcode(onlyif) != 0:
                ret = {"comment": "onlyif condition is false", "result": True}
                log.debug("onlyif condition is false")
    return ret