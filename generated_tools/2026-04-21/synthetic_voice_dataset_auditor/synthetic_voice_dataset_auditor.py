import os
import csv
import argparse
from typing import List, Tuple
import soundfile as sf
import tensorflow as tf
from joblib import Parallel, delayed
from tqdm import tqdm

def load_audio(file_path: str) -> Tuple[bool, str]:
    """Load an audio file and return its data and sample rate."""
    try:
        data, samplerate = sf.read(file_path)
        return data, samplerate
    except Exception as e:
        return None, str(e)

def detect_synthetic_voice(audio_data, model, threshold: float) -> float:
    """Run the synthetic voice detection model on the audio data."""
    try:
        # Preprocess audio data for the model
        audio_tensor = tf.convert_to_tensor(audio_data, dtype=tf.float32)
        audio_tensor = tf.expand_dims(audio_tensor, axis=0)

        # Run the model to get a prediction score
        prediction = model(audio_tensor)
        score = float(prediction.numpy()[0][0])
        return score
    except Exception as e:
        return -1.0

def analyze_file(file_path: str, model, threshold: float) -> dict:
    """Analyze a single audio file for synthetic voice detection."""
    audio_data, error = load_audio(file_path)
    if audio_data is None:
        return {"file": file_path, "error": error, "score": None, "is_synthetic": None}

    score = detect_synthetic_voice(audio_data, model, threshold)
    if score == -1.0:
        return {"file": file_path, "error": "Model inference error", "score": None, "is_synthetic": None}

    is_synthetic = score >= threshold
    return {"file": file_path, "error": None, "score": score, "is_synthetic": is_synthetic}

def process_dataset(directory: str, model_path: str, threshold: float, output_file: str):
    """Process an entire dataset of audio files."""
    if not os.path.exists(directory):
        raise FileNotFoundError(f"Directory not found: {directory}")

    # Load the TensorFlow model
    try:
        model = tf.keras.models.load_model(model_path)
    except Exception as e:
        raise RuntimeError(f"Failed to load model: {e}")

    # Collect all audio file paths
    audio_files = [
        os.path.join(directory, f) for f in os.listdir(directory)
        if os.path.isfile(os.path.join(directory, f)) and f.lower().endswith((".wav", ".flac"))
    ]

    if not audio_files:
        raise ValueError("No audio files found in the directory.")

    # Analyze files in parallel
    results = []
    with tqdm(total=len(audio_files), desc="Analyzing files") as pbar:
        results = Parallel(n_jobs=-1)(
            delayed(analyze_file)(file_path, model, threshold) for file_path in audio_files
        )
        pbar.update(len(audio_files))

    # Write results to CSV
    with open(output_file, mode="w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["file", "error", "score", "is_synthetic"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print(f"Analysis complete. Results saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Synthetic Voice Dataset Auditor")
    parser.add_argument("--dataset", required=True, help="Path to the directory containing audio files.")
    parser.add_argument("--model", required=True, help="Path to the trained TensorFlow model.")
    parser.add_argument("--threshold", type=float, default=0.5, help="Detection threshold for synthetic voices (default: 0.5).")
    parser.add_argument("--output", required=True, help="Path to save the CSV report.")

    args = parser.parse_args()

    try:
        process_dataset(args.dataset, args.model, args.threshold, args.output)
    except Exception as e:
        print(f"Error: {e}")