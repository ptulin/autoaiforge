import torch
import tensorflow as tf
import psutil
import logging
from typing import Any, Union
import time

def profile_memory(model: Union[torch.nn.Module, tf.Module], input_data: Any, log_file: str = None):
    """
    Profiles the memory usage of a given model during inference.

    Args:
        model (torch.nn.Module or tf.Module): The model to profile.
        input_data (Any): The input data for the model.
        log_file (str, optional): Path to a file where logs will be saved. Defaults to None.

    Returns:
        dict: A dictionary containing memory usage metrics.
    """
    # Configure logging
    logger = logging.getLogger("LLM_Memory_Profiler")
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(log_file) if log_file else logging.StreamHandler()
    handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(handler)

    # Check if the model is PyTorch or TensorFlow
    is_torch_model = isinstance(model, torch.nn.Module)
    is_tf_model = isinstance(model, tf.Module)

    if not (is_torch_model or is_tf_model):
        raise ValueError("Model must be a PyTorch or TensorFlow model.")

    # Start profiling
    logger.info("Starting memory profiling...")
    process = psutil.Process()
    initial_memory = process.memory_info().rss
    logger.info(f"Initial memory usage: {initial_memory / (1024 ** 2):.2f} MB")

    peak_memory = initial_memory

    try:
        if is_torch_model:
            with torch.no_grad():
                torch.cuda.empty_cache()
                start_time = time.time()
                output = model(input_data)
                end_time = time.time()
                peak_memory = max(peak_memory, process.memory_info().rss)

        elif is_tf_model:
            start_time = time.time()
            output = model(input_data)
            end_time = time.time()
            peak_memory = max(peak_memory, process.memory_info().rss)

        logger.info(f"Peak memory usage: {peak_memory / (1024 ** 2):.2f} MB")
        logger.info(f"Inference time: {end_time - start_time:.2f} seconds")

    except Exception as e:
        logger.error(f"Error during profiling: {e}")
        raise

    finally:
        logger.info("Memory profiling completed.")

    return {
        "initial_memory_mb": initial_memory / (1024 ** 2),
        "peak_memory_mb": peak_memory / (1024 ** 2),
        "inference_time_s": end_time - start_time
    }

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="LLM Memory Profiler")
    parser.add_argument("--model_path", type=str, required=True, help="Path to the model file.")
    parser.add_argument("--framework", type=str, choices=["torch", "tensorflow"], required=True, help="Framework of the model (torch or tensorflow).")
    parser.add_argument("--log_file", type=str, default=None, help="Path to save the log file.")
    args = parser.parse_args()

    # Load the model
    if args.framework == "torch":
        model = torch.load(args.model_path)
    elif args.framework == "tensorflow":
        model = tf.keras.models.load_model(args.model_path)

    # Dummy input data
    input_data = torch.randn(1, 3, 224, 224) if args.framework == "torch" else tf.random.normal([1, 224, 224, 3])

    # Profile memory
    profile_memory(model, input_data, args.log_file)