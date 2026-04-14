import argparse
import json
import httpx
from http.server import BaseHTTPRequestHandler, HTTPServer
import re

class ProxyHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        # Log the request
        self.server.log_request(self.path, post_data, self.headers)

        # Forward the request to the actual API
        try:
            response = self.server.forward_request(self.path, post_data, self.headers)
        except httpx.RequestError as e:
            self.send_error(502, f"Bad Gateway: {e}")
            return

        # Log the response
        self.server.log_response(self.path, response.text)

        # Send the response back to the client
        self.send_response(response.status_code)
        for header, value in response.headers.items():
            if header.lower() not in ["content-length", "transfer-encoding"]:
                self.send_header(header, value)
        self.end_headers()
        self.wfile.write(response.content)

class ProxyServer(HTTPServer):
    def __init__(self, server_address, RequestHandlerClass, logfile, target_url):
        super().__init__(server_address, RequestHandlerClass)
        self.logfile = logfile
        self.target_url = target_url
        self.logs = []

    def log_request(self, path, data, headers):
        log_entry = {
            "type": "request",
            "path": path,
            "data": data.decode("utf-8"),
            "headers": {key: headers[key] for key in headers.keys()}
        }
        self.logs.append(log_entry)
        self.analyze_data(log_entry)

    def log_response(self, path, data):
        log_entry = {
            "type": "response",
            "path": path,
            "data": data
        }
        self.logs.append(log_entry)
        self.analyze_data(log_entry)

    def forward_request(self, path, data, headers):
        url = f"{self.target_url}{path}"
        response = httpx.post(url, data=data, headers=headers)
        return response

    def analyze_data(self, log_entry):
        # Example: Detect sensitive information
        sensitive_patterns = [
            r"password=\S+",
            r"api_key=\S+",
            r"secret=\S+"
        ]
        for pattern in sensitive_patterns:
            if re.search(pattern, log_entry["data"]):
                log_entry["anomaly"] = "Sensitive information detected"

    def save_logs(self):
        with open(self.logfile, "w") as f:
            json.dump(self.logs, f, indent=4)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI API Traffic Monitor")
    parser.add_argument("--port", type=int, required=True, help="Port to run the proxy server on")
    parser.add_argument("--logfile", type=str, required=True, help="File to save traffic logs")
    parser.add_argument("--target_url", type=str, required=True, help="Target URL of the AI API to forward requests to")
    args = parser.parse_args()

    server_address = ('', args.port)
    httpd = ProxyServer(server_address, ProxyHTTPRequestHandler, args.logfile, args.target_url)

    print(f"Starting proxy server on port {args.port}...")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        httpd.save_logs()
        httpd.server_close()
