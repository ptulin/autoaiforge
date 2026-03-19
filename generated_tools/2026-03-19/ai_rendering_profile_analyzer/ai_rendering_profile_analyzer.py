import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import os

def analyze_rendering_logs(input_file, output_file, output_format):
    try:
        # Load the data
        if input_file.endswith('.csv'):
            data = pd.read_csv(input_file)
        elif input_file.endswith('.json'):
            data = pd.read_json(input_file)
        else:
            raise ValueError("Unsupported file format. Only CSV and JSON are supported.")

        # Validate required columns
        required_columns = ['frame', 'render_time', 'gpu_usage', 'resolution']
        for col in required_columns:
            if col not in data.columns:
                raise ValueError(f"Missing required column: {col}")

        # Perform analysis
        avg_render_time = data['render_time'].mean()
        max_gpu_usage = data['gpu_usage'].max()
        high_res_frames = data[data['resolution'] > 1080]

        recommendations = {
            "average_render_time": float(avg_render_time),
            "max_gpu_usage": int(max_gpu_usage),
            "high_resolution_frame_count": int(len(high_res_frames)),
            "dlss_recommendation": "Consider using DLSS 5 for high-resolution frames to optimize performance."
        }

        # Output results
        if output_format == 'json':
            with open(output_file, 'w') as f:
                json.dump(recommendations, f, indent=4)
        elif output_format == 'text':
            with open(output_file, 'w') as f:
                for key, value in recommendations.items():
                    f.write(f"{key}: {value}\n")
        elif output_format == 'plot':
            plt.figure(figsize=(10, 6))
            plt.plot(data['frame'], data['render_time'], label='Render Time (ms)')
            plt.plot(data['frame'], data['gpu_usage'], label='GPU Usage (%)')
            plt.xlabel('Frame')
            plt.ylabel('Metrics')
            plt.title('Rendering Performance Analysis')
            plt.legend()
            plt.savefig(output_file)
        else:
            raise ValueError("Unsupported output format. Choose from 'json', 'text', or 'plot'.")

    except Exception as e:
        raise RuntimeError(f"Error during analysis: {e}")


def main():
    parser = argparse.ArgumentParser(description="AI Rendering Profile Analyzer")
    parser.add_argument('--input', required=True, help="Path to the input rendering log file (CSV or JSON).")
    parser.add_argument('--output', required=True, help="Path to the output file.")
    parser.add_argument('--format', choices=['json', 'text', 'plot'], required=True, help="Output format: 'json', 'text', or 'plot'.")

    args = parser.parse_args()

    try:
        analyze_rendering_logs(args.input, args.output, args.format)
        print(f"Analysis completed successfully. Results saved to {args.output}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()