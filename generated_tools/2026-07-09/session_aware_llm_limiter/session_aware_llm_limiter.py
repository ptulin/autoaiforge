import time
import json

class Limiter:
    def __init__(self, query_limit=100, session_duration=3600):
        """
        Initialize the Limiter with configurable thresholds.

        :param query_limit: Maximum number of queries allowed per session.
        :param session_duration: Maximum session duration in seconds.
        """
        self.query_limit = query_limit
        self.session_duration = session_duration
        self.sessions = {}

    def log_interaction(self, user_id):
        """
        Log a user interaction and check thresholds.

        :param user_id: Unique identifier for the user.
        :raises Exception: If thresholds are exceeded.
        """
        current_time = time.time()
        if user_id not in self.sessions:
            self.sessions[user_id] = {
                'start_time': current_time,
                'query_count': 0
            }

        session = self.sessions[user_id]
        session_duration = current_time - session['start_time']

        if session_duration > self.session_duration:
            # Reset session if duration exceeded
            self.sessions[user_id] = {
                'start_time': current_time,
                'query_count': 1
            }
        else:
            session['query_count'] += 1

        if session['query_count'] > self.query_limit:
            raise Exception(f"Query limit exceeded for user {user_id}. Limit: {self.query_limit}")

        if session_duration > self.session_duration:
            raise Exception(f"Session duration exceeded for user {user_id}. Limit: {self.session_duration} seconds")

    def export_sessions(self):
        """
        Export the current session data as JSON.

        :return: JSON string of session data.
        """
        return json.dumps(self.sessions)

    def reset_session(self, user_id):
        """
        Reset the session for a specific user.

        :param user_id: Unique identifier for the user.
        """
        if user_id in self.sessions:
            del self.sessions[user_id]

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Session-Aware LLM Limiter")
    parser.add_argument('--query_limit', type=int, default=100, help="Maximum number of queries allowed per session.")
    parser.add_argument('--session_duration', type=int, default=3600, help="Maximum session duration in seconds.")
    args = parser.parse_args()

    limiter = Limiter(query_limit=args.query_limit, session_duration=args.session_duration)
    print("Limiter initialized. Use the API methods to log interactions and monitor sessions.")