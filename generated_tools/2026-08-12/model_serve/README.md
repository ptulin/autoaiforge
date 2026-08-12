# AI Model Serving Framework
This framework provides a simple and flexible way to deploy and serve AI models in production environments. It supports various model formats and frameworks, including TensorFlow, PyTorch, and scikit-learn.

## Installation
To install the required packages, run the following command:
```bash
pip install flask tensorflow torch scikit-learn
```

## Usage
To use the framework, run the following command:
```bash
python model_serve.py --model_path <model_path> --framework <framework> --endpoint <endpoint>
```
Replace `<model_path>` with the path to your model file, `<framework>` with the framework type (tensorflow, pytorch, scikit-learn), and `<endpoint>` with the API endpoint.

## Testing
To run the tests, use the following command:
```bash
pytest test_model_serve.py
```