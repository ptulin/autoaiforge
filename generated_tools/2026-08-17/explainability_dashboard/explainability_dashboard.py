import argparse
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split


def load_model(model_path):
    try:
        return pd.read_pickle(model_path)
    except Exception as e:
        print(f"Error loading model: {e}")
        return None


def load_dataset(dataset_path):
    try:
        return pd.read_csv(dataset_path)
    except Exception as e:
        print(f"Error loading dataset: {e}")
        return None


def create_dashboard(model, dataset):
    app = dash.Dash(__name__)
    app.layout = html.Div([
        html.H1('Explainability Dashboard'),
        dcc.Graph(id='feature-importance'),
        dcc.Graph(id='decision-boundary')
    ])

    @app.callback(
        Output('feature-importance', 'figure'),
        [Input('feature-importance', 'id')]
    )
    def update_feature_importance(graph_id):
        fig = px.bar(x=model.feature_importances_, title='Feature Importance')
        return fig

    @app.callback(
        Output('decision-boundary', 'figure'),
        [Input('decision-boundary', 'id')]
    )
    def update_decision_boundary(graph_id):
        fig = px.scatter(x=dataset.iloc[:, 0], y=dataset.iloc[:, 1], title='Decision Boundary')
        return fig

    return app


def main():
    parser = argparse.ArgumentParser(description='Explainability Dashboard')
    parser.add_argument('--model', help='Path to AI model', required=True)
    parser.add_argument('--dataset', help='Path to dataset', required=True)
    args = parser.parse_args()

    model = load_model(args.model)
    dataset = load_dataset(args.dataset)

    if model and dataset:
        create_dashboard(model, dataset)
    else:
        print("Error: Unable to load model or dataset.")

if __name__ == '__main__':
    main()