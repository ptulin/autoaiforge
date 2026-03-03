# Media Manipulation Detector

## Overview
The Media Manipulation Detector is a Python tool designed to analyze images and videos for potential signs of manipulation or deepfake content. It uses computer vision techniques to identify artifacts, inconsistencies, and anomalies in visual media.

## Features
- Detect anomalies in images and videos.
- Save analysis results to a JSON file.
- Simple CLI interface for ease of use.

## Installation
Install the required dependencies using pip:

```bash
pip install opencv-python numpy pytest
```

## Usage
Run the tool from the command line:

```bash
python media_manipulation_detector.py <file_path> <output>
```

- `<file_path>`: Path to the input image or video file.
- `<output>`: Path to the output JSON file where results will be saved.

Example:

```bash
python media_manipulation_detector.py example.jpg output.json
```

## Testing
To run the tests, use pytest:

```bash
pytest test_media_manipulation_detector.py
```

## Limitations
- The anomaly detection logic is a placeholder and should be replaced with a more robust algorithm for production use.
- The tool currently supports only basic image and video formats.

## License
This project is licensed under the MIT License.