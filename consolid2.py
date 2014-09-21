import sys
import time

import os

def GetDataFile(fname):
	retrievedData = {}
	retrievedTimes = set()
	data=""
	with open (fname, "r") as myfile:
		data += myfile.read()
		for l in data.split('\n'):
			fields = l.split(',')
			if len(fields) < 3:
				continue
			optime = int(fields[0])
			price = float(fields[1])
			btc = float(fields[2])
			if optime not in retrievedData:
				retrievedData[optime] = []
			retrievedData[optime].append( (price, btc, l) )
	return retrievedData

def MergeData( totalData,mergeData ):
	return [ (f[0], f[1], f[2], f[3]) for f in mergeData if f[0] not in totalTimes ]

def WriteData(data):
	dataK =	data.keys()
	dataK.sort(reverse=True)
	mintime = min(dataK)
	maxtime = max(dataK)

	outfname = "dataconsolid-" + str(mintime) + "-" + str(maxtime) + ".txt"
	f = open(outfname, "w")
	for k in dataK:
		for itm in data[k]:
			f.write( itm[2] + "\n"  )
	f.close()

def maxDiff( data ): 
	dataK = data.keys()
	dataK.sort()
	dataDiffs = [x - dataK[i - 1] for i, x in enumerate(dataK) if i > 0]
	return max(dataDiffs)

completeData = {}
for dirpath,dirname,filenames in os.walk(sys.argv[1]):
	filenames.sort()
	for files in filenames:
		if files.endswith(".txt"):
			retrievedData = GetDataFile( os.path.join(dirpath,files) )
			print "retData ", len(retrievedData), " maxTimeDiff " , maxDiff( retrievedData )
			completeData.update(retrievedData)

print "total maxtimediff: ", maxDiff(completeData)

WriteData(completeData)

quit()

