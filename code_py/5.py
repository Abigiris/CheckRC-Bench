import os

BASE_STATUS = {"status": True, "comment": ""}


def _valid(status, comment):
    status["status"] = False
    status["comment"] = comment


def mock_retcode(cmd, cwd=None, runas=None, env=None):
    return 0


__salt__ = {
    "cmd.retcode": mock_retcode
}


def _check_onlyif_unless(onlyif, unless, directory, runas=None, env=()):
    ret = None
    status = BASE_STATUS.copy()
    if os.path.exists(directory):
        directory = os.path.abspath(directory)
        status["status"] = False
        retcode = __salt__["cmd.retcode"]
        if onlyif is not None:
            if not isinstance(onlyif, str):
                if not onlyif:
                    _valid(status, "onlyif condition is false")
            elif isinstance(onlyif, str):
                if retcode(onlyif, cwd=directory, runas=runas, env=env) != 0:
                    _valid(status, "onlyif condition is false")
    if status["status"]:
        ret = status
    return ret


if __name__ == "__main__":
    case_str = _check_onlyif_unless("ls -l", None, None)