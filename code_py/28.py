def test_subclass(self):
    a = IntervalDtype("interval[int64, right]")
    b = IntervalDtype("interval[int64, right]")

    assert issubclass(type(a), type(a))
    assert issubclass(type(a), type(b))