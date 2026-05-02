import pytest
from unittest.mock import patch, MagicMock, mock_open
import auto_patch_applier
import os

def test_fetch_patch_suggestions():
    with patch("openai.Completion.create") as mock_openai:
        mock_openai.return_value = MagicMock(choices=[MagicMock(text="Patch content")])
        result = auto_patch_applier.fetch_patch_suggestions("./test_project")
        assert result == "Patch content"

def test_apply_patch():
    with patch("subprocess.run") as mock_subprocess, \
         patch("builtins.open", mock_open()):
        mock_subprocess.return_value = MagicMock(returncode=0, stderr="")
        result = auto_patch_applier.apply_patch("patch content", "./test_project")
        assert result == "Patch applied successfully."

def test_sandbox_test_patch():
    with patch("shutil.copytree") as mock_copytree, \
         patch("shutil.rmtree") as mock_rmtree, \
         patch("subprocess.run") as mock_subprocess:
        
        mock_subprocess.return_value = MagicMock(returncode=0)
        result = auto_patch_applier.sandbox_test_patch("./test_project")
        assert result == "Sandbox testing passed."

def test_rollback_patch():
    with patch("subprocess.run") as mock_subprocess:
        mock_subprocess.return_value = MagicMock(returncode=0, stderr="")
        result = auto_patch_applier.rollback_patch("./test_project")
        assert result == "Patch rolled back successfully."
