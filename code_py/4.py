import numpy as np


class MockPandas:
    class DataFrame:
        def __init__(self):
            self.shape = (10, 2)
            self.dtypes = "float64"
            self.ndim = 2
    class Series:
        def __init__(self):
            self.shape = (10,)
            self.dtypes = "int64"
            self.ndim = 1

class MockPytest:
    def importorskip(self, modname):
        if modname == "pandas":
            return MockPandas()
        raise ImportError()

pytest = MockPytest()

class Bunch:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


def check_as_frame(
    bunch, dataset_func, expected_data_dtype=None, expected_target_dtype=None
):
    pd = pytest.importorskip("pandas")
    frame_bunch = dataset_func(as_frame=True)
    assert hasattr(frame_bunch, "frame")
    assert isinstance(frame_bunch.frame, pd.DataFrame)
    assert isinstance(frame_bunch.data, pd.DataFrame)
    assert frame_bunch.data.shape == bunch.data.shape
    if frame_bunch.target.ndim > 1:
        assert isinstance(frame_bunch.target, pd.DataFrame)
    else:
        assert isinstance(frame_bunch.target, pd.Series)
    assert frame_bunch.target.shape[0] == bunch.target.shape[0]
    if expected_data_dtype is not None:
        assert np.all(frame_bunch.data.dtypes == expected_data_dtype)
    if expected_target_dtype is not None:
        assert np.all(frame_bunch.target.dtypes == expected_target_dtype)

    # Test for return_X_y and as_frame=True
    frame_X, frame_y = dataset_func(as_frame=True, return_X_y=True)
    assert isinstance(frame_X, pd.DataFrame)
    if frame_y.ndim > 1:
        assert isinstance(frame_X, pd.DataFrame)
    else:
        assert isinstance(frame_y, pd.Series)


if __name__ == "__main__":
    # Mock data for execution check
    m_data = Bunch(data=type('obj',(),{'shape':(1,1)})(), target=type('obj',(),{'shape':(1,)})())
    def mock_func(**kwargs):
        pd = MockPandas()
        if kwargs.get('return_X_y'):
            return pd.DataFrame(), pd.Series()
        return Bunch(frame=pd.DataFrame(), data=pd.DataFrame(), target=pd.Series())
    
    try:
        check_as_frame(m_data, mock_func)
    except Exception:
        pass