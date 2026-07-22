# AI Storyboard Generator

## Overview
The AI Storyboard Generator automates the creation of visual storyboards for film or animation projects. It takes a text-based script as input and uses AI to generate visual concept art for each scene, along with optional scene descriptions and camera direction notes. The output can be saved as a PDF storyboard or as individual image files.

## Features
- Parse a script file into individual scenes.
- Generate AI-powered images for each scene based on the script and a specified style.
- Create a PDF storyboard with images and descriptions.

## Installation
1. Install Python 3.8 or later.
2. Install the required packages:
   ```bash
   pip install Pillow reportlab openai
   ```

## Usage
Run the script from the command line:
```bash
python ai_storyboard_generator.py --script <script_path> --style <image_style> --output <output_path>
```

### Arguments
- `--script`: Path to the text script file.
- `--style`: Image style (e.g., watercolor, sketch). Default is `realistic`.
- `--output`: Output file path (PDF or directory for images).

## Testing
Run the tests using `pytest`:
```bash
pytest test_ai_storyboard_generator.py
```

## Notes
- Ensure you have an OpenAI API key set up in your environment to use the image generation feature.
- The tool handles edge cases such as missing files, network errors, and empty input gracefully.
