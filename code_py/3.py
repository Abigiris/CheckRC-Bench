import numpy as np


class MockClassifier:
    def __init__(self):
        self._estimator_type = "classifier"
        
    def get_params(self, deep=True):
        return {}
    
    def set_params(self, **params):
        return self
    
    def fit(self, X, y):
        return self


class BaseSearch:
    def __init__(self, estimator, param_candidates, cv=None):
        self.estimator = estimator
        self.param_candidates = param_candidates
        self.cv = cv
        self.cv_results_ = {}

    def fit(self, X, y):
        return self


class GridSearchCV(BaseSearch):
    pass


class RandomizedSearchCV(BaseSearch):
    def __init__(self, estimator, param_distributions, n_iter=10, cv=None):
        super().__init__(estimator, param_distributions, cv)
        self.n_iter = n_iter


X = np.array([[1, 2], [3, 4]])
y = np.array([0, 1])


def test_trivial_cv_results_attr():
    # Test search over a "grid" with only one point.
    clf = MockClassifier()
    grid_search = GridSearchCV(clf, {"foo_param": [1]}, cv=2)
    grid_search.fit(X, y)
    assert hasattr(grid_search, "cv_results_")

    random_search = RandomizedSearchCV(clf, {"foo_param": [0]}, n_iter=1, cv=2)
    random_search.fit(X, y)
    assert hasattr(grid_search, "cv_results_")


if __name__ == "__main__":
    test_trivial_cv_results_attr()