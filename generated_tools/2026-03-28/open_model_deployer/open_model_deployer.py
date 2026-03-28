import argparse
import os
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn

# Mockable model loader function
def load_model(model_path):
    # Simulate loading a model (replace with actual implementation later)
    if os.path.isdir(model_path):
        return lambda x: f"Mock prediction for '{x}' with model at {model_path}"
    else:
        return lambda x: f"Mock prediction for '{x}' with model ID {model_path}"

def create_fastapi_app(model):
    app = FastAPI()

    @app.get("/predict")
    async def predict(input_text: str):
        try:
            result = model(input_text)
            return JSONResponse(content={"result": result})
        except Exception as e:
            return JSONResponse(content={"error": str(e)}, status_code=500)

    return app

def deploy_model(model_path, backend):
    if backend.lower() not in ["fastapi"]:
        raise ValueError("Currently, only 'fastapi' backend is supported.")

    # Load the model
    try:
        model = load_model(model_path)
    except Exception as e:
        raise RuntimeError(f"Failed to load the model from {model_path}. Error: {e}")

    # Deploy using FastAPI
    if backend.lower() == "fastapi":
        app = create_fastapi_app(model)
        uvicorn.run(app, host="0.0.0.0", port=8000)

def main():
    parser = argparse.ArgumentParser(description="Open Model Deployer: Deploy AI models as REST APIs.")
    parser.add_argument("--model", required=True, help="Path to the model (local directory or model ID).")
    parser.add_argument("--backend", required=True, choices=["fastapi"], help="Deployment backend (currently only 'fastapi' is supported).")

    args = parser.parse_args()

    try:
        deploy_model(args.model, args.backend)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()