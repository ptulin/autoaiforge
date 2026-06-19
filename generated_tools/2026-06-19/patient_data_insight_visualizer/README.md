# Patient Data Insight Visualizer

## Description
The Patient Data Insight Visualizer is a Python library and CLI tool designed to help healthcare teams visualize patient data trends and AI-derived insights. It provides customizable charts and graphs to make complex data accessible and actionable, enabling better understanding of patient trends, highlighting anomalies, and interpreting AI predictions in the context of rare disease diagnostics.

## Features
- Generates interactive or static visualizations of patient data trends.
- Supports overlaying AI predictions onto patient data for better context.
- Allows customization of visualization styles to fit different use cases.

## Installation
1. Clone the repository or download the `patient_data_insight_visualizer.py` file.
2. Install the required dependencies:
   ```bash
   pip install pandas==1.5.3 matplotlib==3.7.2 seaborn==0.12.2 plotly==5.15.0
   ```

## Usage
### CLI
To use the tool via the command line, run:
```bash
python patient_data_insight_visualizer.py --input <input_file> --output <output_file>
```
Example:
```bash
python patient_data_insight_visualizer.py --input patient_data.csv --output insights.html
```

### Library
You can also use the tool as a Python library:
```python
from patient_data_insight_visualizer import load_data, generate_visualizations

data = load_data("patient_data.csv")
generate_visualizations(data, "insights.html")
```

## Example Input
Input CSV file:
```csv
date,value1,value2
2023-01-01,10,20
2023-01-02,15,25
```

## Example Output
- Time-series plot saved as `insights_time_series.html`
- Heatmap saved as `insights_heatmap.png`
- Scatter plot saved as `insights_scatter.html`

## Testing
Run the tests using pytest:
```bash
pytest test_patient_data_insight_visualizer.py
```

## License
This project is licensed under the MIT License.