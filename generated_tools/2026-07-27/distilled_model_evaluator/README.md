# Distilled Model Evaluator

## Description
Distilled Model Evaluator is a CLI tool designed to evaluate the performance of distilled AI models against their full-sized counterparts. It provides a summary of metrics such as accuracy, latency, and memory usage, helping developers assess the trade-offs made during model distillation.

## Features
- Compare distilled (student) model with original (teacher) model.
- Reports metrics like accuracy, latency, and memory usage.
- Supports evaluation on multiple datasets.
- Outputs tabular performance comparison (console or CSV).

## Installation

Install the required Python packages:

```bash
pip install torch==2.0.1 numpy==1.23.5 pandas==1.5.3 tabulate==0.9.0
```

## Usage

### Example Command

```bash
python distilled_model_evaluator.py --student model_student.pth --teacher model_teacher.pth --data eval_dataset.csv
```

### Save Output to CSV

```bash
python distilled_model_evaluator.py --student model_student.pth --teacher model_teacher.pth --data eval_dataset.csv --output comparison_report.csv
```

## Input
- `--student`: Path to the distilled (student) model file.
- `--teacher`: Path to the original (teacher) model file.
- `--data`: Path to the evaluation dataset (CSV).
- `--output`: Optional path to save the comparison report (CSV).

## Output
- Tabular performance comparison displayed in the console.
- Optional CSV file containing the comparison report.

## License
MIT License