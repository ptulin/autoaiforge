# Image Misinformation Checker

This Python tool helps developers determine if an image has been AI-generated or manipulated. It uses image recognition models to detect GAN-generated artifacts and verifies image metadata for authenticity.

## Features
- Detect GAN-generated artifacts in images.
- Extract and analyze image metadata for discrepancies.
- Process individual image files or directories of images.

## Installation
No external dependencies are required. This tool uses Python's standard library.

## Usage
Run the tool from the command line:

```bash
python image_misinformation_checker.py <input>
```

- `<input>`: Path to an image file or a directory containing image files.

## Example
```bash
python image_misinformation_checker.py /path/to/image.jpg
```

## Testing
Run the tests using `pytest`:

```bash
pytest test_image_misinformation_checker.py
```

## License
MIT License