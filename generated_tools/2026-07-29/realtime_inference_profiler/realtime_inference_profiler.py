import asyncio
import time
import numpy as np
import pandas as pd
from typing import Callable, Dict, Any

def generate_workload(workload: str, rate: int, duration: int) -> asyncio.Queue:
    """
    Generate a workload queue based on the specified pattern.

    Args:
        workload (str): The workload pattern ('steady' or 'bursty').
        rate (int): Requests per second.
        duration (int): Duration of the workload in seconds.

    Returns:
        asyncio.Queue: A queue with timestamps for requests.
    """
    queue = asyncio.Queue()
    if workload == 'steady':
        interval = 1 / rate
        for i in range(rate * duration):
            queue.put_nowait(time.time() + i * interval)
    elif workload == 'bursty':
        for i in range(duration):
            burst_size = np.random.poisson(rate)
            for _ in range(burst_size):
                queue.put_nowait(time.time() + i)
    else:
        raise ValueError("Unsupported workload type. Use 'steady' or 'bursty'.")
    return queue

async def worker(queue: asyncio.Queue, model: Callable, results: list):
    """
    Process requests from the queue and record performance metrics.

    Args:
        queue (asyncio.Queue): The workload queue.
        model (Callable): The inference function to profile.
        results (list): A list to store the results.
    """
    while not queue.empty():
        request_time = await queue.get()
        await asyncio.sleep(max(0, request_time - time.time()))
        start_time = time.time()
        try:
            model()  # Call the model function
        except Exception as e:
            results.append({'error': str(e)})
            continue
        end_time = time.time()
        results.append({'latency': end_time - start_time, 'timestamp': start_time})

async def profile_async(model: Callable, workload: str, rate: int, duration: int, workers: int) -> pd.DataFrame:
    """
    Profile the performance of a model under a specific workload.

    Args:
        model (Callable): The inference function to profile.
        workload (str): The workload pattern ('steady' or 'bursty').
        rate (int): Requests per second.
        duration (int): Duration of the workload in seconds.
        workers (int): Number of concurrent workers.

    Returns:
        pd.DataFrame: Performance metrics.
    """
    queue = generate_workload(workload, rate, duration)
    results = []
    tasks = [worker(queue, model, results) for _ in range(workers)]
    await asyncio.gather(*tasks)
    return pd.DataFrame(results)

def profile(model: Callable, workload: str, rate: int, duration: int = 10, workers: int = 1, output_format: str = 'json') -> Any:
    """
    Profile the performance of a model and return metrics.

    Args:
        model (Callable): The inference function to profile.
        workload (str): The workload pattern ('steady' or 'bursty').
        rate (int): Requests per second.
        duration (int): Duration of the workload in seconds.
        workers (int): Number of concurrent workers.
        output_format (str): Output format ('json' or 'csv').

    Returns:
        Any: Performance metrics in the specified format.
    """
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    metrics = loop.run_until_complete(profile_async(model, workload, rate, duration, workers))
    loop.close()
    if output_format == 'json':
        return metrics.to_dict(orient='records')
    elif output_format == 'csv':
        return metrics.to_csv(index=False)
    else:
        raise ValueError("Unsupported output format. Use 'json' or 'csv'.")

if __name__ == "__main__":
    import argparse

    def dummy_model():
        """A dummy model for testing."""
        time.sleep(0.01)

    parser = argparse.ArgumentParser(description="Real-Time Inference Profiler")
    parser.add_argument('--workload', type=str, required=True, choices=['steady', 'bursty'], help="Workload pattern")
    parser.add_argument('--rate', type=int, required=True, help="Requests per second")
    parser.add_argument('--duration', type=int, default=10, help="Duration of the workload in seconds")
    parser.add_argument('--workers', type=int, default=1, help="Number of concurrent workers")
    parser.add_argument('--output-format', type=str, default='json', choices=['json', 'csv'], help="Output format")

    args = parser.parse_args()

    metrics = profile(dummy_model, args.workload, args.rate, args.duration, args.workers, args.output_format)
    if args.output_format == 'json':
        print(metrics)
    else:
        print(metrics)