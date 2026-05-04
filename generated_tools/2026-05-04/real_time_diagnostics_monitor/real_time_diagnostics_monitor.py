import asyncio
import json
import pickle
from typing import Callable, Optional
import websockets
from sklearn.base import BaseEstimator

class DiagnosticMonitor:
    def __init__(self, model_path: str, alert_callback: Optional[Callable[[dict], None]] = None):
        """
        Initialize the DiagnosticMonitor.

        :param model_path: Path to the pre-trained model file (pickle format).
        :param alert_callback: Optional callback function to handle alerts.
        """
        self.model_path = model_path
        self.alert_callback = alert_callback
        self.model = self._load_model()

    def _load_model(self) -> BaseEstimator:
        """
        Load the pre-trained model from the specified path.

        :return: Loaded model.
        """
        try:
            with open(self.model_path, 'rb') as f:
                model = pickle.load(f)
            if not isinstance(model, BaseEstimator):
                raise ValueError("Loaded object is not a scikit-learn model.")
            return model
        except Exception as e:
            raise RuntimeError(f"Failed to load model: {e}")

    async def _process_message(self, message: str):
        """
        Process a single message from the data stream.

        :param message: JSON string containing patient data.
        """
        try:
            data = json.loads(message)
            if not isinstance(data, dict):
                raise ValueError("Message must be a JSON object.")

            features = data.get("features")
            if not isinstance(features, list):
                raise ValueError("Features must be a list.")

            prediction = self.model.predict([features])[0]
            alert = {
                "patient_id": data.get("patient_id"),
                "prediction": prediction,
                "timestamp": data.get("timestamp")
            }

            if self.alert_callback:
                self.alert_callback(alert)
            else:
                print(json.dumps(alert))

        except Exception as e:
            print(f"Error processing message: {e}")

    async def start_stream(self, websocket_url: str):
        """
        Start monitoring the real-time data stream.

        :param websocket_url: WebSocket URL to connect to.
        """
        try:
            async with websockets.connect(websocket_url) as websocket:
                print("Connected to WebSocket.")
                async for message in websocket:
                    await self._process_message(message)
        except Exception as e:
            print(f"Error in WebSocket connection: {e}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Real-Time Diagnostics Monitor")
    parser.add_argument("--model", required=True, help="Path to the pre-trained model file.")
    parser.add_argument("--websocket", required=True, help="WebSocket URL to connect to.")
    args = parser.parse_args()

    monitor = DiagnosticMonitor(model_path=args.model)
    asyncio.run(monitor.start_stream(args.websocket))