import torch
import psutil
from transformers import AutoModel, AutoTokenizer

class LazyLoader:
    def __init__(self, model_name: str, memory_limit: int = None):
        """
        Initialize the LazyLoader.

        :param model_name: Hugging Face model name (e.g., 'gpt2').
        :param memory_limit: Memory limit in MB for lazy loading. If None, no limit is enforced.
        """
        self.model_name = model_name
        self.memory_limit = memory_limit
        self.model = None
        self.tokenizer = None

    def _check_memory(self):
        """
        Check if the current memory usage exceeds the specified limit.

        :return: True if memory usage is within the limit, False otherwise.
        """
        if self.memory_limit is None:
            return True

        available_memory = psutil.virtual_memory().available / (1024 * 1024)  # Convert to MB
        return available_memory >= self.memory_limit

    def load(self):
        """
        Load the model and tokenizer lazily based on memory constraints.

        :return: The loaded model and tokenizer.
        """
        if not self._check_memory():
            raise MemoryError(f"Insufficient memory to load the model. Available memory is below the limit of {self.memory_limit} MB.")

        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModel.from_pretrained(self.model_name)
        return self

    def generate(self, input_text: str):
        """
        Perform inference using the lazy-loaded model.

        :param input_text: Input text for the model.
        :return: Model output.
        """
        if self.model is None or self.tokenizer is None:
            raise ValueError("Model and tokenizer must be loaded before inference. Call the `load` method first.")

        inputs = self.tokenizer(input_text, return_tensors="pt")
        with torch.no_grad():
            outputs = self.model(**inputs)
        return outputs

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="LLM Lazy Loader")
    parser.add_argument("model_name", type=str, help="Hugging Face model name (e.g., 'gpt2').")
    parser.add_argument("--memory_limit", type=int, default=None, help="Memory limit in MB for lazy loading.")

    args = parser.parse_args()

    try:
        loader = LazyLoader(args.model_name, args.memory_limit).load()
        print(f"Model '{args.model_name}' loaded successfully.")
    except MemoryError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")