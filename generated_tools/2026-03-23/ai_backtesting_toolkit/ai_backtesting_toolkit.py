import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from typing import Callable, Dict

def backtest(strategy: Callable[[pd.DataFrame], pd.DataFrame], data_path: str) -> Dict[str, float]:
    """
    Backtest a trading strategy using historical market data.

    Args:
        strategy (Callable[[pd.DataFrame], pd.DataFrame]): A function implementing the trading strategy.
        data_path (str): Path to the CSV file containing historical market data.

    Returns:
        Dict[str, float]: A dictionary containing performance metrics.
    """
    try:
        # Load historical market data
        data = pd.read_csv(data_path)
        if data.empty:
            raise ValueError("The input CSV file is empty.")

        # Ensure required columns exist
        required_columns = {"date", "price"}
        if not required_columns.issubset(data.columns):
            raise ValueError(f"CSV file must contain columns: {', '.join(required_columns)}")

        # Apply the trading strategy
        trades = strategy(data)
        if "action" not in trades.columns or "price" not in trades.columns:
            raise ValueError("The strategy must return a DataFrame with 'action' and 'price' columns.")

        # Calculate performance metrics
        initial_balance = 10000
        balance = initial_balance
        positions = 0
        for _, row in trades.iterrows():
            if row["action"] == "buy":
                positions += balance / row["price"]
                balance = 0
            elif row["action"] == "sell":
                balance += positions * row["price"]
                positions = 0

        final_balance = balance + (positions * trades.iloc[-1]["price"])
        roi = (final_balance - initial_balance) / initial_balance
        sharpe_ratio = np.mean(trades["price"]) / np.std(trades["price"]) if len(trades) > 1 else 0

        # Generate visualization
        plt.figure(figsize=(10, 6))
        plt.plot(data["date"], data["price"], label="Market Price")
        buy_signals = trades[trades["action"] == "buy"]
        sell_signals = trades[trades["action"] == "sell"]
        plt.scatter(buy_signals["date"], buy_signals["price"], color="green", label="Buy", marker="^")
        plt.scatter(sell_signals["date"], sell_signals["price"], color="red", label="Sell", marker="v")
        plt.legend()
        plt.title("Trading Strategy Backtest")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.grid()
        plt.savefig("backtest_results.png")

        return {
            "ROI": roi,
            "Sharpe Ratio": sharpe_ratio,
            "Final Balance": final_balance
        }

    except FileNotFoundError:
        raise FileNotFoundError("The specified data file was not found.")
    except ValueError as ve:
        raise ve
    except Exception as e:
        raise RuntimeError(f"An error occurred during backtesting: {e}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="AI Backtesting Toolkit")
    parser.add_argument("strategy_module", type=str, help="Path to the Python module containing the strategy function.")
    parser.add_argument("data_path", type=str, help="Path to the CSV file containing historical market data.")

    args = parser.parse_args()

    try:
        # Dynamically import the strategy module
        import importlib.util
        spec = importlib.util.spec_from_file_location("strategy_module", args.strategy_module)
        strategy_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(strategy_module)

        # Ensure the strategy function exists
        if not hasattr(strategy_module, "strategy"):
            raise ValueError("The specified module does not contain a 'strategy' function.")

        # Run backtest
        metrics = backtest(strategy_module.strategy, args.data_path)
        print("Backtest Results:")
        for key, value in metrics.items():
            print(f"{key}: {value}")

    except Exception as e:
        print(f"Error: {e}")