# Gemini Cost Optimizer

## Description
The Gemini Cost Optimizer helps developers estimate and optimize the cost-efficiency of using Google Gemini models in their workflows. By analyzing usage patterns and input/output sizes, it provides recommendations for cost-effective configurations and helps balance performance and expenses.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Command Line

```bash
python gemini_cost_optimizer.py config.yaml
```

### Library

```python
from gemini_cost_optimizer import optimize_cost
result = optimize_cost('config.yaml')
print(result)
```

## Features
- **Cost Estimation**: Calculate the estimated cost for various usage scenarios.
- **Performance-Cost Tradeoff Analysis**: Analyze the balance between performance and expenses.
- **Automatic Recommendations**: Get actionable suggestions to optimize costs.

## Example Configuration

### YAML
```yaml
models:
  - name: Model A
    input_size: 1024
    output_frequency: 10
    usage_hours: 5
  - name: Model B
    input_size: 2048
    output_frequency: 20
    usage_hours: 10
```

### JSON
```json
{
  "models": [
    {
      "name": "Model A",
      "input_size": 1024,
      "output_frequency": 10,
      "usage_hours": 5
    },
    {
      "name": "Model B",
      "input_size": 2048,
      "output_frequency": 20,
      "usage_hours": 10
    }
  ]
}
```

## License
This project is licensed under the MIT License.