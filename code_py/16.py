def sanitize_win_path(winpath):
    """
    Remove illegal path characters for windows
    """
    intab = "<>:|?*"
    if isinstance(winpath, str):
        winpath = winpath.translate({ord(c): "_" for c in intab})
    elif isinstance(winpath, str):
        outtab = "_" * len(intab)
        trantab = "".maketrans(intab, outtab)
        winpath = winpath.translate(trantab)
    return winpath