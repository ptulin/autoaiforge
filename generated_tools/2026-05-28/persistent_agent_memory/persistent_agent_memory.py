import sqlite3
import json
import redis
from pydantic import BaseModel, ValidationError
from typing import Optional, Dict, Any

class AgentMemory:
    def __init__(self, backend: str, **kwargs):
        self.backend = backend.lower()
        if self.backend == 'sqlite':
            self.db_path = kwargs.get('db_path', ':memory:')
            self._init_sqlite()
        elif self.backend == 'json':
            self.file_path = kwargs.get('file_path', 'memory.json')
            self._init_json()
        elif self.backend == 'redis':
            self.redis_client = redis.Redis(
                host=kwargs.get('host', 'localhost'),
                port=kwargs.get('port', 6379),
                decode_responses=True
            )
        else:
            raise ValueError("Unsupported backend. Choose 'sqlite', 'json', or 'redis'.")

    def _init_sqlite(self):
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS memory (
                                agent_id TEXT PRIMARY KEY,
                                state TEXT
                              )''')
        self.conn.commit()

    def _init_json(self):
        try:
            with open(self.file_path, 'r') as f:
                json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            with open(self.file_path, 'w') as f:
                json.dump({}, f)

    def save_state(self, agent_id: str, state: Dict[str, Any]):
        if not isinstance(state, dict):
            raise ValueError("State must be a dictionary.")

        if self.backend == 'sqlite':
            self.cursor.execute('''INSERT OR REPLACE INTO memory (agent_id, state)
                                   VALUES (?, ?)''', (agent_id, json.dumps(state)))
            self.conn.commit()
        elif self.backend == 'json':
            with open(self.file_path, 'r') as f:
                data = json.load(f)
            data[agent_id] = state
            with open(self.file_path, 'w') as f:
                json.dump(data, f)
        elif self.backend == 'redis':
            self.redis_client.set(agent_id, json.dumps(state))

    def load_state(self, agent_id: str) -> Optional[Dict[str, Any]]:
        if self.backend == 'sqlite':
            self.cursor.execute('SELECT state FROM memory WHERE agent_id = ?', (agent_id,))
            result = self.cursor.fetchone()
            return json.loads(result[0]) if result else None
        elif self.backend == 'json':
            with open(self.file_path, 'r') as f:
                data = json.load(f)
            return data.get(agent_id)
        elif self.backend == 'redis':
            result = self.redis_client.get(agent_id)
            return json.loads(result) if result else None

    def delete_state(self, agent_id: str):
        if self.backend == 'sqlite':
            self.cursor.execute('DELETE FROM memory WHERE agent_id = ?', (agent_id,))
            self.conn.commit()
        elif self.backend == 'json':
            with open(self.file_path, 'r') as f:
                data = json.load(f)
            if agent_id in data:
                del data[agent_id]
            with open(self.file_path, 'w') as f:
                json.dump(data, f)
        elif self.backend == 'redis':
            self.redis_client.delete(agent_id)

    def __del__(self):
        if self.backend == 'sqlite':
            self.conn.close()
