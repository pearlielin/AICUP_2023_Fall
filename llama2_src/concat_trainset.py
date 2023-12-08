import pandas as pd

if __name__ == '__main__':

    col_names = ['id', 'start_pos', 'input', 'output']
    df_1 = pd.read_csv(
        'dataset/processed/line_split/First_Phase_Text_Dataset_processed.tsv', sep="\t", names=col_names)
    df_2 = pd.read_csv(
        'dataset/processed/line_split/Second_Phase_Text_Dataset_processed.tsv', sep="\t", names=col_names)
    df_3 = pd.read_csv(
        'dataset/augment_data.tsv', sep="\t", names=col_names)
    df_4 = pd.read_csv(
        'dataset/processed/line_split/Validation_Release_processed.tsv', sep="\t", names=col_names)

    df = pd.concat([df_1, df_2, df_3, df_4])

    df['instruction'] = "Find out the Protected Health Information."
    df.to_csv('dataset/processed/line_split/total_train.tsv',
              sep='\t', index=False)
