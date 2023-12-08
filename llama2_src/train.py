from transformers import GenerationConfig, LlamaForCausalLM, LlamaTokenizer
import torch
import pandas as pd
import logging
import time
from tqdm import tqdm
import argparse
import random
import yaml
from ludwig.api import LudwigModel


if __name__ == '__main__':
    df = pd.read_csv('dataset/processed/line_split/total_train.tsv', sep="\t")

    qlora_fine_tuning_config = yaml.safe_load(
        """
    model_type: llm
    base_model: meta-llama/Llama-2-7b-hf

    input_features:
        - name: instruction
          type: text

    output_features:
        - name: output
          type: text

    prompt:
        template: >-
            Below is an instruction that describes a task, paired with an input
            that provides further context. Write a response that appropriately
            completes the request.

            ### Instruction: {instruction}

            ### Input: {input}

            ### Response:

    generation:
        temperature: 0.1
        max_new_tokens: 512

    adapter:
        type: lora

    quantization:
        bits: 4

    preprocessing:
        global_max_sequence_length: 512
        split:
            type: random
            probabilities:
            - 1
            - 0
            - 0

    trainer:
        type: finetune
        epochs: 1
        batch_size: 1
        eval_batch_size: 2
        gradient_accumulation_steps: 16
        learning_rate: 0.0004
        learning_rate_scheduler:
            warmup_fraction: 0.03
    """
    )

model = LudwigModel(config=qlora_fine_tuning_config,
                    logging_level=logging.INFO)

start_time = time.time()
results = model.train(dataset=df)
end_time = time.time()
print("====training time: " + str(end_time-start_time) + "====")
