import argparse
import json
import os
from pydub import AudioSegment
import numpy as np
from scipy.stats import kurtosis

def analyze_audio(file_path):
    """
    Analyze an audio file to detect characteristics of AI-generated music.

    Parameters:
        file_path (str): Path to the audio file.

    Returns:
        dict: A dictionary containing the confidence score and analysis details.
    """
    try:
        audio = AudioSegment.from_file(file_path)
        samples = np.array(audio.get_array_of_samples())

        # Normalize samples
        samples = samples / np.max(np.abs(samples))

        # Feature 1: Repetitiveness (measured via kurtosis)
        repetitiveness = kurtosis(samples)

        # Feature 2: Silence ratio
        silence_threshold = 0.01
        silence_ratio = np.mean(np.abs(samples) < silence_threshold)

        # Feature 3: Dynamic range (difference between max and min amplitude)
        dynamic_range = np.max(samples) - np.min(samples)

        # Combine features into a confidence score (simplified example)
        confidence_score = min(1.0, max(0.0, (repetitiveness + silence_ratio - dynamic_range) / 3))

        return {
            "file": file_path,
            "confidence_score": confidence_score,
            "details": {
                "repetitiveness": repetitiveness,
                "silence_ratio": silence_ratio,
                "dynamic_range": dynamic_range
            }
        }

    except Exception as e:
        return {
            "file": file_path,
            "error": str(e)
        }

def main():
    parser = argparse.ArgumentParser(description="AI Track Identifier: Detect AI-generated audio patterns.")
    parser.add_argument("--input", nargs="+", required=True, help="Paths to input audio files.")
    parser.add_argument("--output", required=True, help="Path to output JSON report.")
    args = parser.parse_args()

    input_files = args.input
    output_file = args.output

    if not input_files:
        print("Error: No input files provided.")
        return

    results = []

    for file_path in input_files:
        if not os.path.isfile(file_path):
            results.append({"file": file_path, "error": "File not found."})
            continue

        result = analyze_audio(file_path)
        results.append(result)

    try:
        with open(output_file, "w") as f:
            json.dump(results, f, indent=4)
        print(f"Analysis complete. Results saved to {output_file}")
    except Exception as e:
        print(f"Error writing output file: {e}")

if __name__ == "__main__":
    main()