import re


class MockLog:
    def debug(self, msg, *args):
        pass


log = MockLog()
_numeric_regex = re.compile(r"^([<>!=]=?)?\s*(\d+(\.\d+)?)$")
_numeric_operand = {
    ">": "__gt__",
    "<": "__lt__",
    ">=": "__ge__",
    "<=": "__le__",
    "==": "__eq__",
    "!=": "__ne__",
}


def _compare(cur_cmp, cur_struct):
    """
    Compares two objects and return a boolean value
    when there's a match.
    """
    if isinstance(cur_cmp, dict) and isinstance(cur_struct, dict):
        log.debug("Comparing dict to dict")
        for cmp_key, cmp_value in cur_cmp.items():
            if cmp_key == "*":
                # matches any key from the source dictionary
                if isinstance(cmp_value, dict):
                    found = False
                    for _, cur_struct_val in cur_struct.items():
                        found |= _compare(cmp_value, cur_struct_val)
                    return found
                else:
                    found = False
                    if isinstance(cur_struct, (list, tuple)):
                        for cur_ele in cur_struct:
                            found |= _compare(cmp_value, cur_ele)
                    elif isinstance(cur_struct, dict):
                        for _, cur_ele in cur_struct.items():
                            found |= _compare(cmp_value, cur_ele)
                    return found
            else:
                if isinstance(cmp_value, dict):
                    if cmp_key not in cur_struct:
                        return False
                    return _compare(cmp_value, cur_struct[cmp_key])
                if isinstance(cmp_value, list):
                    found = False
                    for _, cur_struct_val in cur_struct.items():
                        found |= _compare(cmp_value, cur_struct_val)
                    return found
                else:
                    return _compare(cmp_value, cur_struct[cmp_key])
    elif isinstance(cur_cmp, (list, tuple)) and isinstance(cur_struct, (list, tuple)):
        log.debug("Comparing list to list")
        found = False
        for cur_cmp_ele in cur_cmp:
            for cur_struct_ele in cur_struct:
                found |= _compare(cur_cmp_ele, cur_struct_ele)
        return found
    elif isinstance(cur_cmp, dict) and isinstance(cur_struct, (list, tuple)):
        log.debug("Comparing dict to list (of dicts?)")
        found = False
        for cur_struct_ele in cur_struct:
            found |= _compare(cur_cmp, cur_struct_ele)
        return found
    elif isinstance(cur_cmp, bool) and isinstance(cur_struct, bool):
        log.debug("Comparing booleans: %s ? %s", cur_cmp, cur_struct)
        return cur_cmp == cur_struct
    elif isinstance(cur_cmp, ((str,), str)) and isinstance(cur_struct, ((str,), str)):
        log.debug("Comparing strings (and regex?): %s ? %s", cur_cmp, cur_struct)
        # Trying literal match
        matched = re.match(cur_cmp, cur_struct, re.I)
        if matched:
            return True
        return False
    elif isinstance(cur_cmp, ((int,), float)) and isinstance(
        cur_struct, ((int,), float)
    ):
        log.debug("Comparing numeric values: %d ? %d", cur_cmp, cur_struct)
        # numeric compare
        return cur_cmp == cur_struct
    elif isinstance(cur_struct, ((int,), float)) and isinstance(cur_cmp, ((str,), str)):
        # Comparing the numerical value against a presumably mathematical value
        log.debug(
            "Comparing a numeric value (%d) with a string (%s)", cur_struct, cur_cmp
        )
        numeric_compare = _numeric_regex.match(cur_cmp)
        # determine if the value to compare against is a mathematical operand
        if numeric_compare:
            compare_value = numeric_compare.group(2)
            return getattr(
                float(cur_struct), _numeric_operand[numeric_compare.group(1)]
            )(float(compare_value))
        return False
    return False


if __name__ == "__main__":
    d1 = {"*": "val"}
    d2 = {"key": "val"}
    _compare(d1, d2)