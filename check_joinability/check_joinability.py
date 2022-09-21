import sys
import os
import pandas as pd
import math
import json
from datasketch import MinHashLSHEnsemble, MinHash
import time
import joinability_options as options

DEFAULT_DIR = "datasets/"
DEFAULT_DIMENSIONS_DIR="dimensions/"
DEFAULT_COD_DIR = "_cod_lists/"
DEFAULT_ENTRY_FILE = DEFAULT_COD_DIR+"list_sources"
NUM_PERM = 256
NUM_PART = 32

def main():
	# initialize. This is still hard-coded.
	s1 = DEFAULT_DIR + options.dataset1
	s2 = DEFAULT_DIR + options.dataset2
		
	c1 = options.columns1
	c2 = options.columns2

	m1 = MinHash(num_perm=NUM_PERM)
	m2= MinHash(num_perm=NUM_PERM)
	
	print("\treading files")		
	df1 = pd.read_csv(s1, dtype='unicode',usecols=c1)
	list_df1 = list(df1)
	df2 = pd.read_csv(s2, dtype='unicode',usecols=c2)
	list_df2 = list(df2)

	#Initialize the combined MinHashes. This needs to be done at setup time, not at query time.
	df1_total=df1[list_df1[0]].astype(str) + " " + df1[list_df1[1]].astype(str)
	df2_total=df2[list_df2[0]].astype(str) + " " + df2[list_df2[1]].astype(str)
	
	start = time.time()
	
	#update the combined MinHashes
	print("\tcreating hashes")
	startm1 = time.time()
	for i in df1_total:
			m1.update(i.encode('utf8'))
	print("Time m1: "+str(time.time()-startm1)+"\n")
	
	startm2 = time.time()
	for i in df2_total:
			m2.update(i.encode('utf8'))				
	print("Time m2: "+str(time.time()-startm2)+"\n")

	end_hashing = time.time()
	
	print("\tchecking joinability")
	stop = False
	first = 0.0
	last = 1.0
	sure = 0
	#The termination criteria for the dychotomic search is that we got a delta <0.05
	while first<=(last-0.049):
		found = False
		q = (first+last)/2
		lshensemble = MinHashLSHEnsemble(threshold=q, num_perm=NUM_PERM, num_part=NUM_PART)
		lshensemble.index([("s1",m1,len(df1_total))])
		#lshensemble.index([("s2",m2,len(df2_total))])
		print("First = "+str(first)+" Last: "+str(last)+"\n")
		for k in lshensemble.query(m2,len(df2_total)):
			print(k)
			print("Result:\n\tsources joinable with containment > "+str(q))
			found = True
		if(found):
			first = q
			sure = q
		else:
			last = q	
	
	print("Result:\n\tsources joinable with containment > "+str(sure))
		
	final_time = time.time()
	hashing_time = end_hashing - start
	querying_time = final_time - end_hashing
	print("Hashing time:"+str(hashing_time))	
	print("Querying time:"+str(querying_time))	
	print("Total time:"+str(hashing_time + querying_time))	
	
			
if __name__ == "__main__":
    main()