import argparse
import json
import numpy as np
import torch
from scipy.linalg import eig, inv, solve

def load_matrix_from_file(file_path):
    """Load a matrix from a CSV or JSON file."""
    try:
        if file_path.endswith('.csv'):
            with open(file_path, 'r') as f:
                return np.loadtxt(f, delimiter=',')
        elif file_path.endswith('.json'):
            with open(file_path, 'r') as f:
                data = json.load(f)
                return np.array(data)
        else:
            raise ValueError("Unsupported file format. Use CSV or JSON.")
    except Exception as e:
        raise ValueError(f"Error loading matrix: {e}")

def eigen_decomposition(matrix):
    """Perform eigenvalue decomposition."""
    try:
        values, vectors = eig(matrix)
        return {
            "eigenvalues": values.tolist(),
            "eigenvectors": vectors.tolist()
        }
    except Exception as e:
        raise ValueError(f"Eigen decomposition failed: {e}")

def matrix_inversion(matrix):
    """Compute the inverse of a matrix."""
    try:
        inverse = inv(matrix)
        return {
            "inverse": inverse.tolist()
        }
    except Exception as e:
        raise ValueError(f"Matrix inversion failed: {e}")

def solve_linear_system(matrix, b):
    """Solve a linear system Ax = b."""
    try:
        solution = solve(matrix, b)
        return {
            "solution": solution.tolist()
        }
    except Exception as e:
        raise ValueError(f"Solving linear system failed: {e}")

def handle_ill_conditioned(matrix, operation, b=None):
    """Handle ill-conditioned matrices using AI (Torch)."""
    try:
        tensor_matrix = torch.tensor(matrix, dtype=torch.float32)
        if operation == 'inverse':
            inverse = torch.linalg.pinv(tensor_matrix).numpy()
            return {
                "approx_inverse": inverse.tolist()
            }
        elif operation == 'solve' and b is not None:
            tensor_b = torch.tensor(b, dtype=torch.float32)
            solution = torch.linalg.lstsq(tensor_matrix, tensor_b).solution.numpy()
            return {
                "approx_solution": solution.tolist()
            }
        else:
            raise ValueError("Unsupported operation for AI fallback.")
    except Exception as e:
        raise ValueError(f"AI fallback failed: {e}")

def main():
    parser = argparse.ArgumentParser(description="AI-Powered Matrix Solver")
    parser.add_argument('--file', type=str, required=True, help="Path to the input matrix file (CSV or JSON).")
    parser.add_argument('--operation', type=str, required=True, choices=['eigen', 'inverse', 'solve'], help="Matrix operation to perform.")
    parser.add_argument('--b', type=str, help="Path to the vector b (for solving linear systems). Required if operation is 'solve'.")
    parser.add_argument('--output', type=str, choices=['json', 'text'], default='json', help="Output format.")

    args = parser.parse_args()

    try:
        matrix = load_matrix_from_file(args.file)

        if args.operation == 'eigen':
            result = eigen_decomposition(matrix)
        elif args.operation == 'inverse':
            try:
                result = matrix_inversion(matrix)
            except ValueError:
                result = handle_ill_conditioned(matrix, 'inverse')
        elif args.operation == 'solve':
            if not args.b:
                raise ValueError("Path to vector b is required for solving linear systems.")
            b = load_matrix_from_file(args.b)
            try:
                result = solve_linear_system(matrix, b)
            except ValueError:
                result = handle_ill_conditioned(matrix, 'solve', b)
        else:
            raise ValueError("Invalid operation.")

        if args.output == 'json':
            print(json.dumps(result, indent=4))
        else:
            for key, value in result.items():
                print(f"{key}: {value}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()