import json
import requests
from pydantic import BaseModel, ValidationError
import argparse

class Design(BaseModel):
    id: str
    layout: dict

class ClaudeAPIError(Exception):
    pass

def fetch_design(api_url: str, design_id: str) -> Design:
    try:
        response = requests.get(f"{api_url}/designs/{design_id}")
        response.raise_for_status()
        return Design(**response.json())
    except requests.RequestException as e:
        raise ClaudeAPIError(f"Failed to fetch design: {e}")
    except ValidationError as e:
        raise ClaudeAPIError(f"Invalid design data: {e}")

def modify_design(design: Design, theme: str = None, resize: tuple = None) -> Design:
    modified_layout = design.layout.copy()

    if theme:
        modified_layout['theme'] = theme

    if resize:
        modified_layout['dimensions'] = {'width': resize[0], 'height': resize[1]}

    return Design(id=design.id, layout=modified_layout)

def update_design(api_url: str, design: Design) -> None:
    try:
        response = requests.put(f"{api_url}/designs/{design.id}", json=design.dict())
        response.raise_for_status()
    except requests.RequestException as e:
        raise ClaudeAPIError(f"Failed to update design: {e}")

def main():
    parser = argparse.ArgumentParser(description="Claude UI Customizer")
    parser.add_argument("api_url", help="Base URL of the Claude Design API")
    parser.add_argument("design_id", help="ID of the design to fetch and modify")
    parser.add_argument("--theme", help="Theme to apply to the design")
    parser.add_argument("--resize", nargs=2, type=int, metavar=("WIDTH", "HEIGHT"), help="Resize dimensions for the design")
    parser.add_argument("--output", help="Path to save the modified design JSON")

    args = parser.parse_args()

    try:
        design = fetch_design(args.api_url, args.design_id)
        modified_design = modify_design(design, theme=args.theme, resize=tuple(args.resize) if args.resize else None)

        if args.output:
            with open(args.output, "w") as f:
                json.dump(modified_design.dict(), f, indent=4)
            print(f"Modified design saved to {args.output}")
        else:
            update_design(args.api_url, modified_design)
            print("Design updated successfully.")

    except ClaudeAPIError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()