import argparse
import requests
import time
import queue
from flask import Flask, request, jsonify
from threading import Thread, Lock

app = Flask(__name__)

class LLMInstance:
    def __init__(self, name, url, quota):
        self.name = name
        self.url = url
        self.quota = quota
        self.lock = Lock()
        self.requests_handled = 0

    def is_available(self):
        with self.lock:
            return self.requests_handled < self.quota

    def handle_request(self, query):
        with self.lock:
            if self.requests_handled >= self.quota:
                raise Exception(f"Quota exceeded for {self.name}")
            self.requests_handled += 1

        try:
            start_time = time.time()
            response = requests.post(self.url, json={"query": query}, timeout=5)
            response_time = time.time() - start_time
            response.raise_for_status()
            return response.json(), response_time
        except requests.RequestException as e:
            return {"error": str(e)}, float('inf')

class LLMRouter:
    def __init__(self):
        self.instances = []

    def add_instance(self, name, url, quota):
        self.instances.append(LLMInstance(name, url, quota))

    def route_request(self, query):
        available_instances = [instance for instance in self.instances if instance.is_available()]

        if not available_instances:
            return {"error": "No available LLM instances"}

        best_instance = None
        best_response_time = float('inf')
        best_response = None

        for instance in available_instances:
            try:
                response, response_time = instance.handle_request(query)
                if response_time < best_response_time:
                    best_response_time = response_time
                    best_instance = instance
                    best_response = response
            except Exception as e:
                continue

        if best_instance:
            return best_response
        else:
            return {"error": "All instances failed"}

router = LLMRouter()

def setup_router():
    # Example setup, replace with real URLs and quotas
    router.add_instance("local1", "http://localhost:5001/query", 10)
    router.add_instance("cloud", "https://cloud-llm.example.com/query", 100)

@app.route('/query', methods=['POST'])
def query():
    data = request.json
    if not data or 'query' not in data:
        return jsonify({"error": "Invalid input, 'query' is required"}), 400

    query = data['query']
    response = router.route_request(query)
    return jsonify(response)

def main():
    parser = argparse.ArgumentParser(description="LLM Load Balancer")
    parser.add_argument('--query', type=str, help="Query to send to the LLMs")
    parser.add_argument('--targets', type=str, help="Comma-separated list of target LLM instances")
    args = parser.parse_args()

    if args.query:
        setup_router()
        response = router.route_request(args.query)
        print(response)
    else:
        setup_router()
        app.run(host='0.0.0.0', port=5000)

if __name__ == "__main__":
    main()