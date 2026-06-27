import pytest
import numpy as np
from unittest.mock import patch, mock_open
from matrix_solver_ai import load_matrix_from_file, eigen_decomposition, matrix_inversion, solve_linear_system, handle_ill_conditioned

def test_load_matrix_from_file_csv():
    mock_csv = "1,2,3\n4,5,6\n7,8,9"
    with patch("builtins.open", mock_open(read_data=mock_csv)) as mock_file:
        with patch("numpy.loadtxt", return_value=np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])):
            matrix = load_matrix_from_file("test.csv")
            np.testing.assert_array_equal(matrix, np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]))

def test_load_matrix_from_file_json():
    mock_json = "[[1, 2, 3], [4, 5, 6], [7, 8, 9]]"
    with patch("builtins.open", mock_open(read_data=mock_json)) as mock_file:
        with patch("json.load", return_value=[[1, 2, 3], [4, 5, 6], [7, 8, 9]]):
            matrix = load_matrix_from_file("test.json")
            np.testing.assert_array_equal(matrix, np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]))

def test_eigen_decomposition():
    matrix = np.array([[1, 2], [2, 1]])
    result = eigen_decomposition(matrix)
    assert "eigenvalues" in result
    assert "eigenvectors" in result

def test_matrix_inversion():
    matrix = np.array([[1, 2], [3, 4]])
    result = matrix_inversion(matrix)
    expected_inverse = np.linalg.inv(matrix).tolist()
    assert result["inverse"] == expected_inverse

def test_solve_linear_system():
    matrix = np.array([[3, 1], [1, 2]])
    b = np.array([9, 8])
    result = solve_linear_system(matrix, b)
    expected_solution = np.linalg.solve(matrix, b).tolist()
    assert result["solution"] == expected_solution

def test_handle_ill_conditioned():
    matrix = np.array([[1e-10, 0], [0, 1e-10]])
    result = handle_ill_conditioned(matrix, 'inverse')
    assert "approx_inverse" in result
    assert np.allclose(np.dot(matrix, np.array(result["approx_inverse"])), np.eye(2), atol=1e-5)
