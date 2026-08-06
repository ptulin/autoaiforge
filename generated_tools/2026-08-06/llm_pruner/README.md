# LLM Pruner

A tool for pruning Large Language Models (LLMs) to reduce their size while maintaining performance.

## Installation

To install the required packages, run:

```bash
pip install torch transformers
```

## Usage

To prune an LLM model, run:

```bash
python llm_pruner.py --model_path <model_path> --pruning_ratio <pruning_ratio> --output_path <output_path>
```

Replace `<model_path>` with the path to the LLM model file, `<pruning_ratio>` with the desired pruning ratio, and `<output_path>` with the path to save the pruned model.