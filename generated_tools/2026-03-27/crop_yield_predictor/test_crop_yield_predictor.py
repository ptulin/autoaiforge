import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock
from io import StringIO
from crop_yield_predictor import preprocess_data, train_model, predict_and_save

def test_preprocess_data():
    mock_csv = "soil_quality,temperature,rainfall,historical_yield\n1.2,25,100,200\n0.8,22,90,180"
    with patch("pandas.read_csv", return_value=pd.read_csv(StringIO(mock_csv))):
        X, y, scaler = preprocess_data("mock.csv")
        assert X.shape == (2, 3)
        assert len(y) == 2
        assert np.allclose(y, [200, 180])

def test_train_model():
    X = np.array([[1.2, 25, 100], [0.8, 22, 90]])
    y = np.array([200, 180])
    model = train_model(X, y, 'random_forest', n_estimators=10)
    assert hasattr(model, "predict")
    predictions = model.predict(X)
    assert len(predictions) == len(y)

def test_predict_and_save():
    mock_csv = "soil_quality,temperature,rainfall,historical_yield\n1.2,25,100,200\n0.8,22,90,180"
    with patch("pandas.read_csv", return_value=pd.read_csv(StringIO(mock_csv))):
        mock_model = MagicMock()
        mock_model.predict.return_value = [210, 190]
        mock_scaler = MagicMock()
        mock_scaler.transform.return_value = np.array([[1.2, 25, 100], [0.8, 22, 90]])

        with patch("pandas.DataFrame.to_csv") as mock_to_csv:
            predict_and_save(mock_model, mock_scaler, "mock.csv", "output.csv")
            mock_to_csv.assert_called_once()
            args, kwargs = mock_to_csv.call_args
            assert kwargs["index"] is False
            assert "output.csv" in args
