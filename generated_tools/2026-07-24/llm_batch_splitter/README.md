# LLM Batch Splitter

## Description
LLM Batch Splitter is a Python library designed to split large input batches for language model (LLM) inference into smaller, memory-efficient chunks. This enables seamless processing on low-resource devices while automatically managing batching and reassembly of outputs.

## Features
- **Automatic Batch Splitting**: Splits input texts into smaller chunks based on memory constraints.
- **Output Reassembly**: Reassembles model outputs in the original order.
- **Optimized for Performance**: Minimal overhead during processing.

## Installation
Install the required dependencies:
```bash
pip install numpy==1.23.5 transformers==4.33.2
```

## Usage
```python
from llm_batch_splitter import process_in_chunks
from transformers import AutoModelForCausalLM, AutoTokenizer

# Load your model and tokenizer
model_name = "gpt2"
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Input texts
inputs = ["Hello, world!", "How are you?", "This is a test."]

# Process inputs in chunks
outputs = process_in_chunks(model, tokenizer, inputs, max_chunk_size=2)
print(outputs)
```

## CLI Usage
```bash
python llm_batch_splitter.py --inputs "Hello, world!" "How are you?" --max_chunk_size 2
```

## License
This project is licensed under the MIT License.
