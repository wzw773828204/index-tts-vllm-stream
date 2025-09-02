#!/bin/bash
set -e  # Exit on any error

MODEL_DIR=$1
VLLM_DIR="$MODEL_DIR/vllm"

if [ -z "$MODEL_DIR" ]; then
    echo "Error: MODEL_DIR not provided"
    exit 1
fi

echo "Creating vllm directory: $VLLM_DIR"
mkdir -p "$VLLM_DIR"

echo "Downloading tokenizer files..."
if ! wget https://modelscope.cn/models/openai-community/gpt2/resolve/master/tokenizer.json -O "$VLLM_DIR/tokenizer.json"; then
    echo "Error: Failed to download tokenizer.json"
    exit 1
fi

if ! wget https://modelscope.cn/models/openai-community/gpt2/resolve/master/tokenizer_config.json -O "$VLLM_DIR/tokenizer_config.json"; then
    echo "Error: Failed to download tokenizer_config.json"
    exit 1
fi

echo "Converting model format..."
if ! python convert_hf_format.py --model_dir "$MODEL_DIR"; then
    echo "Error: Model conversion failed"
    exit 1
fi

echo "All operations completed successfully!"
exit 0
