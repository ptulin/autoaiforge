# Sandbox Behavior Analyzer

## Description
The Sandbox Behavior Analyzer is a Python library designed to analyze and classify AI agent behavior logs to detect potential rogue actions. It uses anomaly detection techniques to identify deviations from expected behavior patterns based on historical data. The tool outputs a summary report highlighting flagged anomalies with risk scores.

## Installation

1. Clone the repository or download the `sandbox_behavior_analyzer.py` file.
2. Install the required dependencies:
   ```bash
   pip install numpy==1.23.5 scipy==1.10.1 pandas==1.5.3 scikit-learn==1.2.2
   ```

## Usage

### As a Library
```python
from sandbox_behavior_analyzer import analyze_logs

# Analyze a log file
anomalies = analyze_logs('agent_logs.json')
print(anomalies)
```

### As a CLI Tool
```bash
python sandbox_behavior_analyzer.py agent_logs.json
```

## Features
- **Log Parsing and Preprocessing**: Supports JSON and CSV log formats, handles missing values, and scales numeric data.
- **Anomaly Detection**: Uses Isolation Forest and statistical techniques to detect anomalies.
- **Risk Scoring**: Provides a risk score for each flagged anomaly.

## Example
Given a log file `agent_logs.json`:
```json
[
    {"action": "login", "duration": 5},
    {"action": "logout", "duration": 3}
]
```
Run the tool:
```bash
python sandbox_behavior_analyzer.py agent_logs.json
```
Output:
```
Anomalies detected:
   risk_score
0        2.5
```

## Testing
Run the tests using pytest:
```bash
pytest test_sandbox_behavior_analyzer.py
```