import os
import pytest
from unittest import mock
from llm_model_switcher import activate_model

def test_activate_model_success(tmp_path):
    base_path = tmp_path / "models"
    base_path.mkdir()
    version = "llama_cpp_v0.2"
    model_path = base_path / version
    model_path.mkdir()

    activate_model(version, str(base_path))

    symlink_path = base_path / "current"
    assert symlink_path.is_symlink()
    assert os.readlink(symlink_path) == str(model_path)
    assert os.environ['LLM_MODEL_PATH'] == str(symlink_path)

def test_activate_model_version_not_found(tmp_path):
    base_path = tmp_path / "models"
    base_path.mkdir()
    version = "non_existent_version"

    with pytest.raises(FileNotFoundError):
        activate_model(version, str(base_path))

def test_activate_model_symlink_error(tmp_path):
    base_path = tmp_path / "models"
    base_path.mkdir()
    version = "llama_cpp_v0.2"
    model_path = base_path / version
    model_path.mkdir()

    symlink_path = base_path / "current"
    symlink_path.touch()  # Create a file instead of a symlink

    with mock.patch("os.symlink", side_effect=OSError("Mocked symlink error")):
        with pytest.raises(Exception, match="Failed to create symbolic link: Mocked symlink error"):
            activate_model(version, str(base_path))