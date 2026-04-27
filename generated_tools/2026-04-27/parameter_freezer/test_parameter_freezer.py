import pytest
from unittest.mock import patch, MagicMock, mock_open
from parameter_freezer import freeze_model_layers, load_config

def test_freeze_model_layers():
    model = MagicMock()
    param1 = MagicMock()
    param2 = MagicMock()
    param1.requires_grad = True
    param2.requires_grad = True
    model.named_parameters.return_value = [
        ("layer1.weight", param1),
        ("layer2.bias", param2),
    ]
    layers_to_freeze = ["layer1"]

    freeze_model_layers(model, layers_to_freeze)

    assert param1.requires_grad is False
    assert param2.requires_grad is True

def test_load_config():
    with patch("builtins.open", mock_open(read_data="freeze_layers:\n  - layer1\n  - layer2")):
        config = load_config("dummy_path.yaml")
        assert config == {"freeze_layers": ["layer1", "layer2"]}

@pytest.mark.parametrize("mock_layers,layers_to_freeze,expected", [
    ([
        ("layer1.weight", MagicMock(requires_grad=True)),
        ("layer2.bias", MagicMock(requires_grad=True)),
    ], ["layer1"], [False, True]),
    ([
        ("layer1.weight", MagicMock(requires_grad=True)),
        ("layer2.bias", MagicMock(requires_grad=True)),
    ], ["layer2"], [True, False]),
    ([
        ("layer1.weight", MagicMock(requires_grad=True)),
        ("layer2.bias", MagicMock(requires_grad=True)),
    ], ["layer1", "layer2"], [False, False]),
])
def test_freeze_layers(mock_layers, layers_to_freeze, expected):
    model = MagicMock()
    model.named_parameters.return_value = mock_layers

    freeze_model_layers(model, layers_to_freeze)

    for i, (_, param) in enumerate(mock_layers):
        assert param.requires_grad is expected[i]
