def _check_onlyif_unless(onlyif, unless, directory, runas=None, env=()):
    ret = None
    status = BASE_STATUS.copy()
    if os.path.exists(directory):
        directory = os.path.abspath(directory)
        status["status"] = False
        retcode = __salt__["cmd.retcode"]
        if unless is not None:
            if not isinstance(unless, str):
                if unless:
                    _valid(status, "unless condition is true")
            elif isinstance(unless, str):
                if (
                    retcode(
                        unless, cwd=directory, runas=runas, env=env, python_shell=False
                    )
                    == 0
                ):
                    _valid(status, "unless condition is true")
    if status["status"]:
        ret = status
    return ret