import os
import shutil
import argparse

def activate_model(version, base_path):
    """
    Activates the specified model version by updating a symbolic link and setting environment variables.

    Args:
        version (str): The version of the model/framework to activate.
        base_path (str): The base directory where model versions are stored.

    Raises:
        FileNotFoundError: If the specified version does not exist.
        Exception: If the symbolic link cannot be created.
    """
    model_path = os.path.join(base_path, version)
    symlink_path = os.path.join(base_path, "current")

    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model version '{version}' does not exist in {base_path}.")

    # Update symbolic link
    try:
        if os.path.islink(symlink_path) or os.path.exists(symlink_path):
            os.unlink(symlink_path)
        os.symlink(model_path, symlink_path)
    except OSError as e:
        raise Exception(f"Failed to create symbolic link: {e}")

    # Update environment variable
    os.environ['LLM_MODEL_PATH'] = symlink_path
    print(f"Activated model version: {version}")
    print(f"Environment variable LLM_MODEL_PATH set to: {symlink_path}")

def parse_arguments():
    """
    Parse command-line arguments.

    Returns:
        argparse.Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description="LLM Model Switcher: Switch between different versions of LLM models/frameworks."
    )
    parser.add_argument(
        "--activate",
        type=str,
        required=True,
        help="The model/framework version to activate."
    )
    parser.add_argument(
        "--base-path",
        type=str,
        required=True,
        help="The base directory where model versions are stored."
    )
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    try:
        activate_model(args.activate, args.base_path)
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error: {e}")