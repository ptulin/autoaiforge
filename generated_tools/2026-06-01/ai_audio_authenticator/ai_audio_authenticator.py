import argparse
import librosa
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import os

def extract_features(audio_path):
    try:
        y, sr = librosa.load(audio_path, sr=None)
        spectral_centroid = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))
        spectral_bandwidth = np.mean(librosa.feature.spectral_bandwidth(y=y, sr=sr))
        spectral_rolloff = np.mean(librosa.feature.spectral_rolloff(y=y, sr=sr))
        zero_crossing_rate = np.mean(librosa.feature.zero_crossing_rate(y))
        return [spectral_centroid, spectral_bandwidth, spectral_rolloff, zero_crossing_rate]
    except Exception as e:
        raise ValueError(f"Error processing audio file {audio_path}: {e}")

def generate_spectrogram(audio_path, output_path):
    try:
        y, sr = librosa.load(audio_path, sr=None)
        plt.figure(figsize=(10, 4))
        S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128, fmax=8000)
        S_dB = librosa.power_to_db(S, ref=np.max)
        librosa.display.specshow(S_dB, sr=sr, x_axis='time', y_axis='mel')
        plt.colorbar(format='%+2.0f dB')
        plt.title('Mel-frequency spectrogram')
        plt.tight_layout()
        plt.savefig(output_path)
        plt.close()
    except Exception as e:
        raise ValueError(f"Error generating spectrogram for {audio_path}: {e}")

def analyze_audio(audio_path, plot=False):
    features = extract_features(audio_path)

    # Simulated model for demonstration purposes
    model = RandomForestClassifier()
    model.fit([[0.1, 0.2, 0.3, 0.4], [0.5, 0.6, 0.7, 0.8]], [0, 1])
    scaler = StandardScaler()
    scaler.fit([[0.1, 0.2, 0.3, 0.4], [0.5, 0.6, 0.7, 0.8]])

    scaled_features = scaler.transform([features])
    confidence = model.predict_proba(scaled_features)[0][1]

    if plot:
        output_path = os.path.splitext(audio_path)[0] + '_spectrogram.png'
        generate_spectrogram(audio_path, output_path)
        print(f"Spectrogram saved to {output_path}")

    return confidence

def main():
    parser = argparse.ArgumentParser(description="AI Audio Authenticity Checker")
    parser.add_argument('--input', required=True, help="Path to the input audio file")
    parser.add_argument('--plot', action='store_true', help="Generate a spectrogram visualization")
    args = parser.parse_args()

    try:
        confidence = analyze_audio(args.input, plot=args.plot)
        print(f"Confidence that the audio is AI-generated: {confidence:.2f}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
