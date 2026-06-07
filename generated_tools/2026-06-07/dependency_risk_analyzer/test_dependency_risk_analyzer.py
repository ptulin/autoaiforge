import pytest
from unittest.mock import patch, mock_open, MagicMock
from dependency_risk_analyzer import parse_dependencies, query_cve_database, analyze_dependencies

def test_parse_dependencies_requirements():
    mock_data = "requests==2.26.0\npandas==1.3.3\n"
    with patch("builtins.open", mock_open(read_data=mock_data)):
        dependencies = parse_dependencies("requirements.txt")
        assert dependencies == [
            {"name": "requests", "version": "==2.26.0"},
            {"name": "pandas", "version": "==1.3.3"}
        ]

def test_parse_dependencies_pyproject():
    mock_data = "[tool.poetry.dependencies]\nrequests = \"2.26.0\"\npandas = \"1.3.3\"\n"
    with patch("builtins.open", mock_open(read_data=mock_data)):
        with patch("toml.load", return_value={"tool": {"poetry": {"dependencies": {"requests": "2.26.0", "pandas": "1.3.3"}}}}):
            dependencies = parse_dependencies("pyproject.toml")
            assert dependencies == [
                {"name": "requests", "version": "2.26.0"},
                {"name": "pandas", "version": "1.3.3"}
            ]

def test_query_cve_database():
    mock_response = {
        "result": {
            "CVE_Items": [
                {
                    "cve": {
                        "CVE_data_meta": {"ID": "CVE-2023-1234"},
                        "description": {"description_data": [{"value": "Example vulnerability description."}]}
                    }
                }
            ]
        }
    }
    with patch("requests.get") as mock_get:
        mock_get.return_value = MagicMock(status_code=200, json=lambda: mock_response)
        vulnerabilities = query_cve_database("requests", "2.26.0")
        assert vulnerabilities == [
            {"id": "CVE-2023-1234", "description": "Example vulnerability description."}
        ]

def test_analyze_dependencies():
    mock_dependencies = [
        {"name": "requests", "version": "2.26.0"},
        {"name": "pandas", "version": "1.3.3"}
    ]
    mock_cve_data = [
        {"id": "CVE-2023-1234", "description": "Example vulnerability description.", "risk_level": "LOW", "confidence": 0.85}
    ]
    with patch("dependency_risk_analyzer.parse_dependencies", return_value=mock_dependencies):
        with patch("dependency_risk_analyzer.query_cve_database", return_value=mock_cve_data):
            with patch("dependency_risk_analyzer.classify_risk", return_value=mock_cve_data):
                report = analyze_dependencies("requirements.txt", "json")
                assert "requests" in report
                assert "pandas" in report
