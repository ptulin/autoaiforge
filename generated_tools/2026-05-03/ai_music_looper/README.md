# AI Music Looper

AI Music Looper is a command-line tool that analyzes music files, identifies repetitive patterns, and suggests seamless loop points. This tool is ideal for music producers and video editors who need perfectly looping audio tracks for their projects.

## Features
- Analyze music files for repeating patterns.
- Identify seamless loop points.
- Option to preview suggested loop points.

## Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd ai_music_looper
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the tool from the command line:

```bash
python ai_music_looper.py --input path/to/your/music/file.mp3
```

To preview the suggested loop points:

```bash
python ai_music_looper.py --input path/to/your/music/file.mp3 --preview
```

## Example

```bash
python ai_music_looper.py --input track.mp3 --preview
```

Output:
```
Suggested loop points:
Start: 0.00s, End: 1.00s
Start: 1.00s, End: 2.00s
...
Previewing loops for file: track.mp3
Loop from 0.00s to 1.00s
Loop from 1.00s to 2.00s
...
```

## Requirements
- Python 3.7+
- librosa==0.10.0
- numpy==1.26.0

## License
This project is licensed under the MIT License.