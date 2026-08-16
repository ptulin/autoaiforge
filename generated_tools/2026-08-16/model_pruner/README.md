# Model Pruner
This tool helps optimize AI model architecture by pruning unnecessary weights and connections, resulting in a more efficient and lightweight model.

## Usage
To use the model pruner, simply run the script with the following arguments:
* `--input_model`: The path to the trained model file
* `--pruning_ratio`: The pruning ratio
* `--pruning_method`: The pruning method (either `gradient-based` or `magnitude-based`)
* `--output_model`: The path to the pruned model file

## Example
```bash
python model_pruner.py --input_model model.pt --pruning_ratio 0.5 --pruning_method magnitude-based --output_model pruned_model.pt
```