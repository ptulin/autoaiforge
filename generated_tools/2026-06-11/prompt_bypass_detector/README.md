# Prompt Bypass Detector

## Overview
The Prompt Bypass Detector is a Python tool designed to help developers detect and classify attempted bypasses of AI safety guardrails. It analyzes input prompts and model responses for suspicious patterns, aiding in identifying edge cases and improving model safety.

## Features
- Detect potential bypass attempts in input prompts and model responses.
- Classify inputs and responses as "safe" or "bypass."
- Provide anomaly scores for both input and response.

## Installation

Install the required dependencies using pip:

```bash
pip install scikit-learn numpy
```

## Usage

Run the tool from the command line:

```bash
python prompt_bypass_detector.py "<input_prompt>" "<model_response>"
```

Example:

```bash
python prompt_bypass_detector.py "This is a test prompt." "This is a test response."
```

## Testing

To run the tests, install `pytest` and run the following command:

```bash
pip install pytest
pytest test_prompt_bypass_detector.py
```

## Files
- `prompt_bypass_detector.py`: The main tool for detecting prompt bypass attempts.
- `test_prompt_bypass_detector.py`: Test cases for the tool.

## Notes
- Ensure that the `bypass_detector_model.pkl` and `tfidf_vectorizer.pkl` files are present in the same directory as `prompt_bypass_detector.py`.
- If these files are missing, the tool will return an error indicating their absence.
