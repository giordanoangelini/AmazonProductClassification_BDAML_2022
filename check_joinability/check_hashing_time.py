import csv
import sys
import os
import pandas as pd
import math
import json
from datasketch import MinHashLSHEnsemble, MinHash
import time
import joinability_options as options
import sys

DEFAULT_DIR = "datasets/"
DEFAULT_DIMENSIONS_DIR="dimensions/"
DEFAULT_COD_DIR = "_cod_lists/"
DEFAULT_ENTRY_FILE = DEFAULT_COD_DIR+"list_sources"
NUM_PERM = 256
NUM_PART = 32

def main(i):
	# initialize. This is still hard-coded.
    s1 = DEFAULT_DIR + options.dataset1
		
    c1 = []

    for col in range(i):
        c1.append(col)

    m1 = MinHash(num_perm=NUM_PERM)

    start = time.time()

    print("\treading files")		
    df1 = pd.read_csv(s1, dtype='unicode',usecols=c1)
    list_df1 = list(df1)

    df1_total = ''

	#Initialize the combined MinHashes. This needs to be done at setup time, not at query time.
    for col in range(len(list_df1)):
        df1_total += (df1[list_df1[col]].astype(str) + " ")

	#update the combined MinHashes
    for i in df1_total:
        m1.update(i.encode('utf8'))
	
    end = time.time()
    hashing_time = end - start

    print("Hashing time:"+str(hashing_time))	

    with open(options.OUTFILE, 'a', encoding='UTF8') as f:
        f.write('\n'+str(hashing_time))
			
if __name__ == "__main__":
    for i in range(1,17):
        main(i)