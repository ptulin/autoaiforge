import argparse
import json
import torch
from torch.utils.data import DataLoader
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import matplotlib.pyplot as plt
import os

def load_dataset(dataset_path):
    """Load dataset from a JSONL file."""
    try:
        with open(dataset_path, 'r', encoding='utf-8') as f:
            data = [json.loads(line) for line in f]
        return data
    except FileNotFoundError:
        raise FileNotFoundError(f"Dataset file not found: {dataset_path}")
    except json.JSONDecodeError:
        raise ValueError(f"Dataset file is not a valid JSONL file: {dataset_path}")

def prepare_data(dataset, tokenizer):
    """Tokenize dataset."""
    texts = [item['text'] for item in dataset]
    labels = [item['label'] for item in dataset]
    encodings = tokenizer(texts, truncation=True, padding=True, max_length=512)
    return [{'input_ids': torch.tensor(encodings['input_ids'][i]), 'attention_mask': torch.tensor(encodings['attention_mask'][i]), 'labels': torch.tensor(labels[i])} for i in range(len(texts))]

def learning_rate_range_test(model_name, dataset_path, lr_min, lr_max, output_plot):
    """Perform a learning rate range test."""
    print("Loading dataset...")
    dataset = load_dataset(dataset_path)

    print("Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    print("Preparing data...")
    tokenized_data = prepare_data(dataset, tokenizer)
    dataloader = DataLoader(tokenized_data, batch_size=8, shuffle=True)

    print("Loading model...")
    model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)

    optimizer = torch.optim.AdamW(model.parameters(), lr=lr_min)

    if not list(model.parameters()):
        raise ValueError("Model has no parameters to optimize.")

    learning_rates = []
    losses = []

    lr = lr_min
    model.train()

    print("Starting learning rate range test...")
    for step, batch in enumerate(dataloader):
        if lr > lr_max:
            break

        for param_group in optimizer.param_groups:
            param_group['lr'] = lr

        inputs = {key: value.to(torch.device('cpu')) for key, value in batch.items()}

        optimizer.zero_grad()
        outputs = model(**inputs)
        loss = outputs.loss
        loss.backward()
        optimizer.step()

        learning_rates.append(lr)
        losses.append(loss.item())

        lr *= 1.1  # Increase learning rate by 10%

    print("Plotting results...")
    plt.plot(learning_rates, losses)
    plt.xscale('log')
    plt.xlabel('Learning Rate')
    plt.ylabel('Loss')
    plt.title('Learning Rate Finder')
    plt.savefig(output_plot)
    print(f"Plot saved to {output_plot}")

def main():
    parser = argparse.ArgumentParser(description="Learning Rate Finder for Fine-Tuning")
    parser.add_argument('--model', type=str, required=True, help="Hugging Face model name")
    parser.add_argument('--dataset', type=str, required=True, help="Path to dataset in JSONL format")
    parser.add_argument('--range', type=float, nargs=2, required=True, metavar=('LR_MIN', 'LR_MAX'), help="Learning rate range (min max)")
    parser.add_argument('--output', type=str, default='lr_plot.png', help="Output file for the learning rate vs. loss plot")

    args = parser.parse_args()

    try:
        learning_rate_range_test(args.model, args.dataset, args.range[0], args.range[1], args.output)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
