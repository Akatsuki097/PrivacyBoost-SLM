import os
import sys

file_path = "run_bert_training_eval.py"
print(f"Reading {file_path}...")

with open(file_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

# --- 1. DEFINE THE CORRECT HEADER ---
# This explicitly adds the script's own folder to the path and imports BertForMTL directly.
super_header = """import sys
import os
# Force Python to look in the script's own directory for 'modeling' and 'utils'
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

import json
import logging
import math
import random
import time
import shutil
import argparse
from fnmatch import fnmatch
from copy import deepcopy
from dataclasses import dataclass, field
from typing import Optional, Union, List, Dict, Tuple
import numpy as np

# PyTorch & ML
import torch
from torch.optim import AdamW
from torch.utils.data import DataLoader
from tensorboardX import SummaryWriter
from accelerate import Accelerator
import datasets
from datasets import load_dataset
try:
    from datasets import load_metric
except ImportError:
    from evaluate import load as load_metric

# Transformers
import transformers
from transformers import (
    CONFIG_MAPPING,
    MODEL_FOR_MASKED_LM_MAPPING,
    AutoConfig,
    AutoModelForMaskedLM,
    AutoTokenizer,
    HfArgumentParser,
    Trainer,
    TrainingArguments,
    is_torch_tpu_available,
    set_seed,
    AutoModelForMultipleChoice,
    get_scheduler
)
try:
    from transformers import SchedulerType
except ImportError:
    from transformers.trainer_utils import SchedulerType

# Local Imports (CRITICAL: These must function)
try:
    from modeling.modeling_bert import BertForMTL
    from utils.data_utils import (
        MedQAForBert, 
        MedMACQAForBert, 
        HeadQAForBert, 
        MMLUForBert, 
        DataCollatorForMultipleChoice
    )
except ImportError as e:
    print("\\nCRITICAL ERROR: Could not import project files!")
    print(f"Error details: {e}")
    print("Please make sure the folders 'modeling' and 'utils' exist in this directory.")
    print(f"Current Directory: {os.getcwd()}")
    print(f"Script Directory: {current_dir}\\n")
    # We re-raise to stop execution so you see the error immediately
    raise e 
"""

# --- 2. FIND START OF REAL CODE ---
# We keep everything after the logger definition
start_index = 0
found_logger = False
for i, line in enumerate(lines):
    if "logger = logging.getLogger(__name__)" in line:
        start_index = i
        found_logger = True
        break

if not found_logger:
    print("Warning: Could not find logger definition. Using generic cleanup.")
    # Fallback: strip imports manually if logger line is missing
    clean_body = [line for line in lines if not line.startswith("import ") and not line.startswith("from ")]
else:
    print(f"Found code body at line {start_index}. Replacing headers.")
    clean_body = lines[start_index:]

# --- 3. WRITE THE NEW FILE ---
with open(file_path, "w", encoding="utf-8") as f:
    f.write(super_header + "\n")
    f.writelines(clean_body)

print("-" * 30)
print("SUCCESS! File patched.")
print("If you run the script and get 'ModuleNotFoundError', it means the 'modeling' folder is actually missing from your computer.")