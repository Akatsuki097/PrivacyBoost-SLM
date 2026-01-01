BioLinkBERT Interactive Demo
This project allows you to interact with a medical AI model (BioLinkBERT) by asking it multiple-choice medical questions.

1. Prerequisites
Ensure you have your Anaconda environment activated:

PowerShell

conda activate PBSLM
2. The "Test" Demo (Untrained)
If you just want to see the code run (even if the answers are random), use the base model you downloaded manually.

Ensure your demo.py points to the base folder:

Python

model_path = "./BioLinkBERT-base"
Run the script:

PowerShell

python demo.py
Note: Since this model is untrained, it will likely always guess Option 1 because it hasn't learned how to make decisions yet.

3. The "Smart" Demo (Micro-Trained)
To make the model actually try to answer questions, you need to run a quick 5-minute training session.

Step A: Run Micro-Training
Run this command to train the model for just 50 steps (approx. 5-10 mins). This teaches it how to select options other than "Option 1".

PowerShell

python -W ignore run_bert_training_eval.py --model_name_or_path ./BioLinkBERT-base --dataset_name medqa --seed 1 --per_device_train_batch_size 1 --gradient_accumulation_steps 8 --shot -1 --train_split train_singletask_all_qac_eA --eval_split qta_question_validation_all_qac_eA_medqa --per_device_eval_batch_size 1 --train --output_dir ./results/micro_train --max_steps 50
Step B: Point Demo to New Model
Open demo.py and change line 7 to point to your newly trained folder:

Python

# Change this line:
model_path = "./results/micro_train"
Step C: Run It
PowerShell

python demo.py
Now the model should give different answers based on the question!

Sample Questions to Try
Cardiology:

Q: A 65-year-old male presents with crushing chest pain radiating to his left arm. ECG shows ST elevation.

Option 1: Acid Reflux

Option 2: Acute Myocardial Infarction

Option 3: Panic Attack

Option 4: Pneumonia

General:

Q: A child scrapes his knee and it bleeds. Which cell type stops the bleeding?

Option 1: Neurons

Option 2: Platelets

Option 3: White Blood Cells

Option 4: Red Blood Cells