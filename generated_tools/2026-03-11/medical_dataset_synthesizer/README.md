# Medical Dataset Synthesizer

## Description
The Medical Dataset Synthesizer is a Python tool designed to generate synthetic medical datasets for testing AI diagnostic models. It creates realistic image data for diseases like breast cancer based on statistical distributions and noise injection. This tool is valuable for developers needing diverse, non-sensitive training or testing data.

## Features
- Generate synthetic medical images with configurable parameters.
- Simulate disease patterns with adjustable intensity.
- Save images and annotations for AI model training.

## Installation
1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd medical_dataset_synthesizer
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
Run the tool from the command line:
```bash
python medical_dataset_synthesizer.py --output_dir ./synthetic_data --num_images 100 --image_size 256
```

### Arguments
- `--output_dir`: Directory to save the generated dataset.
- `--num_images`: Number of images to generate.
- `--image_size`: Size of each image (image_size x image_size).
- `--disease_intensity`: Intensity of the disease simulation (default: 50).

## Example
Generate 100 synthetic images of size 256x256 with a disease intensity of 50:
```bash
python medical_dataset_synthesizer.py --output_dir ./synthetic_data --num_images 100 --image_size 256 --disease_intensity 50
```

## Testing
Run the tests using pytest:
```bash
pytest test_medical_dataset_synthesizer.py
```

## License
This project is licensed under the MIT License.
