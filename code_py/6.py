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


if __name__ == "__main__":
    path_str = "C:<temp>:file*.txt"
    print(f"Result 1: {sanitize_win_path(path_str)}")