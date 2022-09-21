import random
import csv
import random 
import string 
import os
import dataset_options as options

DIMENSIONS_DIR = 'dimensions/'
NOISE_DIR = 'generators/datasets_generator/noise/'

# Define dimensions dictionary from 'dimensions/' folder
dimensions = {}
dimension_files = [f for f in os.listdir(DIMENSIONS_DIR) if os.path.isfile(os.path.join(DIMENSIONS_DIR, f))]
for dimension in dimension_files:
    with open(DIMENSIONS_DIR + dimension, 'r', encoding='UTF8') as f:
        dimensions[dimension] = f.readlines()

# Calculate the number of noisy rows (from percentage)
def noisy_rows(noice_percent):
    return int((options.NUM_ROWS/100)*noice_percent)

# Create a random entry in the dataset
def random_row():
    row = []
    for i in options.COLUMNS:
        row.append(random.choice(dimensions[i])[:-1])
    return row

noise_strings = []
with open(NOISE_DIR + 'Noise.randomity_' + str(options.noise_randomity), 'r', encoding='UTF8') as f:
    noise_strings = f.readlines()

def get_pseudorandom_string():
    return random.choice(noise_strings)[:-1]

with open(options.FILENAME, 'w', encoding='UTF8') as f:
    writer = csv.writer(f)
    random_rows = []
    for i in range(options.NUM_ROWS):
        random_rows.append(random_row())
    for i in range(len(options.COLUMNS)):
        list_index = random.sample(range(options.NUM_ROWS), noisy_rows(options.noise))
        for j in list_index:
            random_rows[j][i] = get_pseudorandom_string()
    writer.writerows(random_rows)