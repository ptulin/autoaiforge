import pytest
from unittest.mock import MagicMock, patch, mock_open
import networkx as nx
from recursive_agent_debugger import load_agent_class, debug_agent, visualize_decision_tree

def test_load_agent_class_valid():
    with patch("os.path.exists", return_value=True), \
         patch("importlib.util.spec_from_file_location") as mock_spec, \
         patch("importlib.util.module_from_spec") as mock_module, \
         patch("sys.modules"):

        mock_agent_class = MagicMock()
        mock_module.return_value.Agent = mock_agent_class
        mock_spec.return_value.loader.exec_module = MagicMock()

        agent_class = load_agent_class("dummy_path.py")
        assert agent_class == mock_agent_class

def test_load_agent_class_file_not_found():
    with patch("os.path.exists", return_value=False):
        with pytest.raises(FileNotFoundError):
            load_agent_class("non_existent_file.py")

def test_debug_agent():
    MockAgent = MagicMock()
    mock_instance = MockAgent.return_value
    mock_instance.get_state.side_effect = ["state1", "state2"]
    mock_instance.make_decision.side_effect = ["decision1", "decision2"]
    mock_instance.improve_logic.side_effect = ["improvement1", "improvement2"]

    decision_tree, metrics = debug_agent(MockAgent, 2)

    assert len(decision_tree.nodes) == 2
    assert len(metrics) == 2
    assert metrics[0] == (1, "state1", "decision1", "improvement1")
    assert metrics[1] == (2, "state2", "decision2", "improvement2")

def test_visualize_decision_tree():
    tree = nx.DiGraph()
    tree.add_node("Node1")
    tree.add_node("Node2")
    tree.add_edge("Node1", "Node2")

    with patch("matplotlib.pyplot.savefig") as mock_savefig:
        visualize_decision_tree(tree, output_file="test_output.png")
        mock_savefig.assert_called_once_with("test_output.png")