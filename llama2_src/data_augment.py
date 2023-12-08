import random


def location_other_augment():
    seq_pairs = []
    prefix = ['P.O.  BOX', 'P.O. BOX', 'PO BOX', 'PO  BOX']
    number = random.randint(100, 9999)
    phi_type = 'LOCATION-OTHER:'
    for i in range(0, 200):
        idx = random.randint(0, 3)
        input = prefix[idx] + ' ' + str(number)
        output = phi_type+input
        file_id = 'augment'
        bounary = 0
        seq_pair = f"{file_id}\t{bounary}\t{input}\t{output}\n"
        seq_pairs.append(seq_pair)
    return seq_pairs


def duration_augment():
    seq_pairs = []
    phi_type = 'DURATION:'
    word = ['for', 'history', 'ago', 'pack history', 'of']
    en_number_dict = {'one': '1', 'two': '2', 'three': '3', 'four': '4', 'five': '5', 'six': '6', 'seven': '7',
                      'eight': '8', 'nine': '9', 'ten': '10', '4-5': '4.5', '9-10': '9.5', '3-4': '3.5', '6-7': '6.5'}
    time_format_dict = {'day': 'D', 'days': 'D', 'week': 'W', 'weeks': 'W', 'wks': 'W',
                        'month': 'M', 'months': 'M', 'year': 'Y', 'years': 'Y', 'yr': 'Y', 'yrs': 'Y'}
    for i in range(0, 100):
        word_idx = random.randint(0, 4)
        en_number_idx = random.randint(0, 13)
        en_number = list(en_number_dict.keys())[en_number_idx]
        time_format_idx = random.randint(0, 10)
        time_format = list(time_format_dict.keys())[time_format_idx]
        file_id = 'augment'
        bounary = 0
        if word_idx == 0:
            input = word[word_idx] + ' ' + en_number + ' ' + time_format
            output = phi_type + en_number + ' ' + time_format + '=>P' + en_number_dict[en_number] + \
                time_format_dict[time_format]
            seq_pair = f"{file_id}\t{bounary}\t{input}\t{output}\n"
            seq_pairs.append(seq_pair)
        else:
            input = en_number + ' ' + time_format + ' ' + word[word_idx]
            output = phi_type + en_number + ' ' + time_format + '=>P' + en_number_dict[en_number] + \
                time_format_dict[time_format]
            seq_pair = f"{file_id}\t{bounary}\t{input}\t{output}\n"
            seq_pairs.append(seq_pair)

    for i in range(0, 100):
        word_idx = random.randint(0, 4)
        num = random.randint(0, 40)
        time_format_idx = random.randint(0, 10)
        time_format = list(time_format_dict.keys())[time_format_idx]
        if word_idx == 0:
            input = word[word_idx] + ' ' + str(num) + ' ' + time_format
            output = phi_type + str(num) + ' ' + time_format + \
                '=>P' + str(num) + time_format_dict[time_format]
            seq_pair = f"{file_id}\t{bounary}\t{input}\t{output}\n"
            seq_pairs.append(seq_pair)
        else:
            input = str(num) + ' ' + time_format + ' ' + word[word_idx]
            output = phi_type + str(num) + ' ' + time_format + \
                '=>P' + str(num) + time_format_dict[time_format]
            seq_pair = f"{file_id}\t{bounary}\t{input}\t{output}\n"
            seq_pairs.append(seq_pair)

    return seq_pairs


def time_augment():
    seq_pairs = []
    for i in range(0, 200):
        hour = random.randint(1, 23)
        minute = random.randint(1, 59)
        output_minute = '0'+str(minute) if minute < 10 else str(minute)
        if hour > 12:
            m = 'pm'
            output_hour = hour
        else:
            m = random.choice(['am', 'pm', ''])
            if m == 'pm':
                output_hour = hour+12
            else:
                output_hour = '0'+str(hour) if hour < 10 else str(hour)
        date = random.randint(1, 30)
        output_date = '0'+str(date) if date < 10 else str(date)
        month = random.randint(1, 12)
        output_month = '0'+str(month) if month < 10 else str(month)
        year = random.randint(10, 25)
        st = random.choice([':', '.', ''])
        s = random.choice(['.', '/'])
        # input = format.replace('[hour]',hour).replace('[minute]',minute).replace('[date]',date).replace('[month]',month).replace('[year]',year).replace
        format1 = f"{hour}{st}{minute}{m} on {date}{s}{month}{s}{year}"
        format2 = f"{date}{s}{month}{s}{year} at {hour}{st}{minute}{m}"
        input = random.choice([format1, format2])
        output = f"TIME:{input}=>20{year}-{output_month}-{output_date}T{output_hour}:{output_minute}"
        file_id = 'augment'
        bounary = 0
        seq_pair = f"{file_id}\t{bounary}\t{input}\t{output}\n"
        seq_pairs.append(seq_pair)
        # print(seq_pairs)
    return seq_pairs


if __name__ == '__main__':
    location_other = location_other_augment()
    duration = duration_augment()
    time = time_augment()

    with open('dataset/augment_data.tsv', 'w', encoding='utf-8') as fw:
        for seq_pair in location_other:
            fw.write(seq_pair)

    with open('dataset/augment_data.tsv', 'a', encoding='utf-8') as fw:
        for seq_pair in duration:
            fw.write(seq_pair)

    with open('dataset/augment_data.tsv', 'a', encoding='utf-8') as fw:
        for seq_pair in time:
            fw.write(seq_pair)
