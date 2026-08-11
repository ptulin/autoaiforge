# LLM Agent Composer

This tool allows developers to compose multiple Large Language Model agents into a single, cohesive system.

## Installation

To install the required packages, run the following command:

```bash
pip install transformers scikit-learn
```

## Usage

To use the LLM Agent Composer, run the following command:

```bash
python llm_agent_composer.py --agents model1.pth model2.pth --composition_config composition_config.json
```

Replace `model1.pth` and `model2.pth` with the paths to your LLM agent models, and `composition_config.json` with the path to your composition config file.

## Composition Config File

The composition config file should be a JSON file with the following structure:

```json
{
    "weights": [0.5, 0.5]
}
```

Replace `[0.5, 0.5]` with the weights for your LLM agent models.
