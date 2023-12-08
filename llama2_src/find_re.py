import pandas as pd
from tqdm import tqdm

if __name__ == '__main__':
    with open('dataset/country.txt', 'r') as f:
        country = f.readlines()
        country_list = [c.strip() for c in country]

    output_file = 'llama2_answer.txt'
    col_names = ['id', 'phi_type', 'start_pos',
                 'end_pos', 'value', 'normalized_value']

    answer_df = pd.read_csv(output_file, sep="\t", names=col_names)
    value_list = answer_df['value'].to_list()
    value_list = list(set([x for x in value_list if str(x) != 'nan']))

    col_names = ['id', 'start_pos', 'input', 'output']
    testing_set = pd.read_csv(
        'dataset/processed/line_split/opendid_test_processed.tsv', sep='\t', names=col_names)

    en_number_dict = {'one': '1', 'two': '2', 'three': '3', 'four': '4', 'five': '5', 'six': '6', 'seven': '7',
                      'eight': '8', 'nine': '9', 'ten': '10', '0-1': '0.5', '1-2': '1.5', '2-3': '2.5', '3-4': '3.5', '4-5': '4.5', '5-6':
                      '5.5', '6-7': '6.5', '7-8': '7.5', '8-9': '8.5', '9-10': '9.5'}
    time_format_dict = {'day': 'D', 'week': 'W', 'wk': 'W',
                        'month': 'M', 'year': 'Y',  'yr': 'Y'}
    set_dict = {'once': '1', 'twice': '2', 'thrice': '3', 'one time': '1', 'two times': '2', 'three times': '3', 'four times': '4',
                'five times': '5', 'six times': '6', 'seven times': '7', 'eight times': '8', 'nine times': '9', 'ten times': '10'}

    for row_i, row in tqdm(testing_set.iterrows(), total=testing_set.shape[0]):
        # find set
        for s in list(set_dict.keys()):
            if s in row['input']:
                pos = row['input'].find(s, 0)
                if row['input'][pos-1] == ' ' and row['input'][pos+len(s)] == ' ':
                    start_pos = row['start_pos'] + pos
                    end_pos = row['start_pos'] + pos + len(s)
                    normalized_s = 'R'+set_dict[s]
                    seq = f"{row['id']}\tSET\t{start_pos}\t{end_pos}\t{s}\t{normalized_s}\n"
                    with open(output_file, 'a', encoding='utf-8') as fw:
                        fw.write(seq)
        # find country
        for c in country_list:
            if c in row['input']:
                pos = row['input'].find(c, 0)
                start_pos = row['start_pos'] + pos
                end_pos = row['start_pos'] + pos + len(c)
                if any(c in a for a in value_list):
                    continue
                else:
                    if not row['input'][pos+len(c)].isalpha():
                        seq = f"{row['id']}\tCOUNTRY\t{start_pos}\t{end_pos}\t{c}\n"
                        with open(output_file, 'a', encoding='utf-8') as fw:
                            fw.write(seq)

        # find duration
        time_format_keys = list(time_format_dict.keys())
        for key in time_format_keys:
            if key in row['input']:
                pos = -1
                while True:
                    pos = row['input'].find(key, pos+1)
                    if pos == -1:
                        break
                    if row['input'][pos-1] != ' ' or row['input'][pos+len(key):pos+len(key)+10].find('old', 0) > 0:
                        # pos = row['input'].find(key, pos+1)
                        # if pos == -1:
                        #     break
                        # else:
                        continue
                    st_pos = pos - 2
                    if st_pos < 0:
                        break
                    while True:
                        if row['input'][st_pos] == ' ':
                            st_pos = st_pos+1
                            break
                        else:
                            st_pos -= 1
                    if row['input'][pos + len(key)] == 's':
                        output = row['input'][st_pos:pos + len(key)+1]
                    else:
                        output = row['input'][st_pos:pos + len(key)]
                    start_pos = row['start_pos'] + st_pos
                    end_pos = start_pos + len(output)
                    time_value = row['input'][st_pos:pos-1]
                    if time_value.isnumeric():
                        normalized_output = 'P' + \
                            time_value + time_format_dict[key]
                        seq = f"{row['id']}\tDURATION\t{start_pos}\t{end_pos}\t{output}\t{normalized_output}\n"
                        with open(output_file, 'a', encoding='utf-8') as fw:
                            fw.write(seq)
                    elif time_value in list(en_number_dict.keys()):
                        normalized_output = 'P' + \
                            en_number_dict[time_value] + \
                            time_format_dict[key]
                        seq = f"{row['id']}\tDURATION\t{start_pos}\t{end_pos}\t{output}\t{normalized_output}\n"
                        with open(output_file, 'a', encoding='utf-8') as fw:
                            fw.write(seq)
                    else:
                        continue
