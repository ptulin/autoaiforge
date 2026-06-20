import os
from typing import Dict
from PIL import Image
import exifread

def audit_metadata(image_path: str) -> Dict[str, any]:
    """
    Analyze the metadata of an image to detect anomalies or inconsistencies.

    Args:
        image_path (str): The file path to the image.

    Returns:
        Dict[str, any]: A dictionary containing metadata and any detected anomalies.
    """
    if not os.path.isfile(image_path):
        raise FileNotFoundError(f"File not found: {image_path}")

    metadata = {}
    anomalies = []

    try:
        # Extract EXIF data using exifread
        with open(image_path, 'rb') as img_file:
            exif_data = exifread.process_file(img_file, details=False)

        for tag, value in exif_data.items():
            metadata[tag] = str(value)

        # Analyze metadata for anomalies
        if 'Image Software' in metadata:
            software = metadata['Image Software'].lower()
            if 'ai' in software or 'generated' in software or 'photoshop' in software:
                anomalies.append(f"Potential AI or editing software detected: {software}")

        if 'EXIF DateTimeOriginal' in metadata and 'EXIF DateTimeDigitized' in metadata:
            if metadata['EXIF DateTimeOriginal'] != metadata['EXIF DateTimeDigitized']:
                anomalies.append("Mismatch between original and digitized timestamps.")

        # Check for suspiciously missing metadata
        required_fields = ['Image Make', 'Image Model', 'EXIF DateTimeOriginal']
        for field in required_fields:
            if field not in metadata:
                anomalies.append(f"Missing critical metadata field: {field}")

    except Exception as e:
        return {
            "metadata": {},
            "anomalies": [f"Error processing image: {str(e)}"]
        }

    return {
        "metadata": metadata,
        "anomalies": anomalies
    }

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Image Metadata Auditor")
    parser.add_argument("image_path", type=str, help="Path to the image file to audit")

    args = parser.parse_args()

    try:
        result = audit_metadata(args.image_path)
        print("Metadata:")
        for key, value in result["metadata"].items():
            print(f"  {key}: {value}")

        if result["anomalies"]:
            print("\nAnomalies detected:")
            for anomaly in result["anomalies"]:
                print(f"  - {anomaly}")
        else:
            print("\nNo anomalies detected.")

    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")