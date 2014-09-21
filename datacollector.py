import httplib
import urllib
import time

def getData( endTime ):
	conn = httplib.HTTPConnection("api.bitcoincharts.com")
	if endTime is None:
		conn.request("POST", "/v1/trades.csv?symbol=btceUSD")
	else:
		conn.request("POST", "/v1/trades.csv?symbol=btceUSD&end=" + endTime)
	response = conn.getresponse()
	if response.status != 200:
		return ""
	return response.read()

def getLastItem(data):
	last = ""
	for l in data.split('\n'):
		last = l
	parts = last.split(',')
	return parts[0]

lastTime = None
totalResp = ""
while True:
	response = getData(lastTime)
	if len(response) < 100:
		break
	lastTime = getLastItem(response)
	print lastTime
	totalResp += "\n" + response
	time.sleep(10)

f = open("data-" + lastTime + ".txt", "w")
f.write( totalResp  )      # str() converts to string
f.close()
