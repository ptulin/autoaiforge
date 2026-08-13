# Adversarial Example Generator
This tool generates adversarial examples for AI models, which can be used to test and improve the model's robustness to attacks.

## Installation
To install the required packages, run the following command:
```bash
pip install torch
```

## Usage
To use the tool, run the following command:
```bash
python adversarial_example_generator.py --model model.pt --input input.csv --attack pgd
```

## Tests
To run the tests, use the following command:
```bash
pytest test_adversarial_example_generator.py
```