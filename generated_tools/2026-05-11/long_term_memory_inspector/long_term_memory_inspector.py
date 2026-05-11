import pandas as pd
import numpy as np
from textwrap import shorten

class MemoryInspector:
    """
    A class to inspect and manage long-term memory data structures.
    
    Attributes:
        memory_data (list or dict): The memory data to be inspected.
    """

    def __init__(self, memory_data):
        if not isinstance(memory_data, (list, dict)):
            raise ValueError("Memory data must be a list or a dictionary.")
        self.memory_data = memory_data

    def query(self, keyword):
        """
        Query memory entries containing a specific keyword.

        Args:
            keyword (str): The keyword to search for.

        Returns:
            list: A list of memory entries containing the keyword.
        """
        if not isinstance(keyword, str):
            raise ValueError("Keyword must be a string.")

        if isinstance(self.memory_data, list):
            return [entry for entry in self.memory_data if keyword.lower() in str(entry).lower()]
        elif isinstance(self.memory_data, dict):
            return {key: value for key, value in self.memory_data.items() if keyword.lower() in str(value).lower()}

    def prune(self, condition):
        """
        Prune memory entries based on a condition.

        Args:
            condition (callable): A function that takes a memory entry and returns True if it should be pruned.

        Returns:
            list or dict: The pruned memory data.
        """
        if not callable(condition):
            raise ValueError("Condition must be a callable function.")

        if isinstance(self.memory_data, list):
            self.memory_data = [entry for entry in self.memory_data if not condition(entry)]
        elif isinstance(self.memory_data, dict):
            self.memory_data = {key: value for key, value in self.memory_data.items() if not condition(value)}
        return self.memory_data

    def summarize(self, width=80):
        """
        Summarize the memory data for quick inspection.

        Args:
            width (int): The maximum width of the summary string.

        Returns:
            str: A summarized string representation of the memory data.
        """
        if isinstance(self.memory_data, list):
            summary = ", ".join(map(str, self.memory_data))
        elif isinstance(self.memory_data, dict):
            summary = ", ".join(f"{key}: {value}" for key, value in self.memory_data.items())
        else:
            summary = "Unsupported memory data format."

        return shorten(summary, width=width, placeholder="...")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Long-Term Memory Inspector")
    parser.add_argument("--query", type=str, help="Keyword to query memory entries.")
    parser.add_argument("--prune", type=str, help="Condition to prune memory entries (Python expression).")
    parser.add_argument("--summarize", action="store_true", help="Summarize memory contents.")
    parser.add_argument("--width", type=int, default=80, help="Width for summary output.")

    args = parser.parse_args()

    # Example memory data
    memory_data = [
        "Learned about pandas library.",
        "Attended a meeting on AI ethics.",
        "Read a paper on reinforcement learning.",
        "Discussed project goals with the team."
    ]

    inspector = MemoryInspector(memory_data)

    if args.query:
        print("Query Results:", inspector.query(args.query))

    if args.prune:
        condition = eval(f"lambda x: {args.prune}")
        inspector.prune(condition)
        print("Pruned Memory:", inspector.memory_data)

    if args.summarize:
        print("Memory Summary:", inspector.summarize(width=args.width))