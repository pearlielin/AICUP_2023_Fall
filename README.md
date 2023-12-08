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
├── aicup_submit.ipynb
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
process the medical record and store the processed data to folder `dataset/processed/line_split`
```
python llama2_src/data_preprocess.py
```
#### data augmentation
do the data augmentation on PHI type LOCATION-OTHER, SET, TIME and save the augmented data to `dataset/augment_data.tsv`
```
python llama2_src/data_augment.py
```
#### concatenate training data and augmented data
concatenate the data and save to `dataset/processed/line_split/total_train.tsv`
```
python llama2_src/concat_trainset.py
```
#### training
train the model and save the model to `results`
```
python llama2_src/train.py
```

### Testing Phase
#### preprocess testing set
process the testing set and save the processed data to `dataset/processed/line_split/opendid_test_processed.tsv`
```
python llama2_src/data_preprocess.py -t
```
#### inference
inference the testing set and save the result to `test_output.csv`
```
python llama2_src/inference.py
```
### data postprocess
process the file `test_output.csv` to the answer format and save to `llama2_answer.txt`
```
python llama2_src/data_postprocess.py
```
### find rule-based PHI type and append to llama2_answer.txt
find COUNTRY, SET, DURATION of the testing set via rule-based method and append the output to `llama2_answer.txt`
```
python llama2_src/find_re.py
```

## Roberta
open the script `aicup_submit.ipynb` on colab. Every setting just rewrite the first block


### Checkpoint load
Rewrite the stage_1_model_path to the model checkpoint path. Default download the model (model_36.39.pt) we train save in google drive
```
stage_1_model_path = 'model_36.39.pt'
```
### Training Phase
If train the model from scratch 
set stage_1_model_path to None
and set stage_1_training to True
```
stage_1_model_path = None
stage_1_training = True
```

### Testing Phase
If only test the model performance on test data 
set stage_1_model_path to model be test
and set stage_1_training to False
default download the model (model_36.39.pt) we train save in google drive
```
stage_1_model_path = 'model_36.39.pt'
stage_1_training = False
```

### Download the result
The script will automate download the predict result of test data. The result filename is `roberta_answer.txt`. You need to put the result file to the root directory of this repo to merge the result with llama2 output. 

## Merge result
After use llama2 and Roberta to inference the test data. Use the `ensemble_models_results.py` to merge the two result.

### Check 
Check if the `llama2_answer.txt` and `roberta_answer.txt` both under the root directory of this repo. 

### Merge
Merge the result by execute the following command. And the merge result `answer.txt` will save in the root directory.
```
python ensemble_models_results.py
```


