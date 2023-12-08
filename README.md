# AICUP_2023_Fall
隱私保護與醫學數據標準化競賽： 解碼臨床病例、讓數據說故事競賽 競賽報告
## Environment Setup (python3.10)
### package installation
```
pip uninstall -y tensorflow --quiet
pip install ludwig
pip install ludwig[llm]
pip install accelerate
pip install -i https://test.pypi.org/simple/ bitsandbytes
pip install tqdm
pip install pandas
```
### HuggingFace Token Setup for Llama2 model
```
os.environ["HUGGING_FACE_HUB_TOKEN"] = {Your Token}
```
## 資料夾結構
```
.
├── ensemble_models_results.py
├── dataset
│   ├── augment_data.tsv
│   ├── country.txt
│   ├── First_Phase_Release(Correction)
│   │   ├── answer.txt
│   │   ├── First_Phase_Text_Dataset
│   │   └── Validation_Release
│   ├── opendid_test
│   │   ├── opendid_test
│   │   └── opendid_test.tsv
│   ├── processed
│   │   ├── 5line_split
│   │   │   ├── First_Phase_Text_Dataset_processed.tsv
│   │   │   ├── Second_Phase_Text_Dataset_processed.tsv
│   │   │   ├── total_train.tsv
│   │   │   └── Validation_Release_processed.tsv
│   │   ├── line_split
│   │   │   ├── First_Phase_Text_Dataset_processed.tsv
│   │   │   ├── Second_Phase_Text_Dataset_processed.tsv
│   │   │   ├── total_train.tsv
│   │   │   └── Validation_Release_processed.tsv
│   ├── Second_Phase_Dataset
│   │   ├── answer.txt
│   │   └── Second_Phase_Text_Dataset
│   ├── validation_answer.txt
│   └── Validation_Release_processed.tsv
├── results
│   ├── api_experiment_run
│   │   ├── description.json
│   │   ├── training_statistics.json
│   │   └── model
├── llama2_src
│   ├── concat_trainset.py
│   ├── data_augment.py
│   ├── data_postprocess.py
│   ├── data_preprocess.py
│   ├── find_re.py
│   ├── inference.py
│   └── train.py
```

## Llama2-7B
### Training Phase
#### preprocess training set
```
python llama2_src/data_preprocess.py
```
#### data augmentation
```
python llama2_src/data_augment.py
```
#### concatenate training data and augmented data
```
python llama2_src/concat_trainset.py
```
#### training
```
python llama2_src/train.py
```

### Testing Phase
#### preprocess testing set
```
python llama2_src/data_preprocess.py -t
```
#### inference
```
python llama2_src/inference.py
```
### data postprocess to generate llama2_answer.txt
```
python llama2_src/data_postprocess.py
```
### find rule-based PHI type
```
python llama2_src/find_re.py
```

## Roberta