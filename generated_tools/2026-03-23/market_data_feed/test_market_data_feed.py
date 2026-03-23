import pytest
from unittest.mock import AsyncMock, patch
import json
import pandas as pd
from market_data_feed import save_data, fetch_binance_data

@pytest.fixture
def sample_trade_data():
    return [
        {'timestamp': '2023-01-01T00:00:00', 'price': 20000.0, 'quantity': 0.5},
        {'timestamp': '2023-01-01T00:01:00', 'price': 20010.0, 'quantity': 0.3}
    ]

def test_save_data_csv(sample_trade_data, tmp_path):
    output_file = tmp_path / "output.csv"
    save_data(sample_trade_data, output_file, 'csv')
    assert output_file.exists()
    df = pd.read_csv(output_file)
    assert len(df) == len(sample_trade_data)
    assert df.iloc[0]['price'] == sample_trade_data[0]['price']
    assert df.iloc[1]['quantity'] == sample_trade_data[1]['quantity']

def test_save_data_json(sample_trade_data, tmp_path):
    output_file = tmp_path / "output.json"
    save_data(sample_trade_data, output_file, 'json')
    assert output_file.exists()
    with open(output_file) as f:
        data = json.load(f)
    assert data == sample_trade_data

@pytest.mark.asyncio
@patch('websockets.connect', new_callable=AsyncMock)
async def test_fetch_binance_data(mock_websocket, tmp_path):
    mock_websocket.return_value.__aenter__.return_value.recv = AsyncMock(
        side_effect=[
            json.dumps({"T": 1672531200000, "p": "20000.0", "q": "0.5"}),
            json.dumps({"T": 1672531260000, "p": "20010.0", "q": "0.3"}),
            json.dumps({"T": 1672531320000, "p": "20020.0", "q": "0.2"}),
            Exception("WebSocket closed")
        ]
    )

    output_file = tmp_path / "output.json"
    await fetch_binance_data("btcusdt", output_file, 'json')

    assert output_file.exists()
    with open(output_file) as f:
        data = json.load(f)
    assert len(data) == 3
    assert data[0]['price'] == 20000.0
    assert data[1]['quantity'] == 0.3
