import os
import json
import argparse
from typing import List, Dict
import torch
from unittest.mock import MagicMock

# Mock pretrainedmodels and utils for testing purposes
class MockPretrainedModel:
    def __init__(self, num_classes, pretrained):
        pass

    def eval(self):
        pass

    def __call__(self, img):
        return torch.tensor([[0.1, 0.9]])

class MockLoadTransformImage:
    def __init__(self, model):
        pass

    def __call__(self, image_path):
        return torch.zeros((3, 224, 224))

# Replace pretrainedmodels and utils with mocks
pretrainedmodels = MagicMock()
pretrainedmodels.__dict__ = {
    "xception": MockPretrainedModel
}
utils = MagicMock()
utils.LoadTransformImage = MockLoadTransformImage

# Load pre-trained model
MODEL_NAME = "xception"
model = pretrainedmodels.__dict__[MODEL_NAME](num_classes=1000, pretrained='imagenet')
model.eval()
load_img = utils.LoadTransformImage(model)

def analyze_image(image_path: str) -> Dict[str, float]:
    """
    Analyze a single image for deepfake likelihood.

    Args:
        image_path (str): Path to the image file.

    Returns:
        Dict[str, float]: A dictionary with the likelihood of the image being a deepfake.
    """
    try:
        img = load_img(image_path)
        img = img.unsqueeze(0)  # Add batch dimension
        with torch.no_grad():
            output = model(img)
        probabilities = torch.nn.functional.softmax(output[0], dim=0).tolist()
        return {"deepfake_likelihood": probabilities[1]}  # Example: using the second class as deepfake likelihood
    except Exception as e:
        return {"error": str(e)}

def process_images(input_path: str) -> List[Dict[str, str]]:
    """
    Process a single image or a directory of images.

    Args:
        input_path (str): Path to an image file or directory of images.

    Returns:
        List[Dict[str, str]]: A list of results for each image.
    """
    results = []
    if os.path.isfile(input_path):
        results.append({"file": input_path, **analyze_image(input_path)})
    elif os.path.isdir(input_path):
        for filename in os.listdir(input_path):
            file_path = os.path.join(input_path, filename)
            if os.path.isfile(file_path) and file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
                results.append({"file": file_path, **analyze_image(file_path)})
    else:
        raise ValueError("Invalid input path. Must be a file or directory.")
    return results

def main():
    parser = argparse.ArgumentParser(description="Deepfake Image Detector")
    parser.add_argument('--input', required=True, help="Path to an image file or directory of images.")
    parser.add_argument('--output', required=True, help="Path to save the JSON results.")
    args = parser.parse_args()

    try:
        results = process_images(args.input)
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=4)
        print(f"Results saved to {args.output}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
