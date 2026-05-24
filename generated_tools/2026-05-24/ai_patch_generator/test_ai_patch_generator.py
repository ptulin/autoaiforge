import pytest
from unittest.mock import patch, mock_open
import ai_patch_generator

def test_analyze_vulnerability_file_not_found():
    with pytest.raises(FileNotFoundError):
        ai_patch_generator.analyze_vulnerability("non_existent_file.py")

@patch("ai_patch_generator.open", new_callable=mock_open, read_data="dummy source code")
@patch("os.path.exists", return_value=True)
@patch("ai_patch_generator.openai.Completion.create")
def test_analyze_vulnerability(mock_openai, mock_exists, mock_file):
    mock_openai.return_value = {
        'choices': [{'text': "Vulnerable code:\nprint('Hello')\nSuggested Patch:\nprint('Hello, World!')"}]
    }

    vulnerable_code, suggested_patch = ai_patch_generator.analyze_vulnerability("dummy_file.py")
    assert vulnerable_code == "Vulnerable code:\nprint('Hello')"
    assert suggested_patch == "print('Hello, World!')"

def test_generate_patch_file():
    vulnerable_code = "print('Hello')"
    suggested_patch = "print('Hello, World!')"
    output_path = "test.patch"

    with patch("builtins.open", mock_open()) as mock_file:
        ai_patch_generator.generate_patch_file(vulnerable_code, suggested_patch, output_path)
        mock_file.assert_called_once_with(output_path, 'w')
        handle = mock_file()
        handle.write.assert_called_once()
        written_content = handle.write.call_args[0][0]
        assert "-print('Hello')" in written_content
        assert "+print('Hello, World!')" in written_content
