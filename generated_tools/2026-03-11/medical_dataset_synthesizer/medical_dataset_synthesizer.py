import argparse
import os
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

def generate_synthetic_image(image_size, disease_intensity):
    """Generate a synthetic medical image with noise and disease simulation."""
    base_image = np.random.normal(loc=128, scale=20, size=(image_size, image_size)).astype(np.uint8)
    disease_mask = np.random.normal(loc=disease_intensity, scale=15, size=(image_size, image_size)).astype(np.uint8)
    synthetic_image = np.clip(base_image + disease_mask, 0, 255).astype(np.uint8)
    return synthetic_image

def save_image(image, output_path):
    """Save a numpy array as an image file."""
    img = Image.fromarray(image)
    img.save(output_path)

def generate_dataset(output_dir, num_images, image_size, disease_intensity):
    """Generate a synthetic dataset of medical images."""
    os.makedirs(output_dir, exist_ok=True)
    annotations = []

    for i in range(num_images):
        image = generate_synthetic_image(image_size, disease_intensity)
        image_filename = f"image_{i + 1}.png"
        image_path = os.path.join(output_dir, image_filename)
        save_image(image, image_path)

        annotation = {
            "image": image_filename,
            "disease_intensity": disease_intensity
        }
        annotations.append(annotation)

    annotation_file = os.path.join(output_dir, "annotations.txt")
    with open(annotation_file, "w") as f:
        for annotation in annotations:
            f.write(f"{annotation}\n")

def main():
    parser = argparse.ArgumentParser(description="Medical Dataset Synthesizer")
    parser.add_argument("--output_dir", type=str, required=True, help="Directory to save the generated dataset")
    parser.add_argument("--num_images", type=int, required=True, help="Number of images to generate")
    parser.add_argument("--image_size", type=int, required=True, help="Size of each image (image_size x image_size)")
    parser.add_argument("--disease_intensity", type=int, default=50, help="Intensity of the disease simulation (default: 50)")

    args = parser.parse_args()

    generate_dataset(
        output_dir=args.output_dir,
        num_images=args.num_images,
        image_size=args.image_size,
        disease_intensity=args.disease_intensity
    )

if __name__ == "__main__":
    main()
