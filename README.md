# AICUP_2023_Fall
隱私保護與醫學數據標準化競賽： 解碼臨床病例、讓數據說故事競賽 競賽報告
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
│   │   │   ├── total_train(1+2+aug).tsv
│   │   │   ├── total_train.tsv
│   │   │   └── Validation_Release_processed.tsv
│   ├── Second_Phase_Dataset
│   │   ├── answer.txt
│   │   └── Second_Phase_Text_Dataset
│   ├── validation_answer.txt
│   └── Validation_Release_processed.tsv
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
### data preprocess
```
python llama2_src/data_preprocess.py
```
### data augmentation
```
python llama2_src/data_augment.py
```
### concat training data and augmented data
```
python llama2_src/concat_trainset.py
```
### training
```
python llama2_src/train.py
```
### inference
```
python llama2_src/inference.py
```
### data postprocess
```
python llama2_src/data_postprocess.py
```


## Roberta