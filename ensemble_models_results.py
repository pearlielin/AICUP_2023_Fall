import pandas as pd


if __name__ == '__main__':
    col_names = ['id', 'phi_type', 'start_pos',
                 'end_pos', 'value', 'normalized_value']
    roberta_answer = pd.read_csv(
        'roberta_answer.txt', sep="\t", names=col_names)
    roberta_type = ['IDNUM', 'MEDICALRECORD', 'PATIENT', 'STREET', 'URL',
                    'CITY', 'ZIP', 'HOSPITAL', 'DOCTOR', 'PHONE', 'AGE']
    roberta_answer = roberta_answer[roberta_answer['phi_type'].isin(
        roberta_type)]

    llama2_answer = pd.read_csv(
        'llama2_answer.txt', sep="\t", names=col_names)
    llama2_type = ['STATE', 'DATE', 'DEPARTMENT', 'TIME',
                   'ORGANIZATION', 'COUNTRY', 'LOCATION-OTHER', 'DURATION']
    llama2_answer = llama2_answer[llama2_answer['phi_type'].isin(
        llama2_type)]

    results = pd.concat([roberta_answer, llama2_answer])
    results.to_csv('answer.txt', sep='\t', index=False, header=False)
