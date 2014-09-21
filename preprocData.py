
def preprocessRetData(fname, filt_time):
	retrievedData = {}
	data = ""
	with open (fname, "r") as myfile:
		data += myfile.read()
		for l in data.split('\n'):
			fields = l.split(',')
			if len(fields) < 3:
				continue
			optime = int(fields[0])
			price = float(fields[1])
			btc = float(fields[2])
			if filt_time is not None and optime <= filt_time:
				continue
			if btc < 0.1:
				continue
			if optime not in retrievedData:
				retrievedData[optime] = []
			if len(retrievedData[optime]) == 1:
				if retrievedData[optime][0][1] == price:
					retrievedData[optime][0][2] += btc
					continue
			retrievedData[optime].append( [optime, price, btc] )
	
	retData = []
	for tim in retrievedData:
		retData.append(max(retrievedData[tim], key = lambda x: x[2]))

	return retData

import sys
import pickle

fname_data = sys.argv[1]

filter_time = None
if len(sys.argv[1]) > 2:
	filter_time = int(sys.argv[2])
	
data = preprocessRetData(fname_data,filter_time)

with open("preproc" + fname_data, 'wb') as f:
	pickle.dump(data, f)
