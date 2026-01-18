def test_subclass(self):
    a = DatetimeTZDtype.construct_from_string("datetime64[ns, US/Eastern]")
    b = DatetimeTZDtype.construct_from_string("datetime64[ns, CET]")

    assert issubclass(type(a), type(a))
    assert issubclass(type(a), type(b))