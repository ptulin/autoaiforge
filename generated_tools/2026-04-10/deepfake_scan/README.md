# Deepfake Video and Image Scanner

Deepfake Scan is a command-line tool designed to help users detect potential deepfake content in videos and images. Using advanced AI models, it provides a confidence score for detection and generates visual heatmaps highlighting suspicious areas in the media files. This tool is particularly useful for researchers, journalists, and developers working to combat misinformation and manipulated media.

## Features

- Analyze videos and images for potential deepfake content.
- Generate a confidence score indicating the likelihood of manipulation.
- Create visual heatmaps to highlight suspicious regions in the media.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/deepfake_scan.git
   cd deepfake_scan
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

To use the Deepfake Video and Image Scanner, run the following command:

```bash
python deepfake_scan.py --input <path_to_media_file> [--output <path_to_heatmap_output>]
```

### Examples

1. Analyze an image for deepfake content:
   ```bash
   python deepfake_scan.py --input image.jpg
   ```

2. Analyze a video and save the heatmap:
   ```bash
   python deepfake_scan.py --input video.mp4 --output heatmap.png
   ```

## Requirements

- Python 3.8+
- torch==2.0.1
- opencv-python==4.8.0.74
- numpy==1.23.5
- matplotlib==3.7.2

## Limitations

- This tool uses a simulated deepfake detection model for demonstration purposes. It does not perform actual deepfake detection.
- The tool processes only the first frame of a video for simplicity.

## License

This project is licensed under the MIT License. See the LICENSE file for details.