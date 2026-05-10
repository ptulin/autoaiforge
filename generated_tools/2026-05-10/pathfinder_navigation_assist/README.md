# Pathfinder Navigation Assist

## Description
Pathfinder Navigation Assist is a CLI tool designed to process sensor input (e.g., depth cameras or LiDAR) from smart glasses to identify obstacles and generate navigation guidance. It is tailored for developers creating assistive tools for visually impaired users and includes features like collision warnings and optimal path suggestions.

## Features
- Load point cloud data from a file.
- Detect obstacles within a specified distance threshold.
- Generate audio feedback based on obstacle proximity.
- Play audio feedback to assist navigation.

## Installation
To use this tool, install the required dependencies:

```bash
pip install numpy pytest
```

## Usage
Run the CLI tool with the following command:

```bash
python pathfinder_navigation_assist.py --sensor_input <path_to_point_cloud_file> --feedback audio
```

### Arguments
- `--sensor_input`: Path to the depth data file (point cloud in .pcd format).
- `--feedback`: Type of feedback to provide (default: audio).

## Testing
To run the tests, use:

```bash
pytest test_pathfinder_navigation_assist.py
```

## License
This project is licensed under the MIT License.