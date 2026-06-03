import os
import yaml
from flask import Flask, request, jsonify
import requests
from threading import Thread

def start_server(config_path):
    """
    Start the local server to facilitate communication between IDE and AI agent.

    Args:
        config_path (str): Path to the configuration YAML file.
    """
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)

    ide = config.get('ide')
    agent_url = config.get('agent_url')

    if not ide or not agent_url:
        raise ValueError("Configuration file must specify 'ide' and 'agent_url'.")

    app = Flask(__name__)

    @app.route('/suggest', methods=['POST'])
    def suggest():
        """Endpoint to get code suggestions from the agent."""
        try:
            data = request.json
            if not data or 'code' not in data:
                return jsonify({"error": "Invalid input, 'code' key is required."}), 400

            response = requests.post(f"{agent_url}/suggest", json=data)
            response.raise_for_status()
            return jsonify(response.json())
        except requests.RequestException as e:
            return jsonify({"error": f"Agent request failed: {str(e)}"}), 500

    @app.route('/debug', methods=['POST'])
    def debug():
        """Endpoint to get debugging suggestions from the agent."""
        try:
            data = request.json
            if not data or 'code' not in data:
                return jsonify({"error": "Invalid input, 'code' key is required."}), 400

            response = requests.post(f"{agent_url}/debug", json=data)
            response.raise_for_status()
            return jsonify(response.json())
        except requests.RequestException as e:
            return jsonify({"error": f"Agent request failed: {str(e)}"}), 500

    @app.route('/refactor', methods=['POST'])
    def refactor():
        """Endpoint to get refactoring suggestions from the agent."""
        try:
            data = request.json
            if not data or 'code' not in data:
                return jsonify({"error": "Invalid input, 'code' key is required."}), 400

            response = requests.post(f"{agent_url}/refactor", json=data)
            response.raise_for_status()
            return jsonify(response.json())
        except requests.RequestException as e:
            return jsonify({"error": f"Agent request failed: {str(e)}"}), 500

    def run():
        print(f"Starting server for {ide} integration on http://127.0.0.1:5000")
        app.run(debug=False, port=5000)

    thread = Thread(target=run)
    thread.daemon = True
    thread.start()
