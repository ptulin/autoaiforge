import argparse
import requests
import openai
import os
from dotenv import load_dotenv

def export_figma_elements(file_id, access_token):
    """Export design elements from Figma file."""
    url = f"https://api.figma.com/v1/files/{file_id}"
    headers = {"Authorization": f"Bearer {access_token}"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to fetch Figma file: {e}")

def optimize_design_with_ai(design_elements, optimize_layout):
    """Use AI to optimize design elements."""
    try:
        prompt = "Optimize the following design elements for better layout and style: " + str(design_elements)
        if optimize_layout:
            prompt += " Focus on optimizing the layout."
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=1000
        )
        return response.choices[0].text.strip()
    except openai.error.OpenAIError as e:
        raise RuntimeError(f"Failed to optimize design with AI: {e}")

def update_figma_file(file_id, access_token, optimized_elements):
    """Update Figma file with optimized design elements."""
    url = f"https://api.figma.com/v1/files/{file_id}/comments"
    headers = {"Authorization": f"Bearer {access_token}"}
    data = {"message": "Updated design elements:", "client_meta": optimized_elements}
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to update Figma file: {e}")

def main():
    load_dotenv()

    parser = argparse.ArgumentParser(description="Figma AI Sync Tool")
    parser.add_argument("--file-id", required=True, help="Figma file ID")
    parser.add_argument("--access-token", required=True, help="Figma API access token")
    parser.add_argument("--optimize-layout", action="store_true", help="Optimize layout using AI")
    args = parser.parse_args()

    file_id = args.file_id
    access_token = args.access_token
    optimize_layout = args.optimize_layout

    try:
        design_elements = export_figma_elements(file_id, access_token)
        optimized_elements = optimize_design_with_ai(design_elements, optimize_layout)
        update_figma_file(file_id, access_token, optimized_elements)
        print("Figma file updated successfully.")
    except RuntimeError as e:
        print(e)

if __name__ == "__main__":
    main()