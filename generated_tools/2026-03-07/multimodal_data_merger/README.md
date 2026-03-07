# Multimodal Data Merger

## Description
This tool preprocesses and merges multimodal data (text, images, audio) into a unified format for AI model training. It allows users to align and normalize their datasets, ensuring consistency across different modalities while supporting common preprocessing operations like tokenization, resizing, and spectrogram generation.

## Installation
Install the required dependencies:

```bash
pip install pandas numpy Pillow librosa
```

## Usage
Run the tool from the command line:

```bash
python multimodal_data_merger.py --text <path_to_text_file> \
                                 --images <path_to_image_directory> \
                                 --audio <path_to_audio_directory> \
                                 --output <path_to_output_file> \
                                 --alignment_key <alignment_key> \
                                 --image_output <image_output_directory> \
                                 --audio_output <audio_output_directory>
```

### Arguments
- `--text`: Path to text metadata file (CSV or JSON).
- `--images`: Path to the directory containing images.
- `--audio`: Path to the directory containing audio files.
- `--output`: Path to save the merged dataset (CSV or JSON).
- `--alignment_key`: Key to align modalities (default: `id`).
- `--image_output`: Directory to save processed images (default: `processed_images`).
- `--audio_output`: Directory to save processed audio (default: `processed_audio`).

## Testing
Run the tests using pytest:

```bash
pytest test_multimodal_data_merger.py
```

## License
MIT License