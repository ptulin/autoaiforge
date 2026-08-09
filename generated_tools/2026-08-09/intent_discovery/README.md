# Intent Discovery Tool
This tool helps developers identify and extract intents from large datasets of user queries, which is essential for building effective conversational AI models.

## Installation
To use this tool, you need to install the required packages. You can do this by running the following command:
```bash
pip install spacy scikit-learn
python -m spacy download en_core_web_sm
```

## Usage
To use this tool, simply run the following command:
```bash
python intent_discovery.py --input_file input.txt --output_file output.json
```
Replace `input.txt` with the path to your input file and `output.json` with the path to your desired output file.

## Input File Format
The input file should contain one query per line.

## Output File Format
The output file will contain a JSON object with the discovered intents and keywords.