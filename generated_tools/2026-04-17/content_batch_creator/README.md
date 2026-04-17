# Content Batch Creator

## Overview
The Content Batch Creator is a Python tool that automates the creation of multiple pieces of video and image content from a spreadsheet of inputs. It uses AI models for text-to-image and text-to-video generation, making it a powerful tool for scaling content production for marketing campaigns.

## Features
- Generate images from text prompts using AI models.
- Generate videos from text prompts with customizable durations.
- Process a CSV file containing multiple prompts and durations to create batches of content.

## Requirements
The tool requires the following Python packages:
- `torch`
- `transformers`
- `pandas`
- `imageio`

You can install these dependencies using pip:
```bash
pip install torch transformers pandas imageio
```

## Usage
Run the tool from the command line with the following arguments:

```bash
python content_batch_creator.py --input <path_to_input_csv> --output_folder <path_to_output_folder>
```

### Arguments
- `--input`: Path to the input CSV file. The CSV file must contain the following columns:
  - `text_prompt`: The text prompt for generating content.
  - `video_duration`: The duration of the generated video in seconds (default is 5 seconds if not provided).
- `--output_folder`: Path to the folder where the generated content will be saved.

### Example
1. Create an input CSV file named `input.csv` with the following content:

```csv
text_prompt,video_duration
A beautiful sunset,5
A futuristic city,10
```

2. Run the tool:

```bash
python content_batch_creator.py --input input.csv --output_folder output
```

3. The generated images and videos will be saved in the `output` folder.

## Testing
The tool includes a test suite written with `pytest`. To run the tests, install `pytest`:

```bash
pip install pytest
```

Then run the tests:

```bash
pytest test_content_batch_creator.py
```

The tests include:
- Verifying that the tool generates the expected files for valid input.
- Ensuring the tool handles empty CSV files gracefully.
- Checking that the tool raises an error for missing required columns in the input CSV.

## Notes
- The tool uses the `transformers` library for AI-based content generation. Ensure you have the necessary models downloaded and available.
- The tool is designed to handle errors gracefully, such as missing or empty input files.

## License
This project is licensed under the MIT License.
