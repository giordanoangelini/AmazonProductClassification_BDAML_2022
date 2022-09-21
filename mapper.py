import sys
import os
import pandas as pd
import math
import json
from datasketch import MinHashLSHEnsemble, MinHash
import time

DEFAULT_DIR = "datasets/"
DEFAULT_DIMENSIONS_DIR="dimensions/"
DEFAULT_COD_DIR = "_cod_lists/"
DEFAULT_ENTRY_FILE = DEFAULT_COD_DIR+"list_sources"
NUM_PERM = 512
NUM_PART = 32
THRESHOLD = 0.8

def map_file(mydir, filename, suffix):
	print("Initializing the mapper...")
	# Create an LSH Ensemble index with threshold and number of partition settings.
	lshensemble = MinHashLSHEnsemble(threshold=THRESHOLD, num_perm=NUM_PERM, num_part=NUM_PART)

	# Initialize LSHEnsemble
	index = []
	all_dimension_files = [f for f in os.listdir(DEFAULT_DIMENSIONS_DIR) if os.path.isfile(os.path.join(DEFAULT_DIMENSIONS_DIR, f))]
	for f in all_dimension_files:
		# Create the MinHash for the i-th level
		m = MinHash(num_perm=NUM_PERM)
		with open(DEFAULT_DIMENSIONS_DIR+f,"r") as dimFile:
			content=dimFile.read().split("\n")
			# Update the MinHash
			m.update_batch([s.encode('utf8') for s in content])
			#for d in content:
			#	m.update(d.encode('utf8'))	
			index.append(tuple((f,m,len(content))))
			#print(index)
		
	lshensemble.index(index)		

	

	# Read the entry for the input file
	print("Reading source metadata...")
	with open(DEFAULT_ENTRY_FILE,"r") as entryF:
		entries_decoded=json.load(entryF)
		entry = entries_decoded[mydir+filename+"."+suffix]
		#for each column of the data source
		durationsHashing=[]
		durationsQuery=[]
		to_print = []
		for c in range(entry["num_columns"]):
			m1 = MinHash(NUM_PERM)
			with open(DEFAULT_COD_DIR+filename+"."+str(c),"r") as col:
				startTimeHashing = time.time()
				values=col.read().split("\n")
				for v in values:
					m1.update(v.encode('utf8'))
				#m1.update_batch([s.encode('utf8') for s in values])
				durationHashing = time.time() - startTimeHashing
				durationsHashing.append(durationHashing)
				startTimeQuery = time.time()
				for mapping in lshensemble.query(m1, len(values)):		
					print("Column "+str(c)+" -> "+mapping)
					to_print.append("Column "+str(c)+" -> "+mapping)
				durationQuery = time.time() - startTimeQuery
				durationsQuery.append(durationQuery)
		
		with open('test_output/output.' + filename, 'w') as f:
			f.writelines("%s\n" % l for l in to_print)
			print('', file=f)
			for i in range(len(durationsQuery)):
				print("Query time Column " + str(i) + " = " + str(durationsQuery[i]) + "s", file=f)
			print('', file=f)
			sum_durations = sum(durationsHashing)
			print("Sum durations hashing = "+str(sum_durations), file=f)
			print("Avg durations hashing = "+str((sum_durations/len(durationsHashing))), file=f)
			sum_durations_query = sum(durationsQuery)
			print("Sum durations query = "+str(sum_durations_query), file=f)
			print("Avg durations query = "+str((sum_durations_query/len(durationsQuery))), file=f)

		
def read_entries():
	with open(DEFAULT_ENTRY_FILE,"r") as f:
		data_decoded = json.load(f)
		print(data_decoded.keys())


def main():
	# Map single dataset
	if (len(sys.argv)==2 and sys.argv[1]=="list"):
		#List all sources
		with open(DEFAULT_ENTRY_FILE,"r") as f:
			data_decoded=json.load(f)
			for k in data_decoded.keys():
				print(k)
	elif (len(sys.argv)==3 and sys.argv[1]=="source"):
		if(os.path.exists(sys.argv[2])):
			path = sys.argv[2]
			mydir=path[:path.rfind("/")+1]
			filename=path[path.rfind("/")+1:path.rfind(".")]
			suffix=path[path.rfind(".")+1:]
			map_file(mydir,filename,suffix)
		else:
			print("Error: no such file.")
	else:
		print("Error: invalid call. Usage: mapper [list | source sourcename]") 
  
if __name__ == "__main__":
    main()

