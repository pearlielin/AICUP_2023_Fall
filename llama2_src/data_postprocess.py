import pandas as pd


result_file = 'test_output.csv'
output_file = 'llama2_answer.txt'

accept_type = ['PATIENT', 'DOCTOR', 'USERNAME', 'PROFESSION', 'ROOM', 'DEPARTMENT', 'HOSPITAL', 'ORGANIZATION', 'STREET', 'CITY',
               'STATE', 'ZIP', 'LOCATION-OTHER', 'AGE', 'DATE', 'TIME', 'PHONE', 'FAX', 'EMAIL', 'URL', 'IPADDR',
               'SSN', 'MEDICALRECORD', 'HEALTHPLAN', 'ACCOUNT', 'LICENSE', 'VECHICLE', 'DEVICE', 'BIOID', 'IDNUM']

if __name__ == '__main__':

    df = pd.read_csv(result_file)
    df = df[df['output'] != 'phi:null']

    for row_i, row in df.iterrows():
        phi_output = row['output']
        pos = -1
        eos = 0
        st = -1
        while True:
            if eos == -1:
                break
            pos = phi_output.find(':', pos+1)
            if pos == -1:
                break
            phi_name = phi_output[eos:pos].upper()

            eos = phi_output.find('\\n', eos)
            if eos == -1:
                phi_value = phi_output[pos+1:]
            elif eos:
                phi_value = phi_output[pos+1:eos]
                eos += 2

            time_id = phi_value.find('=>', 0)
            if time_id > 0:
                phi_normalized_value = phi_value[time_id+2:].upper()
                phi_value = phi_value[:time_id]

            if phi_name == 'DOCTOR' and len(phi_value) == 2:
                phi_value = phi_value.upper()
                st = row['input'].find(phi_value, st+1)
            else:
                st = row['input'].lower().find(phi_value, st+1)
            start_pos = row['start_pos'] + st
            end_pos = start_pos + len(phi_value)
            phi_value = row['input'][st:st+len(phi_value)]
            if phi_name == 'STATE' and phi_value.isnumeric():
                phi_name = 'ZIP'

            if len(phi_value) > 1 and phi_name in accept_type:
                if time_id > 0:
                    seq = f"{row['id']}\t{phi_name}\t{start_pos}\t{end_pos}\t{phi_value}\t{phi_normalized_value}\n"
                else:
                    if phi_name == 'IDNUM' and len(phi_value) < 8:
                        continue
                    seq = f"{row['id']}\t{phi_name}\t{start_pos}\t{end_pos}\t{phi_value}\n"

                with open(output_file, 'a', encoding='utf-8') as fw:
                    fw.write(seq)
