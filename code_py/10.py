def present(name, cloud_provider, onlyif=None, unless=None, opts=None, **kwargs):
    """
    Spin up a single instance on a cloud provider, using salt-cloud. This state
    does not take a profile argument; rather, it takes the arguments that would
    normally be configured as part of the state.

    Note that while this function does take any configuration argument that
    would normally be used to create an instance, it will not verify the state
    of any of those arguments on an existing instance. Stateful properties of
    an instance should be configured using their own individual state (i.e.,
    cloud.tagged, cloud.untagged, etc).

    name
        The name of the instance to create

    cloud_provider
        The name of the cloud provider to use

    onlyif
        Do run the state only if is unless succeed

    unless
        Do not run the state at least unless succeed

    opts
        Any extra opts that need to be used
    """
    ret = {"name": name, "changes": {}, "result": None, "comment": ""}

    retcode = __salt__["cmd.retcode"]
    if unless is not None:
        if not isinstance(unless, str):
            if unless:
                return _valid(name, comment="unless condition is true")
        elif isinstance(unless, str):
            if retcode(unless, python_shell=True) == 0:
                return _valid(name, comment="unless condition is true")

    # provider=None not cloud_provider because
    # need to ensure ALL providers don't have the instance
    if __salt__["cloud.has_instance"](name=name, provider=None):
        ret["result"] = True
        ret["comment"] = f"Already present instance {name}"
        return ret

    if __opts__["test"]:
        ret["comment"] = f"Instance {name} needs to be created"
        return ret

    info = __salt__["cloud.create"](cloud_provider, name, opts=opts, **kwargs)
    if info and "Error" not in info:
        ret["changes"] = info
        ret["result"] = True
        ret["comment"] = (
            "Created instance {} using provider {} and the following options: {}".format(
                name, cloud_provider, pprint.pformat(kwargs)
            )
        )
    elif info and "Error" in info:
        ret["result"] = False
        ret["comment"] = "Failed to create instance {} using profile {}: {}".format(
            name,
            profile,
            info["Error"],
        )
    else:
        ret["result"] = False
        ret["comment"] = (
            "Failed to create instance {} using profile {}, "
            "please check your configuration".format(name, profile)
        )
    return ret