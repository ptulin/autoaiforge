# AI Video Captioner

## Description
AI Video Captioner is a Python-based tool that uses AI to automatically generate captions for video files by transcribing audio and optionally translating captions into multiple languages. This tool is useful for content creators looking to make their videos more accessible and reach a global audience.

## Features
- Extract audio from video files.
- Transcribe audio to text using OpenAI's Whisper API.
- Translate captions into multiple languages using OpenAI's GPT model.
- Save captions in `.srt` or `.vtt` formats.

## Installation

1. Clone this repository:
   ```bash
   git clone <repository_url>
   cd ai_video_captioner
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the script with the following arguments:

```bash
python ai_video_captioner.py --video <path_to_video> --output <path_to_output_file> [--lang <comma_separated_language_codes>] [--format <srt|vtt>]
```

### Arguments
- `--video`: Path to the input video file (required).
- `--output`: Path to the output caption file (required).
- `--lang`: Comma-separated list of language codes for translation (optional).
- `--format`: Output caption format, either `srt` or `vtt` (default: `srt`).

### Example

To generate English captions for a video:

```bash
python ai_video_captioner.py --video input.mp4 --output captions.srt
```

To generate captions in English and Spanish:

```bash
python ai_video_captioner.py --video input.mp4 --output captions.srt --lang es
```

## Testing

To run the tests, use `pytest`:

```bash
pytest test_ai_video_captioner.py
```

## Requirements

- Python 3.7+
- ffmpeg-python
- openai
- pytest

Install the dependencies using the provided `requirements.txt` file.

## License

This project is licensed under the MIT License.