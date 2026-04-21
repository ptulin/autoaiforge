# Synthetic Voice Dataset Auditor

## Overview
The Synthetic Voice Dataset Auditor is a Python tool designed to analyze audio datasets for the presence of AI-generated voices. It helps developers clean up datasets or assess their vulnerability to misuse by providing an analysis of synthetic content presence within large collections of audio files.

## Features
- Detects synthetic voices in audio files using a TensorFlow model.
- Processes entire datasets of `.wav` and `.flac` files.
- Outputs results to a CSV file, including detection scores and errors.

## Installation

Install the required dependencies:

```bash
pip install tensorflow soundfile joblib tqdm
```

## Usage

Run the tool from the command line:

```bash
python synthetic_voice_dataset_auditor.py --dataset <path_to_audio_dataset> \
                                          --model <path_to_tensorflow_model> \
                                          --threshold 0.5 \
                                          --output <path_to_output_csv>
```

### Arguments
- `--dataset`: Path to the directory containing audio files.
- `--model`: Path to the trained TensorFlow model.
- `--threshold`: Detection threshold for synthetic voices (default: 0.5).
- `--output`: Path to save the CSV report.

## Testing

Run the tests using `pytest`:

```bash
pytest test_synthetic_voice_dataset_auditor.py
```

The tests include:
- Valid audio file analysis.
- Invalid audio file handling.
- Dataset processing with no audio files.

## License
MIT License