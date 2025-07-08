#!/bin/bash
source activate base

export MODEL=$1
export DATA_NAME=$2
export EXPERIMENT_NAME=$MODEL-$DATA_NAME

export N_GPUS=8
export VLLM_ATTENTION_BACKEND=XFORMERS
export LOG_FILE=log/${EXPERIMENT_NAME}.log
export PROJECT_NAME=Nips
export PPO_MICRO_BATCH_SIZE=4
export PPO_MINI_BATCH_SIZE=32
export TRAIN_BATCH_SIZE=256
export EPOCHS=10
export MAX_PROMPT_LENGTH=512
export MAX_RESPONSE_LENGTH=8192
export ROLLOUT_N=5

if [[ "$MODEL" == "qwen" ]]; then
    export BASE_MODEL=Qwen/Qwen2.5-7B
    export DIR=./models/${EXPERIMENT_NAME}/base
elif [[ "$MODEL" == "qwen_ins" ]]; then
    export BASE_MODEL=Qwen/Qwen2.5-7B-Instruct
    export DIR=./models/${EXPERIMENT_NAME}/instruct
fi

ray stop --force
sleep 1
bash examples/grpo_trainer/math_and_code.sh