import pytest
from unittest.mock import patch, MagicMock, mock_open
from autonomous_agent_debugger import load_agent, debug_agent

def mock_agent(task_input):
    return f"Processed task: {task_input}"

def test_load_agent_valid():
    with patch("os.path.exists", return_value=True), \
         patch("importlib.util.spec_from_file_location") as mock_spec, \
         patch("importlib.util.module_from_spec") as mock_module, \
         patch("sys.modules"):

        mock_loader = MagicMock()
        mock_loader.exec_module = MagicMock()
        mock_spec.return_value = MagicMock(loader=mock_loader)
        mock_agent_module = MagicMock()
        mock_agent_module.run_agent = mock_agent
        mock_module.return_value = mock_agent_module

        agent_function = load_agent("dummy_path.py")
        assert callable(agent_function)

def test_load_agent_missing_file():
    with patch("os.path.exists", return_value=False):
        with pytest.raises(FileNotFoundError):
            load_agent("non_existent_file.py")

def test_load_agent_missing_function():
    with patch("os.path.exists", return_value=True), \
         patch("importlib.util.spec_from_file_location") as mock_spec, \
         patch("importlib.util.module_from_spec") as mock_module, \
         patch("sys.modules"):

        mock_loader = MagicMock()
        mock_loader.exec_module = MagicMock()
        mock_spec.return_value = MagicMock(loader=mock_loader)
        mock_agent_module = MagicMock()
        del mock_agent_module.run_agent  # Simulate missing run_agent function
        mock_module.return_value = mock_agent_module

        with pytest.raises(AttributeError):
            load_agent("dummy_path.py")

def test_debug_agent():
    with patch("prompt_toolkit.PromptSession.prompt", side_effect=["next", "quit"]), \
         patch("rich.console.Console.print") as mock_print:

        debug_agent(mock_agent, "Test Task")

        # Check that the output was printed
        mock_print.assert_any_call("[bold yellow]Output:[/bold yellow]", "Processed task: Test Task")