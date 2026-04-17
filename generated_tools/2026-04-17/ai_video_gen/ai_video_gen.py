import argparse
import os
import torch
from transformers import pipeline
import imageio

def generate_video(image_path, text_description, duration, output_path, style="default"):
    """
    Generate a short video from an image and text description using an AI model.

    Args:
        image_path (str): Path to the input image file.
        text_description (str): Text description for the video.
        duration (int): Duration of the video in seconds.
        output_path (str): Path to save the generated video.
        style (str): Style of the video (default: "default").

    Returns:
        str: Path to the generated video file.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")

    if duration <= 0:
        raise ValueError("Duration must be a positive integer.")

    # Load the AI model for text-to-video generation
    try:
        video_generator = pipeline("text-to-video", model="damo-vilab/text-to-video-ms-1.7b")
    except Exception as e:
        raise RuntimeError(f"Failed to load the AI model: {e}")

    # Generate the video frames
    try:
        video_frames = video_generator(
            text=text_description,
            init_image=image_path,
            num_frames=duration * 10,  # Assuming 10 frames per second
            style=style
        )
    except Exception as e:
        raise RuntimeError(f"Video generation failed: {e}")

    # Save the video to the specified output path
    try:
        imageio.mimwrite(output_path, video_frames, fps=10, format='mp4')
    except Exception as e:
        raise RuntimeError(f"Failed to save video: {e}")

    return output_path

def main():
    parser = argparse.ArgumentParser(description="AI Video Generator")
    parser.add_argument("--image", required=True, help="Path to the input image file.")
    parser.add_argument("--text", required=True, help="Text description for the video.")
    parser.add_argument("--duration", type=int, default=10, help="Duration of the video in seconds (default: 10).")
    parser.add_argument("--output", required=True, help="Path to save the generated video.")
    parser.add_argument("--style", default="default", help="Style of the video (default: 'default').")

    args = parser.parse_args()

    try:
        result_path = generate_video(
            image_path=args.image,
            text_description=args.text,
            duration=args.duration,
            output_path=args.output,
            style=args.style
        )
        print(f"Video successfully generated and saved to: {result_path}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()