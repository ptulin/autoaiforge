# Radiology Image Preprocessor

## Description
Radiology Image Preprocessor is a Python tool designed to preprocess medical imaging data such as X-rays and MRIs for use in AI models. It automates normalization, resizing, and denoising of images, ensuring consistent input quality for diagnostic tools.

## Features
- **Automated Image Normalization**: Scales pixel values to the range [0, 1].
- **Noise Reduction**: Applies Gaussian filtering for clearer model input.
- **Configurable Image Resizing**: Resize images to dimensions suitable for AI models.

## Installation

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

```bash
python radiology_image_preprocessor.py --input_dir ./raw_images --output_dir ./processed_images --width 256 --height 256
```

### Arguments:
- `--input_dir`: Path to the directory containing raw images.
- `--output_dir`: Path to the directory where preprocessed images will be saved.
- `--width`: Width of resized images (default: 256).
- `--height`: Height of resized images (default: 256).

## Example

```bash
python radiology_image_preprocessor.py --input_dir ./raw_images --output_dir ./processed_images
```

## License
MIT License