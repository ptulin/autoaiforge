# Synthetic Data Generator

Synthetic Data Generator is a Python library for creating high-quality synthetic datasets for AI tasks, such as image classification or text processing. It uses preconfigured templates of data generation (e.g., random images with labels or simulated text) and integrates augmentation options, helping.

## Features

- Generate synthetic image datasets with optional augmentation.
- Generate synthetic text datasets with optional augmentation.
- Configurable parameters for dataset size, image dimensions, and text length.

## Installation

Install the required dependencies:

```bash
pip install numpy Pillow
```

## Usage

Run the script with the following options:

```bash
python synthetic_data_generator.py --type [image|text] --num_samples <number> --augment --image_size <width height> --sentence_length <number> --output_dir <directory>
```

### Examples

Generate 100 synthetic images:

```bash
python synthetic_data_generator.py --type image --num_samples 100 --image_size 128 128 --output_dir synthetic_images
```

Generate 50 synthetic text samples with augmentation:

```bash
python synthetic_data_generator.py --type text --num_samples 50 --sentence_length 10 --augment
```

## Testing

Run tests using pytest:

```bash
pytest test_synthetic_data_generator.py
```

All tests are self-contained and do not require network access.

## License

This project is licensed under the MIT License.