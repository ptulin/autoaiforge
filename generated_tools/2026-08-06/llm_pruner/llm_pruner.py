import argparse
import torch
from transformers import AutoModelForSequenceClassification


def prune_model(model_path, pruning_ratio):
    model = AutoModelForSequenceClassification.from_pretrained(model_path)
    for name, param in model.named_parameters():
        if param.requires_grad:
            param.data = torch.where(torch.abs(param) > pruning_ratio * torch.max(torch.abs(param)), param, torch.zeros_like(param))
    return model


def save_model(model, output_path):
    model.save_pretrained(output_path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='LLM Pruner')
    parser.add_argument('--model_path', type=str, required=True, help='Path to the LLM model file')
    parser.add_argument('--pruning_ratio', type=float, required=True, help='Pruning ratio')
    parser.add_argument('--output_path', type=str, required=True, help='Path to save the pruned model')
    args = parser.parse_args()
    model = prune_model(args.model_path, args.pruning_ratio)
    save_model(model, args.output_path)