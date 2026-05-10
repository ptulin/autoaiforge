import cv2
import torch
import pyttsx3
import argparse
import os
import pandas as pd

def load_model(model_name):
    """Load a pre-trained object detection model."""
    try:
        model = torch.hub.load('ultralytics/yolov5', model_name, pretrained=True)
        return model
    except Exception as e:
        raise RuntimeError(f"Error loading model {model_name}: {e}")

def process_frame(frame, model):
    """Process a single video frame to detect objects."""
    try:
        results = model(frame)
        return results.pandas().xyxy[0]  # Return results as a pandas DataFrame
    except Exception as e:
        raise RuntimeError(f"Error processing frame: {e}")

def text_to_speech(text):
    """Convert text to speech using pyttsx3."""
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        raise RuntimeError(f"Error in text-to-speech: {e}")

def process_video(video_source, model_name):
    """Process a video stream or file for object detection and audio feedback."""
    model = load_model(model_name)
    cap = cv2.VideoCapture(video_source)

    if not cap.isOpened():
        raise ValueError(f"Unable to open video source: {video_source}")

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            detections = process_frame(frame, model)

            if isinstance(detections, pd.DataFrame):
                for _, row in detections.iterrows():
                    label = row['name']
                    confidence = row['confidence']
                    if confidence > 0.5:  # Only announce objects with high confidence
                        text_to_speech(f"Detected {label} with confidence {confidence:.2f}")

            # Mocked environment: Skip showing the frame in tests
            if os.getenv("TEST_ENV") != "true":
                cv2.imshow('Smart Glasses AI Bridge', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Smart Glasses AI Bridge")
    parser.add_argument("--video_stream", type=str, required=True, help="Path to video stream or file.")
    parser.add_argument("--model", type=str, default="yolov5s", help="Pre-trained model to use (e.g., yolov5s).")
    args = parser.parse_args()

    try:
        process_video(args.video_stream, args.model)
    except Exception as e:
        print(f"Error: {e}")