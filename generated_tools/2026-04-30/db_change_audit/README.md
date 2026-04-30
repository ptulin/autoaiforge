# AI-Powered DB Change Auditor

## Description
The AI-Powered DB Change Auditor is a Python library designed to record, audit, and analyze database changes triggered by AI-generated queries. It tracks all modifications, identifies anomalies, and provides a clear audit trail for database governance.

## Features
- **Track Database Modifications**: Logs before and after states for all modification queries.
- **Anomaly Detection**: Identifies anomalies in query results using statistical methods.
- **Easy Integration**: Works seamlessly with Python database workflows.

## Installation
```bash
pip install sqlalchemy pandas numpy
```

## Usage
```python
from sqlalchemy import create_engine
from db_change_audit import AuditLogger

engine = create_engine("sqlite:///:memory:")
audit_logger = AuditLogger(engine)

# Example queries
audit_logger.execute_safe("CREATE TABLE users (id INTEGER PRIMARY KEY, age INTEGER)")
audit_logger.execute_safe("INSERT INTO users (age) VALUES (:age)", {"age": 25})
audit_logger.execute_safe("UPDATE users SET age = age + 1")

audit_logger.export_logs("audit_logs.json")
```

## Example Output
Audit logs are saved in JSON format:
```json
[
    {
        "query": "UPDATE users SET age = age + 1",
        "modifications": {
            "before": "State before query execution",
            "after": "State after query execution"
        },
        "anomalies": []
    }
]
```

## License
MIT License