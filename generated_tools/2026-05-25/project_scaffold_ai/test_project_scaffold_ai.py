import os
import pytest
from unittest.mock import patch, mock_open
from project_scaffold_ai import generate_project

@pytest.fixture
def mock_os_makedirs():
    with patch('os.makedirs') as mock_makedirs:
        yield mock_makedirs

@pytest.fixture
def mock_open_file():
    with patch('builtins.open', mock_open()) as mock_file:
        yield mock_file

def test_generate_project_base(mock_os_makedirs, mock_open_file):
    generate_project('python', 'flask', '', 'test_project')
    mock_os_makedirs.assert_called_once_with('test_project', exist_ok=True)
    mock_open_file.assert_called_once_with(os.path.join('test_project', 'app.py'), 'w')
    mock_open_file().write.assert_called_once_with("""from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return \"Hello, Flask!\"

if __name__ == '__main__':
    app.run(debug=True)
""")

def test_generate_project_auth_feature(mock_os_makedirs, mock_open_file):
    generate_project('python', 'flask', 'auth', 'test_project')
    mock_os_makedirs.assert_called_once_with('test_project', exist_ok=True)
    mock_open_file.assert_called_once_with(os.path.join('test_project', 'app.py'), 'w')
    mock_open_file().write.assert_called_once_with("""from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/login', methods=['POST'])
def login():
    return jsonify({'message': 'Login endpoint'})

if __name__ == '__main__':
    app.run(debug=True)
""")

def test_generate_project_invalid_language(mock_os_makedirs):
    with patch('builtins.print') as mock_print:
        generate_project('java', 'flask', '', 'test_project')
        mock_print.assert_called_once_with("Language or framework not supported.")