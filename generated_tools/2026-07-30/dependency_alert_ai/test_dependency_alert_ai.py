import pytest
from unittest.mock import patch, mock_open
from dependency_alert_ai import analyze_dependencies, fetch_vulnerability_data

def test_fetch_vulnerability_data():
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "result": {
                "CVE_Items": [
                    {
                        "cve": {
                            "CVE_data_meta": {"ID": "CVE-2023-1234"},
                            "description": {"description_data": [{"value": "Test vulnerability."}]}
                        },
                        "configurations": {
                            "nodes": [
                                {
                                    "cpe_match": [
                                        {"cpe23Uri": "cpe:2.3:a:example:package:1.0.0"}
                                    ]
                                }
                            ]
                        }
                    }
                ]
            }
        }

        vulnerabilities = fetch_vulnerability_data("example", "1.0.0")
        assert len(vulnerabilities) == 1
        assert vulnerabilities[0]["CVE_data_meta"]["ID"] == "CVE-2023-1234"

def test_analyze_dependencies_file_not_found():
    result = analyze_dependencies("nonexistent.txt")
    assert "error" in result
    assert result["error"] == "File nonexistent.txt does not exist."

def test_analyze_dependencies_with_mocked_data():
    mock_requirements = "example==1.0.0\n"
    with patch("builtins.open", mock_open(read_data=mock_requirements)):
        with patch("dependency_alert_ai.fetch_vulnerability_data") as mock_fetch:
            mock_fetch.return_value = [
                {
                    "CVE_data_meta": {"ID": "CVE-2023-1234"},
                    "description": {"description_data": [{"value": "Test vulnerability."}]}
                }
            ]
            results = analyze_dependencies("requirements.txt")
            assert "example" in results
            assert results["example"]["version"] == "1.0.0"
            assert len(results["example"]["vulnerabilities"]) == 1