# AI Track Identifier

AI Track Identifier is a command-line tool that analyzes audio tracks to detect characteristics commonly associated with AI-generated music. It evaluates features such as repetitiveness, silence ratio, and dynamic range to provide a confidence score for each analyzed track.

## Features
- Detects AI-generated audio patterns.
- Supports popular audio formats such as MP3 and WAV.
- Outputs a JSON report with confidence scores and analysis details for each track.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-repo/ai_track_identifier.git
    cd ai_track_identifier
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

Run the tool with the following command:

```bash
python ai_track_identifier.py --input track1.mp3 track2.wav --output report.json
```

- `--input`: List of audio file paths to analyze.
- `--output`: Path to the JSON file where the analysis report will be saved.

### Example

```bash
python ai_track_identifier.py --input example1.mp3 example2.wav --output analysis_report.json
```

This will analyze `example1.mp3` and `example2.wav` and save the results to `analysis_report.json`.

## Output

The output is a JSON file containing the analysis results for each input file. Example:

```json
[
    {
        "file": "example1.mp3",
        "confidence_score": 0.75,
        "details": {
            "repetitiveness": 2.5,
            "silence_ratio": 0.1,
            "dynamic_range": 0.8
        }
    },
    {
        "file": "example2.wav",
        "error": "File not found."
    }
]
```

## Testing

To run tests, install `pytest` and run:

```bash
pytest test_ai_track_identifier.py
```

## Limitations
- The tool provides a heuristic-based confidence score and is not a definitive detector of AI-generated music.
- Analysis is limited to simple audio features and may not capture complex patterns.

## License
This project is licensed under the MIT License.