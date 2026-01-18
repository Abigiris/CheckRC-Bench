@pytest.mark.slow_test
@pytest.mark.skip_on_windows(reason="testing break in windows")
def test_all_tags(hgfs_setup_and_teardown):
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
            tags = hgfs._all_tags(repo["repo"])
            assert isinstance(tags, list)
            if isinstance(tags, list):
                for value in tags:
                    assert isinstance(value, tuple)
                    assert len(value) == 4
                    assert value[0] in ["test"]
                    assert value[0] not in ["tip"]
                    assert value[1] == 0
                    assert isinstance(value[2], str)
                    assert value[3] is False