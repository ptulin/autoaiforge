# Market Data Feed

## Overview

`market_data_feed` is a lightweight Python CLI tool designed to stream and save real-time market data (price, volume, etc.) for selected cryptocurrencies or stocks. This tool is ideal for training AI models or for live trading systems that require up-to-date market data.

## Features

- Stream real-time market data from Binance.
- Save data in either CSV or JSON format.
- Designed for extensibility to support other platforms in the future.

## Requirements

- Python 3.7+
- `ccxt`
- `pandas`
- `websockets`

Install the required dependencies using pip:

```bash
pip install ccxt pandas websockets
```

## Usage

Run the tool using the command line:

```bash
python market_data_feed.py --asset BTC/USDT --platform binance --output data.csv
```

### Arguments

- `--asset`: The trading pair to fetch data for (e.g., BTC/USDT).
- `--platform`: The trading platform (currently only `binance` is supported).
- `--output`: The output file path (e.g., `data.csv` or `data.json`).

## Testing

To run the tests, install `pytest`:

```bash
pip install pytest
```

Then, run the tests:

```bash
pytest test_market_data_feed.py
```

The tests include:

1. Verifying that data is saved correctly in CSV format.
2. Verifying that data is saved correctly in JSON format.
3. Mocking Binance WebSocket data to test the `fetch_binance_data` function without requiring network access.

## Notes

- The tool currently supports only Binance as the trading platform.
- Ensure that the output file has either `.csv` or `.json` extension.
- The tool saves data in batches of 10 trades to the specified output file.

## License

This project is licensed under the MIT License.