import os
import numpy as np
from transformers import AutoModel

def split_model(model, max_memory):
    """
    Splits a large language model into smaller sub-models based on memory constraints.

    Args:
        model (transformers.PreTrainedModel): The large language model to split.
        max_memory (int): Maximum memory (in MB) allowed for each sub-model.

    Returns:
        list: A list of dictionaries containing sub-model weights and metadata.
    """
    if not isinstance(max_memory, int) or max_memory <= 0:
        raise ValueError("max_memory must be a positive integer.")

    # Extract model weights
    model_weights = model.state_dict()
    total_memory = sum([param.size * param.itemsize for param in model_weights.values()]) / (1024 ** 2)

    if total_memory <= max_memory:
        return [{"weights": model_weights, "metadata": {"part": 1}}]

    sub_models = []
    current_memory = 0
    sub_model_weights = {}
    part = 1

    for name, param in model_weights.items():
        param_memory = param.size * param.itemsize / (1024 ** 2)

        if current_memory + param_memory > max_memory:
            sub_models.append({"weights": sub_model_weights, "metadata": {"part": part}})
            sub_model_weights = {}
            current_memory = 0
            part += 1

        sub_model_weights[name] = param
        current_memory += param_memory

    if sub_model_weights:
        sub_models.append({"weights": sub_model_weights, "metadata": {"part": part}})

    return sub_models

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Micro LLM Splitter: Split large language models into smaller sub-models.")
    parser.add_argument("--model_name", type=str, required=True, help="Hugging Face model name.")
    parser.add_argument("--max_memory", type=int, required=True, help="Maximum memory (in MB) per sub-model.")
    parser.add_argument("--output_dir", type=str, required=True, help="Directory to save sub-models.")

    args = parser.parse_args()

    model = AutoModel.from_pretrained(args.model_name)
    sub_models = split_model(model, args.max_memory)

    os.makedirs(args.output_dir, exist_ok=True)

    for sub_model in sub_models:
        part = sub_model["metadata"]["part"]
        weights_file = os.path.join(args.output_dir, f"sub_model_part_{part}.npy")
        np.save(weights_file, sub_model["weights"])

    print(f"Split model into {len(sub_models)} parts and saved to {args.output_dir}.")