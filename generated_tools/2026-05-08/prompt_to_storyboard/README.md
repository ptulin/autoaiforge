# Prompt to Storyboard Generator

## Description
The Prompt to Storyboard Generator is a command-line tool that takes a text prompt describing a movie scene and generates a storyboard with keyframes and descriptions. It leverages AI text-to-image models to create visual representations of scenes and combines them into a coherent storyboard structure. This tool is perfect for developers and storytellers who want to prototype AI-generated videos more effectively.

## Features
- Converts text prompts into visual storyboard frames.
- Generates scene descriptions alongside images.
- Supports customization of frame count and styles.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd prompt_to_storyboard
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the tool using the following command:

```bash
python prompt_to_storyboard.py --prompt "A spaceship lands on a mysterious planet" --frames 5 --style "cyberpunk"
```

### Arguments:
- `--prompt`: (Required) The text prompt describing the scene.
- `--frames`: (Required) Number of frames to generate.
- `--style`: (Optional) Style of the storyboard (default: "default").
- `--output`: (Optional) Output directory for the storyboard (default: "storyboard_output").

### Example:
```bash
python prompt_to_storyboard.py --prompt "A medieval knight battles a dragon" --frames 4 --style "fantasy" --output "my_storyboard"
```

This will generate 4 frames and a description file in the `my_storyboard` directory.

## Testing

To run the tests, install `pytest` and run:

```bash
pytest test_prompt_to_storyboard.py
```

The tests mock external API calls and verify that the tool generates the expected output.

## Limitations
- The tool requires an OpenAI API key to function properly.
- Internet access is required for generating images via the OpenAI API.

## License
This project is licensed under the MIT License.