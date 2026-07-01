# GPU GEMM Optimizer

This tool analyzes and optimizes low-latency General Matrix Multiplication (GEMM) operations on GPUs for LLM inference. By leveraging vendor-specific libraries like CuPy or ROCm (via PyTorch), it helps developers adjust parameters such as block sizes or memory layouts for maximum throughput.

## Installation

To use this tool, you need to install the required dependencies:

```bash
pip install cupy torch pytest
```

## Usage

Run the tool from the command line:

```bash
python gpu_gemm_optimizer.py --m <rows_of_A> --n <columns_of_B> --k <columns_of_A_rows_of_B> --device <cuda_or_rocm> [--block_size <block_size>]
```

### Example

```bash
python gpu_gemm_optimizer.py --m 512 --n 256 --k 128 --device cuda
```

## Testing

Run the tests using pytest:

```bash
pytest test_gpu_gemm_optimizer.py
```

## Notes

- Ensure you have the appropriate GPU hardware and drivers installed for CUDA or ROCm.
- The tool dynamically imports CuPy or PyTorch, so ensure the required library is installed based on your GPU backend.
