import json
import pandas as pd
import numpy as np
from sqlalchemy import text

class AuditLogger:
    def __init__(self, db_connection):
        """
        Initialize the AuditLogger with a database connection.

        Args:
            db_connection: SQLAlchemy database connection object.
        """
        self.db_connection = db_connection
        self.audit_logs = []

    def execute_safe(self, query, params=None):
        """
        Execute a query safely, logging changes and detecting anomalies.

        Args:
            query (str): SQL query to execute.
            params (dict, optional): Parameters for the query.

        Returns:
            pd.DataFrame: Query result as a pandas DataFrame.
        """
        try:
            # Log the query
            self.audit_logs.append({
                "query": query,
                "params": params,
            })

            # Execute the query
            with self.db_connection.begin() as conn:
                result = conn.execute(text(query), params or {})

                # If the query modifies data, log before/after states
                if query.strip().lower().startswith(("update", "delete", "insert")):
                    self._log_modifications(query, conn)

                # Convert result to DataFrame
                df = pd.DataFrame(result.fetchall(), columns=result.keys())

                # Detect anomalies
                anomalies = self._detect_anomalies(df)
                if anomalies:
                    self.audit_logs[-1]["anomalies"] = anomalies

                return df

        except Exception as e:
            self.audit_logs.append({"error": str(e)})
            raise

    def _log_modifications(self, query, conn):
        """
        Log the before/after state of the database for modification queries.

        Args:
            query (str): SQL query.
            conn: SQLAlchemy connection object.
        """
        # Example: Log the state before and after the query
        self.audit_logs[-1]["modifications"] = {
            "before": "State before query execution (mocked for simplicity)",
            "after": "State after query execution (mocked for simplicity)",
        }

    def _detect_anomalies(self, df):
        """
        Detect anomalies in the query result using simple statistical checks.

        Args:
            df (pd.DataFrame): Query result.

        Returns:
            list: List of anomalies detected.
        """
        anomalies = []
        for column in df.select_dtypes(include=[np.number]).columns:
            mean = df[column].mean()
            std = df[column].std()
            for value in df[column]:
                if abs(value - mean) > 3 * std:  # Simple outlier detection
                    anomalies.append({"column": column, "value": value})
        return anomalies

    def export_logs(self, file_path):
        """
        Export audit logs to a JSON file.

        Args:
            file_path (str): Path to the output JSON file.
        """
        with open(file_path, "w") as f:
            json.dump(self.audit_logs, f, indent=4)

# Main guard for demonstration purposes
if __name__ == "__main__":
    from sqlalchemy import create_engine

    # Example usage
    engine = create_engine("sqlite:///:memory:")
    audit_logger = AuditLogger(engine)

    # Example query
    try:
        audit_logger.execute_safe("CREATE TABLE users (id INTEGER PRIMARY KEY, age INTEGER)")
        audit_logger.execute_safe("INSERT INTO users (age) VALUES (:age)", {"age": 25})
        audit_logger.execute_safe("UPDATE users SET age = age + 1")
        audit_logger.export_logs("audit_logs.json")
    except Exception as e:
        print(f"Error: {e}")