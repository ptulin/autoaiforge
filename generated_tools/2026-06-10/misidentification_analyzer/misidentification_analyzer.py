import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.cluster import KMeans
import json

def analyze_errors(predictions, true_labels, metadata=None, n_clusters=3, output_json=True):
    """
    Analyze misidentifications in AI model predictions.

    Args:
        predictions (list or np.ndarray): Model predictions.
        true_labels (list or np.ndarray): True labels.
        metadata (list of dict, optional): Additional metadata for each data point (e.g., demographic info).
        n_clusters (int): Number of clusters for error clustering.
        output_json (bool): Whether to output a JSON summary.

    Returns:
        dict: JSON summary of the analysis if output_json is True.
    """
    if len(predictions) != len(true_labels):
        raise ValueError("Predictions and true labels must have the same length.")

    if len(predictions) == 0:
        return {
            "confusion_matrix": [],
            "classification_report": {},
            "misclassified_data": {
                "indices": [],
                "predictions": [],
                "true_labels": []
            }
        }

    # Generate confusion matrix
    cm = confusion_matrix(true_labels, predictions)
    labels = sorted(set(true_labels))

    # Plot confusion matrix
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=labels, yticklabels=labels)
    plt.xlabel('Predicted Labels')
    plt.ylabel('True Labels')
    plt.title('Confusion Matrix')
    plt.show()

    # Classification report
    report = classification_report(true_labels, predictions, output_dict=True)

    # Identify misclassified samples
    misclassified_indices = [i for i, (pred, true) in enumerate(zip(predictions, true_labels)) if pred != true]
    misclassified_data = {
        "indices": misclassified_indices,
        "predictions": [predictions[i] for i in misclassified_indices],
        "true_labels": [true_labels[i] for i in misclassified_indices],
    }

    # Add metadata if provided
    if metadata:
        misclassified_data["metadata"] = [metadata[i] for i in misclassified_indices]

        # Cluster misclassified samples
        if len(misclassified_indices) >= n_clusters:  # Ensure enough samples for clustering
            features = np.array([list(m.values()) for m in misclassified_data["metadata"]])
            kmeans = KMeans(n_clusters=n_clusters, random_state=42)
            clusters = kmeans.fit_predict(features)
            misclassified_data["clusters"] = list(clusters)  # Ensure clusters is a list
        else:
            misclassified_data["clusters"] = [0] * len(misclassified_indices)  # Assign all to one cluster

    # Generate JSON summary
    summary = {
        "confusion_matrix": cm.tolist(),
        "classification_report": report,
        "misclassified_data": misclassified_data,
    }

    if output_json:
        print(json.dumps(summary, indent=4))

    return summary

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Misidentification Analyzer")
    parser.add_argument("--predictions", type=str, required=True, help="Path to predictions file (comma-separated).")
    parser.add_argument("--true_labels", type=str, required=True, help="Path to true labels file (comma-separated).")
    parser.add_argument("--metadata", type=str, help="Path to metadata file (JSON format).")
    parser.add_argument("--n_clusters", type=int, default=3, help="Number of clusters for error clustering.")

    args = parser.parse_args()

    # Load data
    predictions = np.loadtxt(args.predictions, delimiter=',')
    true_labels = np.loadtxt(args.true_labels, delimiter=',')
    metadata = None
    if args.metadata:
        with open(args.metadata, 'r') as f:
            metadata = json.load(f)

    analyze_errors(predictions, true_labels, metadata, n_clusters=args.n_clusters)
