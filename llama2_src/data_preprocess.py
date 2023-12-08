import os
import pandas as pd
import argparse


def split_txt_to_passages(filepath):
    with open(filepath) as f:
        txt = f.read()

    pos = 0
    passages = []
    start_pos = []
    end_pos = []
    while True:
        last_pos = pos
        pos = txt.find('\n\n', pos+1)
        if pos == -1:
            break
        else:
            passage = txt[last_pos:pos]
            passages.append(passage)
            start_pos.append(last_pos)
            end_pos.append(pos)

    return start_pos, end_pos, passages


def process_all_files(need_process_folder_list, need_process_answer_files):
    for i, folder in enumerate(need_process_folder_list):
        if len(need_process_answer_files) == 0:
            annos_dict = {}
        else:
            anno_path = 'dataset/' + need_process_answer_files[i]
            with open(anno_path, 'r', encoding='utf-8-sig') as fr:
                anno_lines = fr.readlines()
            annos_dict = process_annotation_file(anno_lines)

        all_seq_pairs = []
        for file in os.listdir('dataset/'+folder):
            filepath = 'dataset/' + folder + '/' + file
            file_id = file.replace('.txt', '')
            all_seq_pairs.extend(process_medical_report(
                filepath, file_id,  annos_dict))

        folder_name = folder[folder.find('/')+1:]
        tsv_output_path = 'dataset/processed/line_split/' + folder_name + '_processed.tsv'
        with open(tsv_output_path, 'w', encoding='utf-8') as fw:
            for seq_pair in all_seq_pairs:
                fw.write(seq_pair)


def process_medical_report_5_lines(filepath, file_id, annos_dict):
    with open(filepath) as f:
        sents = f.readlines()
    article = "".join(sents)
    bounary, item_idx, temp_seq, seq_pairs = 0, 0, "", []
    new_line_idx = 0
    new_line_count = 0
    for w_idx, word in enumerate(article):
        if word == '\n':
            new_line_idx = w_idx + 1
            new_line_count += 1
            if article[bounary:new_line_idx] == '\n':
                continue

            if new_line_count == 5:
                sentence = article[bounary:new_line_idx].replace(
                    '\t', ' ').replace('\n', ' ')
                temp_seq = temp_seq.strip('\\n')
                if temp_seq == "":
                    temp_seq = "PHI:Null"
                seq_pair = f"{file_id}\t{bounary}\t{sentence}\t{temp_seq}\n"
                # seq_pair = special_tokens_dict['bos_token'] + article[bounary:new_line_idx] + special_tokens_dict['sep_token'] + temp_seq + special_tokens_dict['eos_token']
                bounary = new_line_idx
                seq_pairs.append(seq_pair)
                temp_seq = ""
                new_line_count = 0
        if w_idx == annos_dict[file_id][item_idx]['st_idx']:
            phi_key = annos_dict[file_id][item_idx]['phi']
            phi_value = annos_dict[file_id][item_idx]['entity']
            if 'normalize_time' in annos_dict[file_id][item_idx]:
                temp_seq += f"{phi_key}:{phi_value}=>{annos_dict[file_id][item_idx]['normalize_time']}\\n"
            else:
                temp_seq += f"{phi_key}:{phi_value}\\n"
            if item_idx == len(annos_dict[file_id]) - 1:
                continue
            item_idx += 1
    return seq_pairs


def process_medical_report(filepath, file_id, annos_dict):
    '''
    處理單個病理報告

    output : 處理完的 sequence pairs
    '''

    with open(filepath) as f:
        sents = f.readlines()
    article = "".join(sents)

    bounary, item_idx, temp_seq, seq_pairs = 0, 0, "", []
    new_line_idx = 0
    continue_word = ['firstname\n', 'middlename\n', 'lastname\n']
    for w_idx, word in enumerate(article):
        if word == '\n':
            new_line_idx = w_idx + 1
            if article[bounary:new_line_idx] == '\n':
                bounary = new_line_idx
                continue
            if article[bounary:new_line_idx].lower() in continue_word:
                print(article[bounary:new_line_idx])
                continue
            if temp_seq == "":
                temp_seq = "PHI:Null\\n"
            sentence = article[bounary:new_line_idx].replace(
                '\t', ' ').replace('\n', ' ')
            temp_seq = temp_seq[:-2]
            seq_pair = f"{file_id}\t{bounary}\t{sentence}\t{temp_seq}\n"
            bounary = new_line_idx
            seq_pairs.append(seq_pair)
            temp_seq = ""
        if len(annos_dict) != 0:
            if w_idx == annos_dict[file_id][item_idx]['st_idx']:
                phi_key = annos_dict[file_id][item_idx]['phi']
                phi_value = annos_dict[file_id][item_idx]['entity']
                if 'normalize_time' in annos_dict[file_id][item_idx]:
                    temp_seq += f"{phi_key}:{phi_value}=>{annos_dict[file_id][item_idx]['normalize_time']}\\n"
                else:
                    temp_seq += f"{phi_key}:{phi_value}\\n"
                if item_idx == len(annos_dict[file_id]) - 1:
                    continue
                item_idx += 1
    return seq_pairs


def process_annotation_file(lines):
    '''
    處理anwser.txt 標註檔案

    output:annotation dicitonary
    '''
    print("process annotation file...")
    entity_dict = {}
    for line in lines:
        items = line.strip('\n').split('\t')
        if len(items) == 5:
            item_dict = {
                'phi': items[1],
                'st_idx': int(items[2]),
                'ed_idx': int(items[3]),
                'entity': items[4],
            }
        elif len(items) == 6:
            item_dict = {
                'phi': items[1],
                'st_idx': int(items[2]),
                'ed_idx': int(items[3]),
                'entity': items[4],
                'normalize_time': items[5],
            }
        if items[0] not in entity_dict:
            entity_dict[items[0]] = [item_dict]
        else:
            entity_dict[items[0]].append(item_dict)
    print("annotation file done")
    return entity_dict


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--test", help="preprocess testing set",
                        action="store_true")
    args = parser.parse_args()
    if args.test:
        need_process_folder_list = ['opendid_test/opendid_test']
        process_all_files(need_process_folder_list, [])
    else:
        need_process_folder_list = ['First_Phase_Release(Correction)/First_Phase_Text_Dataset',
                                    'First_Phase_Release(Correction)/Validation_Release', 'Second_Phase_Dataset/Second_Phase_Text_Dataset']
        need_process_answer_files = [
            'First_Phase_Release(Correction)/answer.txt', 'validation_answer.txt', 'Second_Phase_Dataset/answer.txt']
        process_all_files(need_process_folder_list, need_process_answer_files)
