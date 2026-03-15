import os
import numpy as np
from PIL import Image, ImageEnhance
import random
import string

def generate_image_data(num_samples=100, image_size=(128, 128), augment=False, output_dir="synthetic_images"):
    """
    Generate synthetic image data with optional augmentation.

    Args:
        num_samples (int): Number of images to generate.
        image_size (tuple): Size of each image (width, height).
        augment (bool): Whether to apply random augmentations.
        output_dir (str): Directory to save generated images.

    Returns:
        list: List of generated image file paths.
        list: List of corresponding labels.
    """
    os.makedirs(output_dir, exist_ok=True)
    image_paths = []
    labels = []

    for i in range(num_samples):
        # Create a random image
        image_array = np.random.randint(0, 256, (image_size[1], image_size[0], 3), dtype=np.uint8)
        image = Image.fromarray(image_array)

        # Apply augmentation if enabled
        if augment:
            enhancer = ImageEnhance.Brightness(image)
            image = enhancer.enhance(random.uniform(0.5, 1.5))

        # Save the image
        label = f"class_{random.randint(0, 9)}"
        filename = f"{label}_{i}.png"
        file_path = os.path.join(output_dir, filename)
        image.save(file_path)

        image_paths.append(file_path)
        labels.append(label)

    return image_paths, labels

def generate_text_data(num_samples=100, sentence_length=10, augment=False):
    """
    Generate synthetic text data with optional augmentation.

    Args:
        num_samples (int): Number of text samples to generate.
        sentence_length (int): Number of words in each sentence.
        augment (bool): Whether to apply random augmentations.

    Returns:
        list: List of generated text samples.
        list: List of corresponding labels.
    """
    # Mocked word list for testing purposes
    words = ["word1", "word2", "word3", "word4", "word5"]
    text_samples = []
    labels = []

    for _ in range(num_samples):
        sentence = " ".join(random.choices(words, k=sentence_length))

        # Apply augmentation if enabled
        if augment:
            sentence = sentence.lower() if random.random() > 0.5 else sentence.upper()

        label = "positive" if random.random() > 0.5 else "negative"
        text_samples.append(sentence)
        labels.append(label)

    return text_samples, labels

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Synthetic Data Generator for AI")
    parser.add_argument("--type", choices=["image", "text"], required=True, help="Type of dataset to generate.")
    parser.add_argument("--num_samples", type=int, default=100, help="Number of samples to generate.")
    parser.add_argument("--augment", action="store_true", help="Enable data augmentation.")
    parser.add_argument("--image_size", type=int, nargs=2, default=(128, 128), help="Size of images (width height).")
    parser.add_argument("--sentence_length", type=int, default=10, help="Number of words in each text sample.")
    parser.add_argument("--output_dir", type=str, default="synthetic_data", help="Output directory for generated data.")

    args = parser.parse_args()

    if args.type == "image":
        generate_image_data(
            num_samples=args.num_samples,
            image_size=tuple(args.image_size),
            augment=args.augment,
            output_dir=args.output_dir
        )
    elif args.type == "text":
        generate_text_data(
            num_samples=args.num_samples,
            sentence_length=args.sentence_length,
            augment=args.augment
        )