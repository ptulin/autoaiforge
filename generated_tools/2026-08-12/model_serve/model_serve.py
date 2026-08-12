import argparse
import json
from flask import Flask, request, jsonify
import tensorflow as tf
import torch
from sklearn import ensemble

app = Flask(__name__)

def load_model(model_path, framework):
    if framework == 'tensorflow':
        return tf.keras.models.load_model(model_path)
    elif framework == 'pytorch':
        return torch.load(model_path)
    elif framework == 'scikit-learn':
        return ensemble.RandomForestClassifier()  # dummy model for testing
    else:
        raise ValueError('Unsupported framework')

def serve_model(model, endpoint, framework):
    def predict():
        data = request.get_json()
        if framework == 'tensorflow':
            predictions = model.predict(data)
        elif framework == 'pytorch':
            predictions = model(torch.tensor(data))
        elif framework == 'scikit-learn':
            predictions = model.predict(data)
        return jsonify({'predictions': predictions.tolist()})

    app.add_url_rule(endpoint, endpoint, predict, methods=['POST'])
    return app

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='AI Model Serving Framework')
    parser.add_argument('--model_path', type=str, required=True, help='Path to the model file')
    parser.add_argument('--framework', type=str, required=True, help='Framework type (tensorflow, pytorch, scikit-learn)')
    parser.add_argument('--endpoint', type=str, required=True, help='API endpoint')
    args = parser.parse_args()
    model = load_model(args.model_path, args.framework)
    app = serve_model(model, args.endpoint, args.framework)
    app.run(debug=True)