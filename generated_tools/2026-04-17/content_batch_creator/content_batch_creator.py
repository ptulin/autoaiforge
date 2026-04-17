import os
import argparse
import pandas as pd
import torch
from transformers import pipeline
import imageio

def generate_image(prompt, output_path):
    generator = pipeline("text-to-image", model="CompVis/stable-diffusion-v1-4")
    image = generator(prompt)[0]["sample"]
    image.save(output_path)

def generate_video(prompt, duration, output_path):
    generator = pipeline("text-to-video", model="damo-vilab/text-to-video-ms-1.7b")
    frames = generator(prompt, num_frames=int(duration * 10))
    with imageio.get_writer(output_path, mode='I', fps=10) as writer:
        for frame in frames:
            writer.append_data(frame)

def process_csv(input_csv, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    try:
        df = pd.read_csv(input_csv)
    except pd.errors.EmptyDataError:
        print("Input CSV is empty. No data to process.")
        return

    required_columns = {'text_prompt', 'video_duration'}
    if not required_columns.issubset(df.columns):
        raise KeyError(f"Input CSV must contain the following columns: {required_columns}")

    for index, row in df.iterrows():
        prompt = row.get('text_prompt', '').strip()
        image_path = os.path.join(output_folder, f"image_{index}.png")
        video_path = os.path.join(output_folder, f"video_{index}.mp4")
        duration = row.get('video_duration', 5)  # Default to 5 seconds

        if prompt:
            generate_image(prompt, image_path)
            generate_video(prompt, duration, video_path)

def main():
    parser = argparse.ArgumentParser(description="Content Batch Creator")
    parser.add_argument('--input', required=True, help="Path to input CSV file")
    parser.add_argument('--output_folder', required=True, help="Path to output folder")
    args = parser.parse_args()

    try:
        process_csv(args.input, args.output_folder)
    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    main()
