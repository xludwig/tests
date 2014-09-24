##### Generic Funcs
import random
import time
import pickle


#Para probar en la realidad progs de test3.py


#### Problem Specific
def gen_context( rundata, runnum, b_bal, d_bal, last_b_d, last_s_d, last_b_b, last_s_b, last_b_cot, last_s_cot, last_res, last_cot, curr_cot ):
	context = {}
	context["last_data"] = rundata[:runnum + 1]
	context["runnum"] = runnum
	context["bal_b"] = b_bal
	context["bal_d"] = d_bal
	context["last_b_d"] = last_b_d
	context["last_s_d"] = last_s_d
	context["last_b_b"] = last_b_b
	context["last_s_b"] = last_s_b
	context["last_b_cot"] = last_b_cot
	context["last_s_cot"] = last_s_cot
	context["last_res"] = last_res
	context["last_cot"] = last_cot
	context["curr_cot"] = curr_cot
	return context
	
def evalFitness( prog, rundata, print_data ):
	b_bal = .02
	d_bal = 0
	
	# Tomo -100 a -10 como % ven
	# Tomo 10 a 100 como % comp
	# Tomo -10 a 10 como no action
	# fuera de rango redondeo a max o min
	
	runnum = 0
	last_b_d = 0
	last_s_d = 0
	last_b_b = 0
	last_s_b = 0
	last_b_cot = 0
	last_s_cot = 0
	last_res = 0
	last_cot = 0
	for dcomplete in rundata:
		if runnum % 1000 == 0:
			sys.stdout.write("-")
    			sys.stdout.flush()
	
		d = dcomplete[1]
		cont = gen_context( rundata, runnum, b_bal, d_bal, last_b_d, last_s_d, last_b_b, last_s_b, last_b_cot, last_s_cot, last_res, last_cot, d ) 
		res = prog.execute( cont )
		if res < -10:
			if res < -100: res = -100
			delta = b_bal * ( -res / 100 )
			if delta >= 0.01:
				if delta > 0.1:
					delta = 0.1
				d_adj = d * 0.995
				d_bal += delta * d_adj * 0.998
				b_bal -= delta
				last_s_cot = d_adj
				last_s_d = delta * d_adj
				last_s_b = delta
				if print_data: print runnum, "[", (b_bal * d + d_bal) ,"] V: ", res, "cot: ", d ,"D: ", d_bal, "B: ", b_bal
		elif res > 10:
			if res > 100: res = 100
			delta = d_bal * ( res / 100 )
			d_adj = d * 1.005
			delta_btc = delta/d_adj
			if delta_btc >= 0.01:
				if delta_btc > 0.1:
					delta_btc = 0.1
				b_bal += delta_btc * 0.998
				d_bal -= delta_btc * d_adj
				last_b_cot = d_adj
				last_b_d = delta
				last_b_b = delta_btc
				if print_data: print runnum, "[", (b_bal * d + d_bal) ,"] C: ", res, "cot: ", d ,"D: ", d_bal, "B: ", b_bal
		last_res = res
		last_cot = d
		runnum += 1

	return b_bal * rundata[len(rundata)-1][1] + d_bal

class generic_func:
	def __init__(self):
		self.num_childs = 2
		self.child = []

	def getParNum(self, parNum):
		return self.child[parNum] 
	
	def setParNum(self, parNum, node):
		self.child[parNum] = node

	def addchild( self, child ):
		self.child.append( child )


class func_root(generic_func):
	def __init__(self):
		generic_func.__init__(self)
		self.num_childs = 1
	def execute( self, context ):
		return self.child[0].execute( context )


class generic_term:
	def __init__(self):
		self.num_childs = 0
		self.child = []
	def addchild( self, child ):
		pass

#Funcs: ( 4: ( ifless, iflesseq, ifmore, ifmoreeq, ifeq), 3: ( if ), 2: ( + - * / > < >= <= == && || prev_delta_x_y), 1 : ( prev_cot, prev_delta ) )

##### 4 pars

class func_ifless(generic_func):
	def __init__(self):
		generic_func.__init__(self)
		self.num_childs = 4

	def execute( self, context ):
		if self.child[0].execute( context ) < self.child[1].execute( context ):
			return self.child[2].execute( context )
		else:
			return self.child[3].execute( context )

class func_iflesseq(generic_func):
	def __init__(self):
		generic_func.__init__(self)
		self.num_childs = 4

	def execute( self, context ):
		if self.child[0].execute( context ) <= self.child[1].execute( context ):
			return self.child[2].execute( context )
		else:
			return self.child[3].execute( context )


class func_ifmore(generic_func):
	def __init__(self):
		generic_func.__init__(self)
		self.num_childs = 4

	def execute( self, context ):
		if self.child[0].execute( context ) > self.child[1].execute( context ):
			return self.child[2].execute( context )
		else:
			return self.child[3].execute( context )

class func_ifmoreeq(generic_func):
	def __init__(self):
		generic_func.__init__(self)
		self.num_childs = 4

	def execute( self, context ):
		if self.child[0].execute( context ) >= self.child[1].execute( context ):
			return self.child[2].execute( context )
		else:
			return self.child[3].execute( context )

class func_ifeq(generic_func):
	def __init__(self):
		generic_func.__init__(self)
		self.num_childs = 4

	def execute( self, context ):
		if self.child[0].execute( context ) == self.child[1].execute( context ):
			return self.child[2].execute( context )
		else:
			return self.child[3].execute( context )

#### 3 pars

class func_if(generic_func):
	def __init__(self):
		generic_func.__init__(self)
		self.num_childs = 3

	def execute( self, context ):
		if self.child[0].execute( context ) != 0:
			return self.child[1].execute( context )
		else:
			return self.child[2].execute( context )

#### 2 pars

class func_plus(generic_func):
	def __init__(self):
		generic_func.__init__(self)
	def execute( self, context ):
		a = self.child[0].execute( context )
		b = self.child[1].execute( context )
		try:		
			return a + b
		except:
			return a

class func_minus(generic_func):
	def __init__(self):
		generic_func.__init__(self)
	def execute( self, context ):
		a = self.child[0].execute( context )
		b = self.child[1].execute( context )
		try:		
			return a - b
		except:
			return b

class func_por(generic_func):
	def __init__(self):
		generic_func.__init__(self)
	def execute( self, context ):
		a = self.child[0].execute( context )
		b = self.child[1].execute( context )
		try:		
			return a * b
		except:
			return a

class func_div(generic_func):
	def __init__(self):
		generic_func.__init__(self)
	def execute( self, context ):
		a = self.child[0].execute( context )
		b = self.child[1].execute( context )
		try:		
			return a / b
		except:
			return b

class func_less(generic_func):
	def __init__(self):
		generic_func.__init__(self)
	def execute( self, context ):
		if self.child[0].execute( context ) < self.child[1].execute( context ):
			return 1
		else:
			return 0
		
class func_lesseq(generic_func):
	def __init__(self):
		generic_func.__init__(self)
	def execute( self, context ):
		if self.child[0].execute( context ) <= self.child[1].execute( context ):
			return 1
		else:
			return 0

class func_more(generic_func):
	def __init__(self):
		generic_func.__init__(self)
	def execute( self, context ):
		if self.child[0].execute( context ) > self.child[1].execute( context ):
			return 1
		else:
			return 0

class func_moreeq(generic_func):
	def __init__(self):
		generic_func.__init__(self)
	def execute( self, context ):
		if self.child[0].execute( context ) >= self.child[1].execute( context ):
			return 1
		else:
			return 0

class func_eq(generic_func):
	def __init__(self):
		generic_func.__init__(self)
	def execute( self, context ):
		if self.child[0].execute( context ) == self.child[1].execute( context ):
			return 1
		else:
			return 0

class func_and(generic_func):
	def __init__(self):
		generic_func.__init__(self)
	def execute( self, context ):
		if ( self.child[0].execute( context ) != 0 ) and ( self.child[1].execute( context ) != 0 ):
			return 1
		else:
			return 0

class func_or(generic_func):
	def __init__(self):
		generic_func.__init__(self)
	def execute( self, context ):
		if ( self.child[0].execute( context ) != 0 ) or ( self.child[1].execute( context ) != 0 ):
			return 1
		else:
			return 0

class func_prev_delta_x_y(generic_func):
	def __init__(self):
		generic_func.__init__(self)
	def execute( self, context ):
		x = self.child[0].execute( context )
		y = self.child[1].execute( context )
		last_data = context["last_data"]
		len_data = len(last_data) - 1
		if len_data < 0:
			return 0
		if x < 0: x = 0
		if y < 0: y = 0
		if x > len_data: x = len_data
		if y > len_data: y = len_data
		return last_data[int(y)][1] - last_data[int(x)][1]

#### 1 par

class func_prev_cot(generic_func):
	def __init__(self):
		generic_func.__init__(self)
		self.num_childs = 1

	def execute( self, context ):
		x = self.child[0].execute( context )
		last_data = context["last_data"]
		len_data = len(last_data) - 1
		if len_data < 0:
			return 0
		if x < 0: x = 0
		if x > len_data: x = len_data
		return last_data[int(x)][1]

class func_prev_delta(generic_func):
	def __init__(self):
		generic_func.__init__(self)
		self.num_childs = 1

	def execute( self, context ):
		x = self.child[0].execute( context )
		last_data = context["last_data"]
		len_data = len(last_data) - 1
		if len_data < 0:
			return 0
		if x < 0: x = 0
		if x > len_data - 1: x = len_data - 1
		a = last_data[len_data][1]
		b = last_data[int(x)][1]
		return a - b

#####################################
#####################################
##### Term

#Term: ( 0, 1, 2, 3, random_const_100, random_const_1000, last_b_d, last_s_d, last_b_b, last_s_b, last_b_cot, last_s_cot, last_res, last_cot, bal_d, bal_b, runnum )

class term_zero(generic_term):
	def __init__(self):
		generic_term.__init__(self)
	def execute( self, context ):
		return 0

class term_one(generic_term):
	def __init__(self):
		generic_term.__init__(self)
	def execute( self, context ):
		return 1

class term_two(generic_term):
	def __init__(self):
		generic_term.__init__(self)
	def execute( self, context ):
		return 2

class term_three(generic_term):
	def __init__(self):
		generic_term.__init__(self)
	def execute( self, context ):
		return 3
		
class term_random_const_100(generic_term):
	def __init__(self):
		generic_term.__init__(self)
		self.num = random.randint(0,100)
	def execute( self, context ):
		return self.num

class term_random_const_1000(generic_term):
	def __init__(self):
		generic_term.__init__(self)
		self.num = random.randint(0,1000)
	def execute( self, context ):
		return self.num

class term_last_b_d(generic_term):
	def __init__(self):
		generic_term.__init__(self)
	def execute( self, context ):
		return context["last_b_d"]

class term_last_s_d(generic_term):
	def __init__(self):
		generic_term.__init__(self)
	def execute( self, context ):
		return context["last_s_d"]

class term_last_b_b(generic_term):
	def __init__(self):
		generic_term.__init__(self)
	def execute( self, context ):
		return context["last_b_b"]

class term_last_s_b(generic_term):
	def __init__(self):
		generic_term.__init__(self)
	def execute( self, context ):
		return context["last_s_b"]

class term_last_b_cot(generic_term):
	def __init__(self):
		generic_term.__init__(self)
	def execute( self, context ):
		return context["last_b_cot"]

class term_last_s_cot(generic_term):
	def __init__(self):
		generic_term.__init__(self)
	def execute( self, context ):
		return context["last_s_cot"]

class term_last_res(generic_term):
	def __init__(self):
		generic_term.__init__(self)
	def execute( self, context ):
		return context["last_res"]

class term_last_cot(generic_term):
	def __init__(self):
		generic_term.__init__(self)
	def execute( self, context ):
		return context["last_cot"]

class term_curr_cot(generic_term):
	def __init__(self):
		generic_term.__init__(self)
	def execute( self, context ):
		return context["curr_cot"]

class term_curr_val(generic_term):
	def __init__(self):
		generic_term.__init__(self)
	def execute( self, context ):
		return context["bal_b"] * context["curr_cot"] + context["bal_d"]

class term_bal_b(generic_term):
	def __init__(self):
		generic_term.__init__(self)
	def execute( self, context ):
		return context["bal_b"]

class term_bal_d(generic_term):
	def __init__(self):
		generic_term.__init__(self)
	def execute( self, context ):
		return context["bal_d"]

class term_runnum(generic_term):
	def __init__(self):
		generic_term.__init__(self)
	def execute( self, context ):
		return context["runnum"]

class term_timediff(generic_term):
	def __init__(self):
		generic_term.__init__(self)
	def execute( self, context ):
		last_data = context["last_data"]
		len_data = len(last_data) - 1
		if len_data < 0:
			return 0
		if len_data < 1:
			return last_data[len_data][0]
		return last_data[len_data][0] - last_data[len_data - 1][0]

class term_curr_vol(generic_term):
	def __init__(self):
		generic_term.__init__(self)
	def execute( self, context ):
		last_data = context["last_data"]
		if len(last_data) < 1:
			return 0
		len_data = len(last_data) - 1
		return last_data[len_data][2]
	
	
		return context["runnum"]

class term_curr_vol_diff(generic_term):
	def __init__(self):
		generic_term.__init__(self)
	def execute( self, context ):
		last_data = context["last_data"]
		len_data = len(last_data) - 1
		if len_data < 0:
			return 0
		if len_data < 1:
			return last_data[len_data][2]
		return last_data[len_data][2] - last_data[len_data - 1][2]

class term_curr_cot_diff(generic_term):
	def __init__(self):
		generic_term.__init__(self)
	def execute( self, context ):
		last_data = context["last_data"]
		len_data = len(last_data) - 1
		if len_data < 0:
			return 0
		if len_data < 1:
			return last_data[len_data][1]
		return last_data[len_data][1] - last_data[len_data - 1][1]


#######################################################################################################


import httplib
import urllib
import json
import hashlib
import hmac
import time
import sys

# Replace these with your own API key data
#
BTC_api_key = "EPZRC7N8-ZNOBS7ZI-43M2QH87-78YB9F9U-AY347DJQ"

BTC_api_secret = "978a8895b69161308553417fc9d1d7ac42dbcf8e6248e5df0a6068a1d6c7c9dc"
#
# Come up with your own method for choosing an incrementing nonce
#

def executeJSONUrl( path, retryOnExcept ):
	while True:
		try:
			conn = httplib.HTTPSConnection("btc-e.com")
			conn.request("POST", path)
			response = conn.getresponse()
			break
		except Exception:
			sys.stdout.write("E")
			sys.stdout.flush()
			if not retryOnExcept:
				return None
			else:
				time.sleep(5)
		
		if response.status != 200 and not retryOnExcept:
			return None
	jres = json.load(response)
	return jres

def getBuySellPrices():
	jres = executeJSONUrl( "/api/2/1/ticker", True )
	if jres == None:
		return None, None
	sell = jres[u'ticker'][u'sell']
	buy = jres[u'ticker'][u'buy']
	return buy, sell


import calendar
import datetime
def get_nonce():
	nonce = calendar.timegm(datetime.datetime.now().timetuple())
	nonce = (nonce % 1000000000) + 1100000000
	return nonce

def executeCommandNoCheck( params, retryOnExcept ):

	params = urllib.urlencode(params)
	 
	#
	# Hash the params string to produce the Sign header value
	#
	H = hmac.new(BTC_api_secret, digestmod=hashlib.sha512)
	H.update(params)
	sign = H.hexdigest()
	 
	headers = {"Content-type": "application/x-www-form-urlencoded",
		           "Key":BTC_api_key,
		           "Sign":sign}
	try:
		conn = httplib.HTTPSConnection("btc-e.com")
		conn.request("POST", "/tapi", params, headers)
		response = conn.getresponse()
	except Exception:
		sys.stdout.write("E")
		sys.stdout.flush()
		if not retryOnExcept:
			return None
		else:
			time.sleep(5)

	if response.status != 200:
		return None
	jres = json.load(response)
 	conn.close()
	return jres

def executeCommand( params, retryOnExcept ):
	jres = executeCommandNoCheck( params, retryOnExcept )
	if jres == None:
		return None
	if jres[u'success'] != 1:
		return None
	return jres




def TradeOrder( orderType, rate, amount ):
	params = {"method":"Trade",
		  "pair": "btc_usd",
		  "type": orderType,
		  "rate": rate,
		  "amount": amount,
		  "nonce": get_nonce()}
	jres = executeCommand( params, False )
	if jres == None:
		return None
	return jres[u'return']['order_id']

def getInfo():
	params = {"method":"getInfo",
		  "nonce": get_nonce()}
	jres = executeCommand( params, True )
	if jres == None:
		return None
	return jres['return']['funds']['btc'], jres['return']['funds']['usd']

def getFunds():
	btc_qty, usd_qty = getInfo()
	last_buy, last_sell = getBuySellPrices()
	return btc_qty*last_sell + usd_qty



def getData( endTime ):
	conn = httplib.HTTPConnection("api.bitcoincharts.com")
	if endTime is None:
		conn.request("POST", "/v1/trades.csv?symbol=btceUSD")
	else:
		conn.request("POST", "/v1/trades.csv?symbol=btceUSD&start=" + endTime)
	response = conn.getresponse()
	if response.status != 200:
		return ""
	return response.read()




def preprocessRetData(data):
	retrievedData = {}
	if data == "":
		return []
	for l in data.split('\n'):
		fields = l.split(',')
		if len(fields) < 3:
			continue
		optime = int(fields[0])
		price = float(fields[1])
		btc = float(fields[2])
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

	return sorted(retData, key = lambda x : x[0])


#######################################################################################################

#print getData(None)


#print getInfo()
#print getBuySellPrices()

def execute( prog ):
	b_bal = .02
	d_bal = 0
	
	# Tomo -100 a -10 como % ven
	# Tomo 10 a 100 como % comp
	# Tomo -10 a 10 como no action
	# fuera de rango redondeo a max o min
	
	runnum = 0
	last_b_d = 0
	last_s_d = 0
	last_b_b = 0
	last_s_b = 0
	last_b_cot = 0
	last_s_cot = 0
	last_res = 0
	last_cot = 0

	last_time = 0

	while True:
		data = getData(str(int(time.time())-60*60*24))
		rundata = preprocessRetData(data)
		last_item = len(rundata) - 1
		if rundata[last_item][0] <= last_time:
			sys.stdout.write("*")
			sys.stdout.flush()
			time.sleep(10)
			continue
		last_time = rundata[last_item][0]
		d = rundata[last_item][1]
		cont = gen_context( rundata, runnum, b_bal, d_bal, last_b_d, last_s_d, last_b_b, last_s_b, last_b_cot, last_s_cot, last_res, last_cot, d )
		 
		res = prog.execute( cont )
		if res < -10:
			if res < -100: res = -100
			delta = b_bal * ( -res / 100 )
			if delta >= 0.01:
				if delta > 0.1:
					delta = 0.1
				buy, sell = getBuySellPrices()
				d_adj = sell * 0.995 
				d_bal += delta * d_adj * 0.998
				b_bal -= delta
				last_s_cot = d_adj
				last_s_d = delta * d_adj
				last_s_b = delta
				print runnum, "[", (b_bal * d + d_bal) ,"] [", res ,"] V: ", d_adj, "cot: ", d ,"D: ", d_bal, "B: ", b_bal
			else:
				print "V muy chico. Pass", delta
				d_adj = d
		elif res > 10:
			if res > 100: res = 100
			delta = d_bal * ( res / 100 )
			buy, sell = getBuySellPrices()
			d_adj = buy * 1.005
			delta_btc = delta/d_adj
			if delta_btc >= 0.01:
				if delta_btc > 0.1:
					delta_btc = 0.1
				b_bal += delta_btc * 0.998
				d_bal -= delta_btc * d_adj
				last_b_cot = d_adj
				last_b_d = delta
				last_b_b = delta_btc
				print runnum, "[", (b_bal * d + d_bal) ,"] [", res ,"] C: ", d_adj, "cot: ", d ,"D: ", d_bal, "B: ", b_bal
			else:
				print "C muy chico. Pass", delta_btc
		else:
			print "Pass"
			d_adj = d

		last_res = res
		last_cot = d_adj
		
		sys.stdout.flush()
		time.sleep(10)

sys.setrecursionlimit(5000)

if len(sys.argv) == 2:
	fname_prog = sys.argv[1]
	with open(fname_prog, 'rb') as f:
		prog = pickle.load(f)

	execute( prog )

print preprocessRetData(getData(str(int(time.time())-1000)))
