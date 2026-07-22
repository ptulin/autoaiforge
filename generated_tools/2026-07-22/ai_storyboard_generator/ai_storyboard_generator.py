import argparse
import os
from PIL import Image, ImageDraw, ImageFont
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import openai
from urllib.request import urlretrieve

def parse_script(script_path):
    """
    Parse the script file into a list of scenes.
    Each scene is separated by a blank line.
    """
    if not os.path.exists(script_path):
        raise FileNotFoundError(f"Script file not found: {script_path}")

    with open(script_path, 'r') as file:
        content = file.read()

    scenes = [scene.strip() for scene in content.split('\n\n') if scene.strip()]
    return scenes

def generate_image(prompt, style):
    """
    Generate an image using OpenAI's API based on the prompt and style.
    """
    try:
        response = openai.Image.create(
            prompt=f"{prompt}, style: {style}",
            n=1,
            size="512x512"
        )
        image_url = response['data'][0]['url']
        return image_url
    except Exception as e:
        raise RuntimeError(f"Failed to generate image: {e}")

def download_image(image_url, output_path):
    """
    Download the image from the URL and save it locally.
    """
    try:
        urlretrieve(image_url, output_path)
    except Exception as e:
        raise RuntimeError(f"Failed to download image: {e}")

def create_pdf(output_path, images, descriptions):
    """
    Create a PDF storyboard from the given images and descriptions.
    """
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter

    for img_path, desc in zip(images, descriptions):
        if os.path.exists(img_path):
            c.drawImage(img_path, 50, height / 2 - 256, width=512, height=512)
        c.drawString(50, height / 2 - 276, desc)
        c.showPage()

    c.save()

def main():
    parser = argparse.ArgumentParser(description="AI Storyboard Generator")
    parser.add_argument('--script', required=True, help="Path to the text script file")
    parser.add_argument('--style', default='realistic', help="Image style (e.g., watercolor, sketch)")
    parser.add_argument('--output', required=True, help="Output file path (PDF or directory for images)")

    args = parser.parse_args()

    # Parse the script
    try:
        scenes = parse_script(args.script)
    except Exception as e:
        print(f"Error parsing script: {e}")
        return

    # Generate images and descriptions
    images = []
    descriptions = []

    for i, scene in enumerate(scenes):
        print(f"Processing scene {i + 1}/{len(scenes)}: {scene[:30]}...")
        try:
            image_url = generate_image(scene, args.style)
            image_path = f"scene_{i + 1}.png"
            download_image(image_url, image_path)
            images.append(image_path)
            descriptions.append(scene)
        except Exception as e:
            print(f"Error generating image for scene {i + 1}: {e}")

    # Generate output
    if args.output.endswith('.pdf'):
        try:
            create_pdf(args.output, images, descriptions)
            print(f"Storyboard PDF created: {args.output}")
        except Exception as e:
            print(f"Error creating PDF: {e}")
    else:
        print("Images saved locally.")

if __name__ == "__main__":
    main()
