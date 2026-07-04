import pytest
from unittest.mock import patch, mock_open
from ml_dependency_inspector import analyze_file, analyze_directory

def test_analyze_file_deprecated_methods():
    code = """
import sklearn
model.fit_transform(data)
model.predict_proba(data)
"""
    with patch("builtins.open", mock_open(read_data=code)):
        with patch("os.path.isfile", return_value=True):
            results = analyze_file("dummy.py")
            assert "fit_transform" in results["deprecated_methods"]
            assert "predict_proba" in results["deprecated_methods"]

def test_analyze_file_insecure_configurations():
    code = """
model.train(data, shuffle=True)
"""
    with patch("builtins.open", mock_open(read_data=code)):
        with patch("os.path.isfile", return_value=True):
            results = analyze_file("dummy.py")
            assert "shuffle=True in training" in results["insecure_configurations"]

def test_analyze_directory():
    code1 = """
model.fit_transform(data)
"""
    code2 = """
model.train(data, shuffle=True)
"""
    mock_files = {
        "/path/file1.py": code1,
        "/path/file2.py": code2
    }

    def mock_file_open(file, *args, **kwargs):
        if file in mock_files:
            return mock_open(read_data=mock_files[file])()
        raise FileNotFoundError(f"File {file} not found")

    with patch("os.path.isdir", return_value=True):
        with patch("os.walk") as mock_walk:
            mock_walk.return_value = [("/path", [], ["file1.py", "file2.py"])]
            with patch("builtins.open", mock_file_open):
                results = analyze_directory("/path")
                assert len(results) == 2
                assert "fit_transform" in results[0]["results"]["deprecated_methods"]
                assert "shuffle=True in training" not in results[0]["results"]["insecure_configurations"]
                assert "shuffle=True in training" in results[1]["results"]["insecure_configurations"]
