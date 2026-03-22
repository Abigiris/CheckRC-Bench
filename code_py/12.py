class IntervalDtype:
    def __init__(self, subtype):
        self.subtype = subtype
    
    def __repr__(self):
        return f"interval[{self.subtype}]"


class TestSubclass:
    def __init__(self):
        pass

    def test_subclass(self):
        a = IntervalDtype("interval[int64, right]")
        b = IntervalDtype("interval[int64, right]")

        assert issubclass(type(a), type(a))


if __name__ == "__main__":
    t = TestSubclass()
    t.test_subclass()