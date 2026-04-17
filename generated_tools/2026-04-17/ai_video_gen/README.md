# AI Video Generator

## Overview
The AI Video Generator tool allows users to create short, engaging, ad-ready videos using an input image and a text description. It leverages Hugging Face's text-to-video/generative video models to generate videos, making it a powerful tool for marketers and developers to quickly prototype video content for campaigns.

## Features
- Generate videos from an image and a text description.
- Specify the duration and style of the video.
- Save the generated video to a specified output path.

## Requirements
- Python 3.7+
- Required Python packages:
  - `torch`
  - `transformers`
  - `imageio`

Install the required packages using pip:
```bash
pip install torch transformers imageio
```

## Usage
Run the script from the command line with the following arguments:

```bash
python ai_video_gen.py --image <path_to_image> --text <text_description> --duration <duration_in_seconds> --output <output_path> [--style <video_style>]
```

### Arguments
- `--image`: Path to the input image file (required).
- `--text`: Text description for the video (required).
- `--duration`: Duration of the video in seconds (default: 10).
- `--output`: Path to save the generated video (required).
- `--style`: Style of the video (default: "default").

### Example
```bash
python ai_video_gen.py --image "input.jpg" --text "A serene beach at sunset" --duration 5 --output "output.mp4" --style "default"
```

## Testing
The tool includes a test suite using `pytest`. To run the tests, install `pytest` and execute:

```bash
pip install pytest
pytest test_ai_video_gen.py
```

The tests cover the following scenarios:
1. Successful video generation.
2. Handling of missing input image files.
3. Validation of invalid duration values.

## Notes
- This tool requires access to the internet to load the AI model from Hugging Face.
- Ensure that the input image file exists and is accessible.
- The output video will be saved in MP4 format.
