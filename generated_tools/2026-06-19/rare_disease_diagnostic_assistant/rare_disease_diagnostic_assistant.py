import argparse
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import joblib
from sklearn.ensemble import RandomForestClassifier

def load_model(model_path):
    """Load the pre-trained AI model."""
    try:
        model = joblib.load(model_path)
        return model
    except Exception as e:
        raise ValueError(f"Error loading model: {e}")

def load_patient_data(input_path):
    """Load patient data from a CSV or JSON file."""
    try:
        if input_path.endswith('.csv'):
            return pd.read_csv(input_path)
        elif input_path.endswith('.json'):
            return pd.read_json(input_path)
        else:
            raise ValueError("Unsupported file format. Use CSV or JSON.")
    except Exception as e:
        raise ValueError(f"Error loading input data: {e}")

def generate_diagnostic_report(model, patient_data):
    """Generate diagnostic predictions and confidence scores."""
    try:
        predictions = model.predict_proba(patient_data)
        classes = model.classes_
        results = []
        for i, probs in enumerate(predictions):
            patient_result = {
                "patient_id": patient_data.index[i],
                "diagnoses": [
                    {"disease": classes[j], "confidence": float(probs[j])}
                    for j in np.argsort(probs)[::-1]
                ]
            }
            results.append(patient_result)
        return results
    except Exception as e:
        raise ValueError(f"Error generating diagnostic report: {e}")

def save_report(report, output_path):
    """Save the diagnostic report to a JSON file."""
    try:
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=4)
    except Exception as e:
        raise ValueError(f"Error saving report: {e}")

def plot_diagnostics(report, output_path):
    """Generate and save diagnostic visualizations."""
    try:
        for patient in report:
            patient_id = patient['patient_id']
            diagnoses = patient['diagnoses'][:5]  # Top 5 diagnoses
            diseases = [d['disease'] for d in diagnoses]
            confidences = [d['confidence'] for d in diagnoses]

            plt.figure(figsize=(10, 6))
            plt.barh(diseases, confidences, color='skyblue')
            plt.xlabel('Confidence')
            plt.title(f'Diagnostic Confidence for Patient {patient_id}')
            plt.gca().invert_yaxis()
            plt.tight_layout()
            plt.savefig(f"{output_path}_patient_{patient_id}.png")
            plt.close()
    except Exception as e:
        raise ValueError(f"Error generating plots: {e}")

def main():
    parser = argparse.ArgumentParser(description="Rare Disease Diagnostic Assistant")
    parser.add_argument('--input', required=True, help="Path to input patient data (CSV or JSON)")
    parser.add_argument('--model', required=True, help="Path to pre-trained AI model (Pickle file)")
    parser.add_argument('--output', required=True, help="Path to save the diagnostic report (JSON file)")

    args = parser.parse_args()

    try:
        # Load model and data
        model = load_model(args.model)
        patient_data = load_patient_data(args.input)

        # Generate diagnostic report
        report = generate_diagnostic_report(model, patient_data)

        # Save report
        save_report(report, args.output)

        # Generate and save visualizations
        plot_diagnostics(report, args.output)

        print(f"Diagnostic report and visualizations saved successfully to {args.output}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()