import argparse
import os
import json
import pandas as pd
import numpy as np
from PIL import Image
import librosa

def preprocess_text(text_file):
    """Load and preprocess text metadata from a CSV or JSON file."""
    if text_file.endswith('.csv'):
        return pd.read_csv(text_file)
    elif text_file.endswith('.json'):
        return pd.read_json(text_file)
    else:
        raise ValueError("Unsupported text file format. Use CSV or JSON.")

def preprocess_images(image_dir, output_dir):
    """Resize images and save them to the output directory."""
    os.makedirs(output_dir, exist_ok=True)
    processed_images = {}

    for image_file in os.listdir(image_dir):
        if image_file.lower().endswith(('png', 'jpg', 'jpeg')):
            img_path = os.path.join(image_dir, image_file)
            try:
                img = Image.open(img_path).convert('RGB')
                img_resized = img.resize((224, 224))
                output_path = os.path.join(output_dir, image_file)
                img_resized.save(output_path)
                processed_images[image_file] = output_path
            except Exception as e:
                print(f"Error processing image {image_file}: {e}")
    return processed_images

def preprocess_audio(audio_dir, output_dir):
    """Convert audio files to spectrograms and save them to the output directory."""
    os.makedirs(output_dir, exist_ok=True)
    processed_audio = {}

    for audio_file in os.listdir(audio_dir):
        if audio_file.lower().endswith(('wav', 'mp3')):
            audio_path = os.path.join(audio_dir, audio_file)
            try:
                y, sr = librosa.load(audio_path, sr=None)
                spectrogram = librosa.feature.melspectrogram(y=y, sr=sr)
                spectrogram_path = os.path.join(output_dir, f"{os.path.splitext(audio_file)[0]}.npy")
                np.save(spectrogram_path, spectrogram)
                processed_audio[audio_file] = spectrogram_path
            except Exception as e:
                print(f"Error processing audio {audio_file}: {e}")
    return processed_audio

def merge_data(text_data, images_data, audio_data, alignment_key):
    """Merge text, image, and audio data into a unified dataset."""
    merged_data = []

    for _, row in text_data.iterrows():
        key = row[alignment_key]
        entry = {
            'text': row.to_dict(),
            'image': images_data.get(key, None),
            'audio': audio_data.get(key, None)
        }
        merged_data.append(entry)

    return merged_data

def main():
    parser = argparse.ArgumentParser(description="Multimodal Data Merger")
    parser.add_argument('--text', required=True, help="Path to text metadata (CSV/JSON)")
    parser.add_argument('--images', required=True, help="Path to image directory")
    parser.add_argument('--audio', required=True, help="Path to audio directory")
    parser.add_argument('--output', required=True, help="Path to output merged dataset (CSV/JSON)")
    parser.add_argument('--alignment_key', default='id', help="Key to align modalities (default: 'id')")
    parser.add_argument('--image_output', default='processed_images', help="Directory to save processed images")
    parser.add_argument('--audio_output', default='processed_audio', help="Directory to save processed audio")

    args = parser.parse_args()

    # Preprocess each modality
    text_data = preprocess_text(args.text)
    images_data = preprocess_images(args.images, args.image_output)
    audio_data = preprocess_audio(args.audio, args.audio_output)

    # Merge data
    merged_data = merge_data(text_data, images_data, audio_data, args.alignment_key)

    # Save merged dataset
    if args.output.endswith('.csv'):
        pd.DataFrame(merged_data).to_csv(args.output, index=False)
    elif args.output.endswith('.json'):
        with open(args.output, 'w') as f:
            json.dump(merged_data, f, indent=4)
    else:
        raise ValueError("Unsupported output file format. Use CSV or JSON.")

if __name__ == "__main__":
    main()