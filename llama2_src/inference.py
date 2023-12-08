from ludwig.api import LudwigModel
import pandas as pd
from tqdm import tqdm

if __name__ == '__main__':

    col_names = ['id', 'start_pos', 'input', 'output']
    path = 'dataset/processed/line_split/opendid_test_processed.tsv'
    testing_set = pd.read_csv(path, sep='\t', names=col_names)
    testing_set['instruction'] = "Find out the Protected Health Information."

    test_output = pd.DataFrame(
        {'id': {}, 'start_pos': {}, 'input': {}, 'output': {}})
    model = LudwigModel.load('results/api_experiment_run/model')

    for row_i, row in tqdm(testing_set.iterrows(), total=testing_set.shape[0]):
        test_example = pd.DataFrame([row])
        predictions = model.predict(dataset=test_example)[0]
        print(f"Input: {row['input']}")
        print(f"Generated Output: {predictions['output_response'][0][0]}")
        print("\n\n")
        test_output.loc[len(test_output)] = [
            row['id'], row['start_pos'], row['input'], predictions['output_response'][0][0]]
        test_output.to_csv('test_output.csv', index=False)
