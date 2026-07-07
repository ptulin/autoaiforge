import os
import json
import argparse
import psutil
import requests

def validate_dependencies(workspace_path):
    """Check if required dependencies are installed in the workspace."""
    requirements_file = os.path.join(workspace_path, 'requirements.txt')
    if not os.path.exists(requirements_file):
        return {'status': 'error', 'message': 'requirements.txt not found in workspace.'}

    missing_dependencies = []
    with open(requirements_file, 'r') as f:
        for line in f:
            package = line.strip()
            if not package:
                continue
            try:
                __import__(package.split('==')[0])
            except ModuleNotFoundError:
                missing_dependencies.append(package)

    if missing_dependencies:
        return {'status': 'error', 'missing_dependencies': missing_dependencies}
    return {'status': 'success', 'message': 'All dependencies are installed.'}

def validate_hardware():
    """Check hardware compatibility for AI workloads."""
    gpu_available = any('nvidia' in partition.device.lower() for partition in psutil.disk_partitions(all=False))
    cpu_cores = psutil.cpu_count(logical=True)

    return {
        'gpu_available': gpu_available,
        'cpu_cores': cpu_cores,
        'status': 'success' if gpu_available and cpu_cores >= 4 else 'warning',
        'message': 'Hardware compatibility check completed.'
    }

def validate_endpoints():
    """Check if local and remote endpoints are reachable."""
    endpoints = ['http://localhost:5000', 'https://api.example.com']
    unreachable_endpoints = []

    for endpoint in endpoints:
        try:
            response = requests.get(endpoint, timeout=5)
            if response.status_code != 200:
                unreachable_endpoints.append(endpoint)
        except requests.RequestException:
            unreachable_endpoints.append(endpoint)

    if unreachable_endpoints:
        return {'status': 'error', 'unreachable_endpoints': unreachable_endpoints}
    return {'status': 'success', 'message': 'All endpoints are reachable.'}

def main():
    """Local AI Workspace Validator"""
    parser = argparse.ArgumentParser(description='Local AI Workspace Validator')
    parser.add_argument('--workspace', required=True, type=str, help='Path to the AI workspace.')
    parser.add_argument('--output', type=str, help='Path to save the validation report as JSON.')
    args = parser.parse_args()

    report = {
        'dependencies': validate_dependencies(args.workspace),
        'hardware': validate_hardware(),
        'endpoints': validate_endpoints()
    }

    if args.output:
        with open(args.output, 'w') as f:
            json.dump(report, f, indent=4)
        print(f'Report saved to {args.output}')
    else:
        print(json.dumps(report, indent=4))

if __name__ == '__main__':
    main()
