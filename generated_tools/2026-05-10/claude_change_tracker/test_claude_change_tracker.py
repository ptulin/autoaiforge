import pytest
import pandas as pd
from claude_change_tracker import track_changes

def test_track_changes_basic():
    dataset_v1 = pd.DataFrame({
        'input': ['a', 'b', 'c'],
        'output': ['x', 'y', 'z'],
        'expected': ['x', 'y', 'w']
    })

    dataset_v2 = pd.DataFrame({
        'input': ['a', 'b', 'c'],
        'output': ['x', 'y', 'w'],
        'expected': ['x', 'y', 'w']
    })

    result = track_changes(dataset_v1, dataset_v2)
    assert result['summary']['improved'] == 1
    assert result['summary']['worsened'] == 0
    assert result['summary']['unchanged'] == 2

def test_track_changes_missing_columns():
    dataset_v1 = pd.DataFrame({
        'input': ['a', 'b', 'c'],
        'output': ['x', 'y', 'z']
    })

    dataset_v2 = pd.DataFrame({
        'input': ['a', 'b', 'c'],
        'output': ['x', 'y', 'w']
    })

    with pytest.raises(ValueError):
        track_changes(dataset_v1, dataset_v2)

def test_track_changes_edge_case_empty():
    dataset_v1 = pd.DataFrame(columns=['input', 'output', 'expected'])
    dataset_v2 = pd.DataFrame(columns=['input', 'output', 'expected'])

    result = track_changes(dataset_v1, dataset_v2)
    assert result['summary']['total_samples'] == 0
    assert result['summary']['improved'] == 0
    assert result['summary']['worsened'] == 0
    assert result['summary']['unchanged'] == 0