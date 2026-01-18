@pytest.mark.slow_test
@pytest.mark.skip_on_windows(reason="testing break in windows")
def test_all_bookmarks(hgfs_setup_and_teardown):
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
            bookmarks = hgfs._all_bookmarks(repo["repo"])
            assert isinstance(bookmarks, list)
            if isinstance(bookmarks, list):
                for value in bookmarks:
                    assert isinstance(value, tuple)
                    assert len(value) == 3
                    assert value[0] in ["bookmark_test"]
                    assert value[1] == 2
                    assert isinstance(value[2], str)