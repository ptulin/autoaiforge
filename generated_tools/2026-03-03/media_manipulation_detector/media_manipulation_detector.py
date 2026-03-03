import cv2
import numpy as np
import argparse
import json

def detect_fake_media(file_path, output):
    """
    Detects possible signs of manipulation in images or videos.

    Args:
        file_path (str): Path to the input image or video file.
        output (str): Path to the output JSON file to save results.

    Returns:
        dict: Metadata about detected anomalies.
    """
    if not file_path:
        raise ValueError("Input file path must be provided.")

    try:
        # Determine if the file is an image or video
        file_type = 'image' if file_path.lower().endswith(('jpg', 'jpeg', 'png')) else 'video'

        results = {
            "file_path": file_path,
            "file_type": file_type,
            "anomalies_detected": False,
            "details": []
        }

        if file_type == 'image':
            image = cv2.imread(file_path)
            if image is None:
                raise FileNotFoundError("Image file not found or cannot be read.")

            # Placeholder analysis: Detect anomalies in the image
            anomalies = analyze_image(image)
            results["anomalies_detected"] = bool(anomalies)
            results["details"] = anomalies

        elif file_type == 'video':
            cap = cv2.VideoCapture(file_path)
            if not cap.isOpened():
                raise FileNotFoundError("Video file not found or cannot be read.")

            anomalies = analyze_video(cap)
            results["anomalies_detected"] = bool(anomalies)
            results["details"] = anomalies

            cap.release()

        # Save results to JSON file
        with open(output, 'w') as f:
            json.dump(results, f, indent=4)

        return results

    except FileNotFoundError as e:
        raise e
    except Exception as e:
        raise RuntimeError(f"Error processing file: {e}")

def analyze_image(image):
    """
    Analyze an image for anomalies.

    Args:
        image (np.ndarray): Image array.

    Returns:
        list: List of detected anomalies.
    """
    anomalies = []
    try:
        if len(image.shape) < 3 or image.shape[2] != 3:
            raise ValueError("Invalid image format. Expected a 3-channel color image.")

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 100, 200)

        if np.sum(edges) > 10000:  # Arbitrary threshold for edge detection
            anomalies.append("High edge density detected, possible manipulation.")
    except Exception as e:
        raise RuntimeError(f"Error analyzing image: {e}")

    return anomalies

def analyze_video(cap):
    """
    Analyze a video for anomalies.

    Args:
        cap (cv2.VideoCapture): Video capture object.

    Returns:
        list: List of detected anomalies.
    """
    anomalies = []
    frame_count = 0

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame_count += 1
            if len(frame.shape) < 3 or frame.shape[2] != 3:
                raise ValueError("Invalid frame format. Expected a 3-channel color frame.")

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 100, 200)

            if np.sum(edges) > 10000:  # Arbitrary threshold for edge detection
                anomalies.append(f"Frame {frame_count}: High edge density detected, possible manipulation.")
    except Exception as e:
        raise RuntimeError(f"Error analyzing video: {e}")

    return anomalies

def main():
    parser = argparse.ArgumentParser(description="Media Manipulation Detector")
    parser.add_argument("file_path", type=str, help="Path to the input image or video file.")
    parser.add_argument("output", type=str, help="Path to the output JSON file.")

    args = parser.parse_args()

    try:
        results = detect_fake_media(args.file_path, args.output)
        print("Detection completed. Results saved to:", args.output)
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
