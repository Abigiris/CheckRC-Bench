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