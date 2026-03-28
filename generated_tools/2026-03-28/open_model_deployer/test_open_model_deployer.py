import pytest
from unittest.mock import patch, MagicMock
from open_model_deployer import deploy_model

def test_deploy_model_fastapi_local():
    with patch("open_model_deployer.load_model") as mock_model_loader:
        mock_model = MagicMock()
        mock_model.return_value = lambda x: f"Mock prediction for '{x}'"
        mock_model_loader.return_value = mock_model

        with patch("open_model_deployer.uvicorn.run") as mock_uvicorn:
            deploy_model("./local_model_dir", "fastapi")
            mock_model_loader.assert_called_once_with("./local_model_dir")
            mock_uvicorn.assert_called_once()

def test_deploy_model_fastapi_huggingface():
    with patch("open_model_deployer.load_model") as mock_model_loader:
        mock_model = MagicMock()
        mock_model.return_value = lambda x: f"Mock prediction for '{x}'"
        mock_model_loader.return_value = mock_model

        with patch("open_model_deployer.uvicorn.run") as mock_uvicorn:
            deploy_model("huggingface/model-id", "fastapi")
            mock_model_loader.assert_called_once_with("huggingface/model-id")
            mock_uvicorn.assert_called_once()

def test_deploy_model_invalid_backend():
    with pytest.raises(ValueError, match="Currently, only 'fastapi' backend is supported."):
        deploy_model("huggingface/model-id", "flask")