import argparse
import logging
import os
from pathlib import Path
from typing import Any, Dict

from PIL import Image
import torch
from transformers import pipeline
import librosa
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MultiModalModelRouter")

def detect_content_type(file_path: str) -> str:
    """Detect the content type of the input file."""
    try:
        ext = Path(file_path).suffix.lower()
        if ext in ['.jpg', '.jpeg', '.png', '.bmp']:
            return 'image'
        elif ext in ['.wav', '.mp3', '.flac']:
            return 'audio'
        elif ext in ['.txt', '.csv', '.json']:
            return 'text'
        else:
            raise ValueError(f"Unsupported file type: {ext}")
    except Exception as e:
        logger.error(f"Error detecting content type: {e}")
        raise

def process_text(file_path: str) -> str:
    """Process text input using a text-based AI model."""
    try:
        with open(file_path, 'r') as f:
            text = f.read()
        model = pipeline("text-generation", model="gpt2")
        result = model(text, max_length=50, num_return_sequences=1)
        return result[0]['generated_text']
    except Exception as e:
        logger.error(f"Error processing text: {e}")
        raise

def process_image(file_path: str) -> str:
    """Process image input using an image-based AI model."""
    try:
        image = Image.open(file_path)
        model = pipeline("image-classification")
        result = model(image)
        return str(result)
    except Exception as e:
        logger.error(f"Error processing image: {e}")
        raise

def process_audio(file_path: str) -> str:
    """Process audio input using an audio-based AI model."""
    try:
        audio, sr = librosa.load(file_path, sr=None)
        duration = librosa.get_duration(y=np.array(audio), sr=sr)
        return f"Audio file duration: {duration:.2f} seconds"
    except Exception as e:
        logger.error(f"Error processing audio: {e}")
        raise

def route_input(file_path: str, content_type: str) -> str:
    """Route the input file to the appropriate model based on content type."""
    if content_type == 'text':
        return process_text(file_path)
    elif content_type == 'image':
        return process_image(file_path)
    elif content_type == 'audio':
        return process_audio(file_path)
    else:
        raise ValueError(f"Unsupported content type: {content_type}")

def main():
    parser = argparse.ArgumentParser(
        description="Multi-Modal Model Router: Route input data to appropriate AI models."
    )
    parser.add_argument('--input_file', required=True, help="Path to the input file.")
    parser.add_argument('--content_type', choices=['text', 'image', 'audio'],
                        help="Specify the content type (text, image, audio). If not provided, it will be auto-detected.")
    parser.add_argument('--debug', action='store_true', help="Enable debug mode.")

    args = parser.parse_args()

    if args.debug:
        logger.setLevel(logging.DEBUG)

    input_file = args.input_file
    if not os.path.exists(input_file):
        logger.error(f"Input file does not exist: {input_file}")
        return

    try:
        content_type = args.content_type or detect_content_type(input_file)
        logger.info(f"Detected content type: {content_type}")

        result = route_input(input_file, content_type)
        print(f"Processed output: {result}")
    except Exception as e:
        logger.error(f"Error: {e}")

if __name__ == "__main__":
    main()
