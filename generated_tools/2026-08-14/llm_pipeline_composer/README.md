# LLM Pipeline Composer

This tool enables developers to create and manage complex LLM pipelines by providing a visual interface for composing and configuring model workflows.

## Installation

To install the required packages, run the following command:

```bash
pip install graphviz streamlit
```

## Usage

To run the tool, execute the following command:

```bash
python llm_pipeline_composer.py --edit
```

This will launch a Streamlit app where you can enter the LLM model and pipeline configuration (in JSON format). Clicking the 'Compose Pipeline' button will generate a directed graph representing the pipeline.