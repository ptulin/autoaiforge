# Smart Glasses AI Bridge

## Overview

The Smart Glasses AI Bridge simplifies the integration of AI models with smart glasses hardware by providing an abstracted interface to process video streams, perform real-time object detection, and send audio feedback to the user. It is highly useful for developers building AI-powered assistive technologies.

## Features

- Load pre-trained object detection models.
- Process video streams or files for real-time object detection.
- Provide audio feedback to users using text-to-speech.

## Installation

Install the required dependencies:

```bash
pip install opencv-python torch pyttsx3 pandas
```

## Usage

Run the tool with the following command:

```bash
python smart_glasses_ai_bridge.py --video_stream <path_to_video> --model <model_name>
```

### Arguments

- `--video_stream`: Path to the video file or stream to process.
- `--model`: Pre-trained model to use for object detection (default: `yolov5s`).

### Example

```bash
python smart_glasses_ai_bridge.py --video_stream video.mp4 --model yolov5s
```

Press `q` to exit the video processing window.

## Testing

Run the tests using `pytest`:

```bash
pytest test_smart_glasses_ai_bridge.py
```

The tests mock external dependencies and do not require network access.

## License

This project is licensed under the MIT License.