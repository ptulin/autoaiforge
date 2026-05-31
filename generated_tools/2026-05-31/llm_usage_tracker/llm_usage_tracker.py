import sqlite3
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import pandas as pd
from rich.console import Console

Base = declarative_base()

class UsageLog(Base):
    __tablename__ = 'usage_logs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    api_key = Column(String, nullable=False)
    tokens_used = Column(Integer, nullable=False)
    user_id = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

class Tracker:
    def __init__(self, db_url='sqlite:///usage_logs.db'):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.console = Console()

    def log_usage(self, api_key, tokens_used, user_id):
        if not api_key or not user_id or tokens_used < 0:
            raise ValueError("Invalid input: api_key, tokens_used, and user_id are required.")

        session = self.Session()
        try:
            log = UsageLog(api_key=api_key, tokens_used=tokens_used, user_id=user_id)
            session.add(log)
            session.commit()
            self.console.log(f"Logged usage: {log}")
        except Exception as e:
            session.rollback()
            self.console.log(f"Error logging usage: {e}")
            raise
        finally:
            session.close()

    def generate_report(self, output_format='csv', output_file=None):
        session = self.Session()
        try:
            logs = session.query(UsageLog).all()
            data = [
                {
                    'id': log.id,
                    'api_key': log.api_key,
                    'tokens_used': log.tokens_used,
                    'user_id': log.user_id,
                    'timestamp': log.timestamp
                }
                for log in logs
            ]
            df = pd.DataFrame(data)

            if output_format == 'csv':
                if output_file:
                    df.to_csv(output_file, index=False)
                    self.console.log(f"Report saved to {output_file}")
                else:
                    self.console.print(df.to_csv(index=False))
            elif output_format == 'table':
                self.console.print(df.to_string(index=False))
            else:
                raise ValueError("Invalid output format. Use 'csv' or 'table'.")

        except Exception as e:
            self.console.log(f"Error generating report: {e}")
            raise
        finally:
            session.close()

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="LLM Usage Tracker")
    parser.add_argument('--db-url', type=str, default='sqlite:///usage_logs.db', help="Database URL")
    parser.add_argument('--log', action='store_true', help="Log usage")
    parser.add_argument('--report', action='store_true', help="Generate usage report")
    parser.add_argument('--api-key', type=str, help="API key")
    parser.add_argument('--tokens-used', type=int, help="Tokens used")
    parser.add_argument('--user-id', type=str, help="User ID")
    parser.add_argument('--output-format', type=str, choices=['csv', 'table'], default='csv', help="Report output format")
    parser.add_argument('--output-file', type=str, help="Output file for CSV report")

    args = parser.parse_args()

    tracker = Tracker(db_url=args.db_url)

    if args.log:
        if not args.api_key or args.tokens_used is None or not args.user_id:
            print("--log requires --api-key, --tokens-used, and --user-id")
        else:
            tracker.log_usage(api_key=args.api_key, tokens_used=args.tokens_used, user_id=args.user_id)

    if args.report:
        tracker.generate_report(output_format=args.output_format, output_file=args.output_file)