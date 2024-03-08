import json
import random
from os.path import join, dirname


def sample_json(json_file_path, num_dicts = 10):
    with open(json_file_path, 'r') as file:
        data = json.load(file)
        selected_dicts = random.sample(data, min(num_dicts, len(data)))
        return selected_dicts

