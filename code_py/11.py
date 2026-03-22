import pytest
from unittest.mock import patch


class MockHGFS:
    def __init__(self):
        self.__opts__ = {}
        
    def init(self):
        return [{"repo": "path/to/repo"}]


hgfs = MockHGFS()


@pytest.mark.slow_test
@pytest.mark.skip_on_windows(reason="testing break in windows")
def test_fix_58852(hgfs_setup_and_teardown):
    with patch.dict(
        hgfs.__opts__,
        {
            "hgfs_remotes": [{str(hgfs_setup_and_teardown): [{"base": "default"}]}],
        },
    ):
        repo = hgfs.init()
        assert isinstance(repo, list)
        if isinstance(repo, list):
            for value in repo:
                assert isinstance(value, dict)
                for key, value in value.items():
                    if key != "repo":
                        assert isinstance(value, str)


if __name__ == "__main__":
    test_fix_58852("mock_path")