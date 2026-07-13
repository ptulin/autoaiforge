# Causal Intervention Simulator

## Overview
The Causal Intervention Simulator is a Python tool that allows developers to simulate interventions on specific components (e.g., neurons, attention heads) in a large language model to observe changes in its behavior. This is useful for understanding the role of individual components in token predictions or model outputs.

## Features
- Load pre-trained language models and tokenizers.
- Simulate interventions on specific components of the model.
- Save the results of the intervention to a CSV file for further analysis.

## Installation
To install the required dependencies, run:

```bash
pip install torch transformers pandas
```

## Usage
Run the tool from the command line:

```bash
python causal_intervention_simulator.py --model <model_path> \
    --sequence "<input_sequence>" \
    --components neuron_45 neuron_46 \
    --output <output_file.csv>
```

### Arguments
- `--model`: Path to the pre-trained model.
- `--sequence`: Input token sequence.
- `--components`: List of components to intervene on (e.g., neuron_45).
- `--output`: Path to save the output CSV file.

## Testing
To run the tests, install `pytest` and execute:

```bash
pip install pytest
pytest test_causal_intervention_simulator.py
```

The tests include:
- Verifying the model and tokenizer loading.
- Simulating interventions on mocked models.
- Saving and verifying results in a CSV file.

## License
This project is licensed under the MIT License.