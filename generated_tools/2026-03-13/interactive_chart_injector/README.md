# Interactive Chart Injector

## Description
Interactive Chart Injector is a Python library that allows AI developers to seamlessly integrate dynamically generated interactive charts from AI tools like Claude into Jupyter notebooks. It parses AI-generated chart data and converts it into interactive visualizations using Plotly, enabling developers to debug, share, and explore AI-driven insights easily.

## Features
- **Seamless Integration**: Easily integrate AI-generated chart data into Jupyter notebooks.
- **Interactive Visualizations**: Supports interactive Plotly charts for deeper exploration.
- **Simple API**: Parse and render AI chart data with a single function call.

## Installation

```bash
pip install plotly==5.15.0 pandas==2.1.1 ipython==8.16.1
```

## Usage

### Example

```python
import interactive_chart_injector

# Example chart data
data = {
    "type": "scatter",
    "data": [
        {"x": [1, 2, 3], "y": [4, 5, 6], "mode": "lines", "name": "Test Line"}
    ],
    "layout": {"title": "Test Scatter Chart"}
}

interactive_chart_injector.render_chart(data)
```

### CLI Usage

You can also use this tool from the command line:

```bash
python interactive_chart_injector.py path_to_chart_data.json
```

## Input Format
The input chart data must be a dictionary or a JSON string with the following structure:

```json
{
    "type": "scatter",  // or "bar"
    "data": [
        {"x": [...], "y": [...], "mode": "lines", "name": "..."}
    ],
    "layout": {"title": "..."}
}
```

## Supported Chart Types
- Scatter
- Bar

## Error Handling
The library validates the input data and raises meaningful errors for:
- Invalid JSON strings
- Missing required keys (`type`, `data`, `layout`)
- Unsupported chart types

## Testing

Run the tests using `pytest`:

```bash
pytest test_interactive_chart_injector.py
```