# matrix_solver_ai

## Overview

`matrix_solver_ai` is a Python tool designed to solve complex matrix computations such as eigenvalue decomposition, matrix inversion, and solving linear systems. It integrates standard numerical libraries with AI models (using PyTorch) to handle ill-conditioned matrices or provide approximate solutions when exact solutions are not feasible.

## Features

- Eigenvalue decomposition
- Matrix inversion
- Solving linear systems (Ax = b)
- AI-assisted fallback for ill-conditioned matrices

## Installation

To use this tool, you need to have Python installed along with the following dependencies:

- `numpy`
- `scipy`
- `torch`

You can install the required dependencies using pip:

```bash
pip install numpy scipy torch
```

## Usage

Run the tool from the command line with the following options:

```bash
python matrix_solver_ai.py --file <path_to_matrix_file> --operation <operation> [--b <path_to_b_vector>] [--output <output_format>]
```

### Arguments

- `--file`: Path to the input matrix file (CSV or JSON).
- `--operation`: The matrix operation to perform. Options are:
  - `eigen`: Perform eigenvalue decomposition.
  - `inverse`: Compute the inverse of the matrix.
  - `solve`: Solve a linear system Ax = b (requires `--b` argument).
- `--b`: Path to the vector `b` (required if `--operation` is `solve`).
- `--output`: Output format. Options are `json` (default) or `text`.

### Example

#### Eigenvalue Decomposition

```bash
python matrix_solver_ai.py --file matrix.json --operation eigen --output json
```

#### Matrix Inversion

```bash
python matrix_solver_ai.py --file matrix.csv --operation inverse --output text
```

#### Solving a Linear System

```bash
python matrix_solver_ai.py --file matrix.json --operation solve --b vector.json --output json
```

## Testing

To run the tests, install `pytest`:

```bash
pip install pytest
```

Then run:

```bash
pytest test_matrix_solver_ai.py
```

The tests include cases for loading matrices from files, performing eigenvalue decomposition, matrix inversion, solving linear systems, and handling ill-conditioned matrices using AI techniques.

## License

This project is licensed under the MIT License.
