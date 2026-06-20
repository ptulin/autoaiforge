# Image Metadata Auditor

## Overview
The Image Metadata Auditor is a Python tool designed to analyze image metadata, such as EXIF data, to identify inconsistencies or anomalies that might indicate an image was generated or manipulated by AI tools. It helps developers validate metadata integrity and detect possible tampering.

## Features
- Extracts EXIF metadata from image files.
- Detects anomalies such as:
  - Use of AI or editing software.
  - Mismatched timestamps.
  - Missing critical metadata fields.

## Installation
To install the required dependencies, run:

```bash
pip install Pillow exifread
```

## Usage
Run the tool from the command line:

```bash
python image_metadata_auditor.py <image_path>
```

Example:

```bash
python image_metadata_auditor.py example.jpg
```

## Output
The tool will output the extracted metadata and any detected anomalies. If no anomalies are detected, it will indicate so.

## Testing
To run the tests, install `pytest`:

```bash
pip install pytest
```

Then execute:

```bash
pytest test_image_metadata_auditor.py
```

The tests include:
- Valid image with no anomalies.
- Missing file.
- Image with anomalies detected.

## License
This project is licensed under the MIT License.