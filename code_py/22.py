@pytest.mark.slow_test
@pytest.mark.skip_on_windows(reason="testing break in windows")
def test_all_branches(hgfs_setup_and_teardown):
    with patch.dict(
        hgfs.__opts__,
        {
            "hgfs_remotes": [{str(hgfs_setup_and_teardown): [{"base": "default"}]}],
        },
    ):
        repos = hgfs.init()
        hgfs.update()
        for repo in repos:
            repo["repo"].open()
            branches = hgfs._all_branches(repo["repo"])
            assert isinstance(branches, list)
            if isinstance(branches, list):
                for value in branches:
                    assert isinstance(value, tuple)
                    assert len(value) == 3
                    assert value[0] in ["default", "test"]
                    assert isinstance(value[1], int)
                    assert isinstance(value[2], str)