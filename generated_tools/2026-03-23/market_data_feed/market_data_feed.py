import argparse
import asyncio
import ccxt
import pandas as pd
import websockets
import json
import os
from datetime import datetime

def save_data(data, output_file, output_format):
    if output_format == 'csv':
        df = pd.DataFrame(data)
        df.to_csv(output_file, index=False)
    elif output_format == 'json':
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=4)
    else:
        raise ValueError("Unsupported output format. Use 'csv' or 'json'.")

async def fetch_binance_data(asset, output_file, output_format):
    url = f'wss://stream.binance.com:9443/ws/{asset.lower()}@trade'
    data = []
    try:
        async with websockets.connect(url) as websocket:
            print(f"Connected to Binance WebSocket for {asset}.")
            while True:
                response = await websocket.recv()
                trade = json.loads(response)
                trade_data = {
                    'timestamp': datetime.fromtimestamp(trade['T'] / 1000).isoformat(),
                    'price': float(trade['p']),
                    'quantity': float(trade['q'])
                }
                data.append(trade_data)
                print(trade_data)
                if len(data) >= 10:  # Save every 10 trades
                    save_data(data, output_file, output_format)
                    data = []
    except Exception as e:
        print(f"Error: {e}")

async def main():
    parser = argparse.ArgumentParser(description="Real-Time Market Data Feed")
    parser.add_argument('--asset', required=True, help="Asset pair (e.g., BTC/USD).")
    parser.add_argument('--platform', required=True, choices=['binance'], help="Trading platform (currently only 'binance' is supported).")
    parser.add_argument('--output', required=True, help="Output file path (e.g., data.csv or data.json).")
    args = parser.parse_args()

    asset = args.asset.replace('/', '').lower()
    output_file = args.output
    output_format = 'csv' if output_file.endswith('.csv') else 'json' if output_file.endswith('.json') else None

    if not output_format:
        print("Error: Output file must have .csv or .json extension.")
        return

    if args.platform == 'binance':
        await fetch_binance_data(asset, output_file, output_format)
    else:
        print("Error: Unsupported platform.")

if __name__ == "__main__":
    asyncio.run(main())