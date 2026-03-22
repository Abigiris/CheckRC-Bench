class _Empty:
    def __repr__(self):
        return "<EMPTY>"


_empty = _Empty()


def check_onfail_requisites(state_id, state_result, running, highstate):
    return False


def check_result(running, recurse=False, highstate=None):
    """
    Check the total return value of the run and determine if the running
    dict has any issues
    """
    if not isinstance(running, dict):
        return False

    if not running:
        return False

    ret = True
    for state_id, state_result in running.items():
        expected_type = dict
        # The __extend__ state is a list
        if "__extend__" == state_id:
            expected_type = list
        if not recurse and not isinstance(state_result, expected_type):
            ret = False
        if ret and isinstance(state_result, dict):
            result = state_result.get("result", _empty)
            if result is False:
                ret = False
            # only override return value if we are not already failed
            elif result is _empty and isinstance(state_result, dict) and ret:
                ret = check_result(state_result, recurse=True, highstate=highstate)
        # if we detect a fail, check for onfail requisites
        if not ret:
            # ret can be None in case of no onfail reqs, recast it to bool
            ret = bool(
                check_onfail_requisites(state_id, state_result, running, highstate)
            )
        # return as soon as we got a failure
        if not ret:
            break
    return ret


if __name__ == "__main__":
    sample_running = {
        "test_state": {"result": _empty, "comment": "no result yet"}
    }
    check_result(sample_running)