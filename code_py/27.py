def test_subclass(self):
    a = PeriodDtype("period[D]")
    b = PeriodDtype("period[3D]")

    assert issubclass(type(a), type(a))
    assert issubclass(type(a), type(b))