import os
import cv2
import numpy as np
from scipy.ndimage import gaussian_filter
import argparse

def normalize_image(image):
    """Normalize pixel values to range [0, 1]."""
    return image / 255.0

def resize_image(image, width, height):
    """Resize image to specified dimensions."""
    return cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)

def denoise_image(image):
    """Apply Gaussian filter for noise reduction."""
    return gaussian_filter(image, sigma=1)

def preprocess_image(image_path, output_path, width, height):
    """Preprocess a single image."""
    try:
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if image is None:
            raise ValueError(f"Unable to read image: {image_path}")

        image = normalize_image(image)
        image = resize_image(image, width, height)
        image = denoise_image(image)

        cv2.imwrite(output_path, (image * 255).astype(np.uint8))
    except Exception as e:
        print(f"Error processing {image_path}: {e}")

def preprocess_images(input_dir, output_dir, width, height):
    """Preprocess all images in the input directory."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for file_name in os.listdir(input_dir):
        input_path = os.path.join(input_dir, file_name)
        output_path = os.path.join(output_dir, file_name)

        if os.path.isfile(input_path):
            preprocess_image(input_path, output_path, width, height)

def main():
    parser = argparse.ArgumentParser(description="Radiology Image Preprocessor")
    parser.add_argument("--input_dir", required=True, help="Path to input directory containing images")
    parser.add_argument("--output_dir", required=True, help="Path to output directory for preprocessed images")
    parser.add_argument("--width", type=int, default=256, help="Width of resized images")
    parser.add_argument("--height", type=int, default=256, help="Height of resized images")

    args = parser.parse_args()

    preprocess_images(args.input_dir, args.output_dir, args.width, args.height)

if __name__ == "__main__":
    main()