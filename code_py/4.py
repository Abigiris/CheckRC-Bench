def test_trivial_cv_results_attr():
    # Test search over a "grid" with only one point.
    clf = MockClassifier()
    grid_search = GridSearchCV(clf, {"foo_param": [1]}, cv=2)
    grid_search.fit(X, y)
    assert hasattr(grid_search, "cv_results_")

    random_search = RandomizedSearchCV(clf, {"foo_param": [0]}, n_iter=1, cv=2)
    random_search.fit(X, y)
    assert hasattr(grid_search, "cv_results_")