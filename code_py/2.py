import warnings


class ScrapyDeprecationWarning(Warning):
    pass


class NewName:
    pass


def create_deprecated_class(name, new_class):
    class Deprecated(new_class):
        pass
    Deprecated.__name__ = name
    return Deprecated


class TestCase:
    def assertRaises(self, exc_type, func, *args, **kwargs):
        try:
            func(*args, **kwargs)
        except exc_type:
            return
        raise AssertionError(f"{exc_type.__name__} not raised")


class TestScrapy(TestCase):
    def __init__(self):
        pass

    def test_issubclass(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", ScrapyDeprecationWarning)
            DeprecatedName = create_deprecated_class("DeprecatedName", NewName)

            class UpdatedUserClass1(NewName):
                pass

            class UpdatedUserClass1a(NewName):
                pass

            class OutdatedUserClass1(DeprecatedName):
                pass

            class OutdatedUserClass1a(DeprecatedName):
                pass

            class UnrelatedClass:
                pass

            class OldStyleClass:
                pass

        assert not issubclass(UnrelatedClass, DeprecatedName)
        assert not issubclass(OldStyleClass, DeprecatedName)
        assert not issubclass(OldStyleClass, DeprecatedName)
        assert not issubclass(OutdatedUserClass1, OutdatedUserClass1a)
        assert not issubclass(OutdatedUserClass1a, OutdatedUserClass1)

        self.assertRaises(TypeError, issubclass, object(), DeprecatedName)


if __name__ == "__main__":
    t = TestScrapy()
    t.test_issubclass()