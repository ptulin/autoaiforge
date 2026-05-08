import os
import argparse
from PIL import Image, ImageDraw, ImageFont
import openai

def generate_storyboard(prompt, frames, style, output_dir):
    """
    Generate a storyboard based on a text prompt.

    Args:
        prompt (str): The text prompt describing the scene.
        frames (int): Number of frames to generate.
        style (str): The style of the storyboard (e.g., 'cyberpunk').
        output_dir (str): Directory to save the storyboard frames and descriptions.

    Returns:
        str: Path to the output directory containing the storyboard.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    descriptions = []

    for i in range(frames):
        frame_prompt = f"{prompt}, frame {i + 1} in {style} style"
        try:
            response = openai.Image.create(prompt=frame_prompt, n=1, size="256x256")
            image_url = response['data'][0]['url']

            # Mock downloading the image (replace with actual download code if needed)
            image = Image.new('RGB', (256, 256), color=(73, 109, 137))
            draw = ImageDraw.Draw(image)
            draw.text((10, 10), f"Frame {i + 1}", fill="white")

            image_path = os.path.join(output_dir, f"frame_{i + 1}.png")
            image.save(image_path)
            descriptions.append(f"Frame {i + 1}: {frame_prompt}")
        except Exception as e:
            print(f"Error generating frame {i + 1}: {e}")

    description_file = os.path.join(output_dir, "descriptions.txt")
    with open(description_file, "w") as f:
        f.write("\n".join(descriptions))

    return output_dir

def main():
    parser = argparse.ArgumentParser(description="Prompt to Storyboard Generator")
    parser.add_argument('--prompt', required=True, help='Text prompt describing the scene')
    parser.add_argument('--frames', type=int, required=True, help='Number of frames to generate')
    parser.add_argument('--style', default='default', help='Style of the storyboard (e.g., cyberpunk)')
    parser.add_argument('--output', default='storyboard_output', help='Output directory for the storyboard')

    args = parser.parse_args()

    output_dir = generate_storyboard(args.prompt, args.frames, args.style, args.output)
    print(f"Storyboard generated in: {output_dir}")

if __name__ == "__main__":
    main()