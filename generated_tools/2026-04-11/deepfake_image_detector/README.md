# Deepfake Image Detector

This CLI tool enables developers to analyze image files for potential deepfakes using pre-trained AI models. It leverages computer vision techniques to detect visual anomalies or artifacts often present in manipulated content. This is particularly useful for validating image authenticity in social media or forensic investigations.

## Features
- Analyze individual image files for deepfake likelihood.
- Process directories containing multiple image files.
- Outputs results in JSON format.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Install dependencies:
   ```bash
   pip install torch
   ```

## Usage

Run the tool using the command line:

```bash
python deepfake_image_detector.py --input <input_path> --output <output_path>
```

- `--input`: Path to an image file or a directory containing image files.
- `--output`: Path to save the JSON results.

### Example

Analyze a single image:
```bash
python deepfake_image_detector.py --input test_image.jpg --output results.json
```

Analyze a directory of images:
```bash
python deepfake_image_detector.py --input test_directory --output results.json
```

## Testing

Run the tests using `pytest`:

```bash
pytest test_deepfake_image_detector.py
```

## Notes

- This tool uses mocked models and image transformations for testing purposes. Replace the mocked components with actual pre-trained models for real-world usage.
