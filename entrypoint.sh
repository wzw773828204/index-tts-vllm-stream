#!/bin/bash

#need to set alias within container
alias python=python3
# Set default values if environment variables are not set
MODEL_DIR=${MODEL_DIR:-"assets/checkpoints/"}
MODEL=${MODEL:-"IndexTeam/IndexTTS-1.5"}
PORT=${PORT:-11996}

# Start the API server
echo "Starting IndexTTS API server on port $PORT..."
export CUDA_VISIBLE_DEVICES=2
VLLM_USE_V1=0 python3 api_server_stream.py --model_dir "$MODEL_DIR" --port "$PORT"
