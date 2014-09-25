##### Generic Funcs
import random
import time
import pickle

def gen_indiv(max_d, func_set, term_set ,method, thresh):
	if max_d == 0 or (method == "GROW" and random.random() < thresh):
		elem = random.choice( term_set )()
	else:
		elem = random.choice( func_set )()
		
	for i in range(elem.num_childs):
		elem.addchild( gen_indiv(max_d - 1, func_set, term_set ,method, thresh) )

	return elem

def init_population( pop_size, max_depth, func_set, term_set, growpct, fullpct):
	thresh = len(term_set) / ( len(term_set) + len(func_set) )

	populat = []
	for i in range(int(pop_size*fullpct)):
		sys.stdout.write("F")
    		sys.stdout.flush()
		indiv = func_root()
		indiv.addchild(gen_indiv(max_depth, func_set, term_set, "FULL", thresh))
		populat.append( indiv )
	for i in range(int(pop_size*growpct)):
		sys.stdout.write("G")
    		sys.stdout.flush()
		indiv = func_root()
		indiv.addchild(gen_indiv(max_depth, func_set, term_set, "GROW", thresh))
		populat.append( indiv )
	return populat

def weighted_choice(choices, getweigth):
   total = sum( getweigth(c) for c in choices)
   r = random.uniform(0, total)
   upto = 0
   for c in choices:
      upto += getweigth(c)
      if upto > r:
         return c

def select_operation( operations ):
	oper = weighted_choice( operations, lambda op: op[1] )
	return oper[0]
	
import copy

def Operation_Copy( population, func_list, term_list, max_d ):
	result = []
	result.append( copy.deepcopy( weighted_choice( population, lambda indiv: indiv.fitness ) ) )
	return result

def count_nodes( indiv ):
	if indiv.num_childs == 0:
		return 1
	cant = 1
	for c in indiv.child:
		cant += count_nodes(c)
	return cant


def get_node_rec( indiv, selnode ):
	#print "GNR: ", indiv.nam, " - ", selnode
	accum_qty = 1
	node_num = 0
	for c in indiv.child:
		if selnode - accum_qty == 0:
			#print "R1", indiv.nam, 0, 0
			return indiv, node_num, 0
		#print "0", c.nam, selnode - accum_qty
		parent, seln, qty = get_node_rec( c, selnode - accum_qty )
		#print "1", parent, seln, qty
		if qty == 0:
			#print "R2", parent.nam, seln, 0
			return parent, seln, 0
		accum_qty += qty
		node_num += 1
		#print "Acc_qty", indiv.nam, c.nam, accum_qty
	
	#print "R4", None, None, accum_qty
	return None, None, accum_qty


## Returns parentNode, parNum
## Passed test_gn2
def get_node_num( indiv, selnode ):
	parent, seln, qty = get_node_rec(indiv, selnode)
	return parent, seln

class cls_test_gn:
	def __init__(self, nam, numnodes):
		self.num_childs = numnodes
		self.nam = nam
		self.childs = []
	def __repr__(self):
		if self.num_child > 0:
			return self.nam + "-" + str(self.num_childs) + ": " + str(self.childs) 
		else:
			return self.nam + "-" + str(self.num_childs)
## A-> B -> C -> D
##       -> E -> F
##            -> G
def test_gn1():
	A = cls_test_gn("A", 1)
	B = cls_test_gn("B", 2)
	C = cls_test_gn("C", 1)
	D = cls_test_gn("D", 0)
	E = cls_test_gn("E", 2)
	F = cls_test_gn("F", 0)
	G = cls_test_gn("G", 0)
	
	A.childs.append(B)
	B.childs.append(C)
	B.childs.append(E)
	C.childs.append(D)
	E.childs.append(F)
	E.childs.append(G)
	
	print A
	print count_nodes(A)
	print get_node_num( A, 1 )
	print get_node_num( A, 2 )
	print get_node_num( A, 3 )
	print get_node_num( A, 4 )
	print get_node_num( A, 5 )
	print get_node_num( A, 6 )
	
	exit()
	

## A-> B -> C -> D
##       -> E -> F
##            -> G
##       -> H -> I
##            -> J
##            -> K -> L
##       -> M -> N
def test_gn2():
	A = cls_test_gn("A", 1)
	B = cls_test_gn("B", 4)
	C = cls_test_gn("C", 1)
	D = cls_test_gn("D", 0)
	E = cls_test_gn("E", 2)
	F = cls_test_gn("F", 0)
	G = cls_test_gn("G", 0)
	H = cls_test_gn("H", 3)
	I = cls_test_gn("I", 0)
	J = cls_test_gn("J", 0)
	K = cls_test_gn("K", 1)
	L = cls_test_gn("L", 0)
	M = cls_test_gn("M", 1)
	N = cls_test_gn("N", 0)
	
	A.childs.append(B)
	B.childs.append(C)
	B.childs.append(E)
	B.childs.append(H)
	B.childs.append(M)
	C.childs.append(D)
	E.childs.append(F)
	E.childs.append(G)
	H.childs.append(I)
	H.childs.append(J)
	H.childs.append(K)
	K.childs.append(L)
	M.childs.append(N)
	
	print A
	print count_nodes(A)
	for i in range( 1, 14 ):
		print i, get_node_num( A, i )
	exit()

#test_gn2() 


def sel_random_node( indiv ):
	cant_nodes = count_nodes( indiv )
	selnode = random.randint(1,cant_nodes-1)
	return get_node_num(indiv, selnode)

def Operation_CrossOver( population, func_list, term_list, max_d ):
	result = []
	indiv1 = weighted_choice( population, lambda indiv: indiv.fitness )
	indiv2 = weighted_choice( population, lambda indiv: indiv.fitness )
	parentNode1, parNum1 = sel_random_node( indiv1 )
	parentNode2, parNum2 = sel_random_node( indiv2 )
	node1 = parentNode1.getParNum(parNum1)
	node2 = parentNode2.getParNum(parNum2)
	parentNode1.setParNum(parNum1, node2)
	parentNode2.setParNum(parNum2, node1)
	result.append( indiv1 )
	result.append( indiv2 )
	return result

def Operation_Mutation( population, func_list, term_list, max_d ):
	result = []
	indiv = weighted_choice( population, lambda indiv: indiv.fitness )
	parentNode, parNum = sel_random_node( indiv )
	node = parentNode.getParNum(parNum)
	num_childs = node.num_childs
	if num_childs == 0:
		elem = random.choice( term_list )()
	elif num_childs == 3: #### esto es re-custom cuando son 3 solo esta el if por lo que no se busca ni se muta
		pass
	else:
		elem = random.choice( func_list )()
		while elem.num_childs != num_childs:
			elem = random.choice( func_list )()
		for i in range(num_childs):
			elem.addchild( node.getParNum(i) )
		parentNode.setParNum(parNum, elem)
	result.append( indiv )
	return result

def Operation_MutationGen( population, func_set, term_set, max_d ):
	result = []
	indiv = weighted_choice( population, lambda indiv: indiv.fitness )
	parentNode, parNum = sel_random_node( indiv )
	
	thresh = len(term_set) / ( len(term_set) + len(func_set) )
	elem = gen_indiv(int(max_d*0.7), func_set, term_set ,"FULL", thresh)
	parentNode.setParNum(parNum, elem)

	result.append( indiv )
	return result

def Operation_NewIndivFull( population, func_set, term_set, max_d ):
	result = []
	thresh = len(term_set) / ( len(term_set) + len(func_set) )
	indiv = gen_indiv(max_d, func_set, term_set ,"FULL", thresh)
	return result

def Operation_NewIndivGrow( population, func_set, term_set, max_d ):
	result = []
	thresh = len(term_set) / ( len(term_set) + len(func_set) )
	indiv = gen_indiv(max_d, func_set, term_set ,"GROW", thresh)
	return result



#### Problem Specific
def gen_context( rundata, runnum, b_bal, d_bal, last_b_d, last_s_d, last_b_b, last_s_b, last_b_cot, last_s_cot, last_res, last_cot, curr_cot ):
	context = {}
	context["all_data"] = rundata
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
	init_b = 0.02
	init_d = 0.0
	
	b_bal = 0.02
	d_bal = 0.0
	
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
	
	operations = 0
	
	for dcomplete in rundata:
		#if runnum % 1000 == 0:
		#	sys.stdout.write("-")
    		#	sys.stdout.flush()
	
		d = dcomplete[1]
		cont = gen_context( rundata, runnum, b_bal, d_bal, last_b_d, last_s_d, last_b_b, last_s_b, last_b_cot, last_s_cot, last_res, last_cot, d ) 
		res = prog.execute( cont )
		if res < -10:
			if res < -100: res = -100
			delta = b_bal * ( -res / 100 )
			if delta >= 0.01:
				if delta > 0.1:
					delta = 0.1
				d_adj = d * 0.999
				d_bal += delta * d_adj * 0.998
				b_bal -= delta
				last_s_cot = d_adj
				last_s_d = delta * d_adj
				last_s_b = delta
				operations += 1
				if print_data: print runnum, "[", (b_bal * d + d_bal) ,"] V: ", res, "cot: ", d ,"D: ", d_bal, "B: ", b_bal
		elif res > 10:
			if res > 100: res = 100
			delta = d_bal * ( res / 100 )
			d_adj = d * 1.001
			delta_btc = delta/d_adj
			if delta_btc >= 0.01:
				if delta_btc > 0.1:
					delta_btc = 0.1
				b_bal += delta_btc * 0.998
				d_bal -= delta_btc * d_adj
				last_b_cot = d_adj
				last_b_d = delta
				last_b_b = delta_btc
				operations += 1
				if print_data: print runnum, "[", (b_bal * d + d_bal) ,"] C: ", res, "cot: ", d ,"D: ", d_bal, "B: ", b_bal
		last_res = res
		last_cot = d
		runnum += 1



	init_val = init_b * rundata[0][1] + init_d
	final_val = b_bal * rundata[len(rundata)-1][1] + d_bal
	res = ( final_val - init_val ) / init_val
	#print init_val, final_val, res 

	if res < -0.01:
		res = 0.0

	if res < 0:
		res = 0.0000000000001

	return res * 1000, operations
	#return b_bal * rundata[len(rundata)-1][1] + d_bal

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

#### 1 par

class func_prev_cot(generic_func):
	def __init__(self):
		generic_func.__init__(self)
		self.num_childs = 1

	def execute( self, context ):
		x = self.child[0].execute( context )
		all_data = context["all_data"]
		runnum = context["runnum"]
		len_data = runnum - 1
		if len_data < 0:
			return 0
		if x < 0: x = 0
		if x > len_data: x = len_data
		return all_data[int(x)][1]

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
		all_data = context["all_data"]
		runnum = context["runnum"]
		len_data = runnum - 1
		if len_data < 0:
			return 0
		if len_data < 1:
			return all_data[len_data][0]
		return all_data[len_data][0] - all_data[len_data - 1][0]

class term_curr_vol(generic_term):
	def __init__(self):
		generic_term.__init__(self)
	def execute( self, context ):
		all_data = context["all_data"]
		runnum = context["runnum"]
		len_data = runnum - 1
		if len(all_data) < 0:
			return 0
		return all_data[len_data][2]

class term_curr_vol_diff(generic_term):
	def __init__(self):
		generic_term.__init__(self)
	def execute( self, context ):
		all_data = context["all_data"]
		runnum = context["runnum"]
		len_data = runnum - 1
		if len_data < 0:
			return 0
		if len_data < 1:
			return all_data[len_data][2]
		return all_data[len_data][2] - all_data[len_data - 1][2]

class term_curr_cot_diff(generic_term):
	def __init__(self):
		generic_term.__init__(self)
	def execute( self, context ):
		all_data = context["all_data"]
		runnum = context["runnum"]
		len_data = runnum - 1
		if len_data < 0:
			return 0
		if len_data < 1:
			return all_data[len_data][1]
		return all_data[len_data][1] - all_data[len_data - 1][1]

max_total_fitness = 0
max_total_fitness_indiv = None
rand_state = None
rundata = None
population = None

import sys

def dumpstate():
	global max_total_fitness
	global max_total_fitness_indiv
	global rand_state
	global rundata
	global population
	
	if max_total_fitness == 0:
		print "Not Dumping State"
		sys.exit()
		return

	print "Dumping State"

	timestr = time.strftime("%Y%m%d-%H%M%S")

	with open(timestr + "_rand.dmp", 'wb') as f:
	    pickle.dump(rand_state, f)

	with open(timestr + "_rundata.dmp", 'wb') as f:
	    pickle.dump(rundata, f)

	with open(timestr + "_max" + str( int(max_total_fitness) ) + ".dmp", 'wb') as f:
	    pickle.dump(max_total_fitness_indiv, f)

	with open(timestr + "_population.dmp", 'wb') as f:
	    pickle.dump(population, f)

	print "Dump Finished"

import signal

def signal_handler(signal, frame):
	dumpstate()
	sys.exit()

def generate( initial_pop, rundat ):
	global max_total_fitness
	global max_total_fitness_indiv
	global rand_state
	global rundata
	global population
	
	rand_state = random.getstate()
	signal.signal(signal.SIGINT, signal_handler)
	
	pop_size = 10000
	max_depth = 3
	max_generations = 1000
	rundata = rundat
	
	func_set = [func_if, func_plus, func_minus, func_por, func_div, func_less, func_more, func_eq, func_and, func_or, func_prev_cot, func_prev_cot, func_prev_cot, func_prev_cot, func_prev_cot]
	term_set = [term_zero, term_one, term_two, term_three, term_random_const_100, term_last_b_d, term_last_s_d, term_last_b_b, term_last_s_b, term_last_b_cot, term_last_s_cot, term_last_res, term_last_cot, term_curr_cot, term_curr_val, term_timediff, term_curr_vol, term_curr_vol_diff, term_curr_cot_diff, term_bal_b, term_bal_d, term_runnum, term_last_b_d, term_last_s_d, term_last_b_b, term_last_s_b, term_last_b_cot, term_last_s_cot, term_last_res, term_last_cot, term_curr_cot, term_curr_val, term_timediff, term_curr_vol, term_curr_vol_diff, term_curr_cot_diff, term_bal_b, term_bal_d, term_runnum, term_last_cot, term_curr_cot, term_curr_val, term_timediff, term_curr_vol, term_curr_vol_diff, term_curr_cot_diff, term_bal_b, term_bal_d, term_last_cot, term_curr_cot, term_curr_val, term_timediff, term_curr_vol, term_curr_vol_diff, term_curr_cot_diff, term_bal_b, term_bal_d, term_last_cot, term_curr_cot, term_curr_val, term_timediff, term_curr_vol, term_curr_vol_diff, term_curr_cot_diff, term_bal_b, term_bal_d]

	copy_probability = 0.0
	crossover_probability = 0.75
	mutation_probability = 0.05
	mutationgen_probability = 0.1
	newindivgrow_probability = 0.05
	newindivfull_probability = 0.05
	operations = [( Operation_Copy, copy_probability), ( Operation_CrossOver, crossover_probability), ( Operation_Mutation, mutation_probability ), ( Operation_MutationGen, mutationgen_probability ), ( Operation_NewIndivFull, newindivfull_probability ), ( Operation_NewIndivGrow, newindivgrow_probability ) ]

	growpct = 0.5
	fullpct = 0.5
	
	topNcpy = 10

	print "Creating Initial Population"
	
	if initial_pop is None:
		population = init_population( pop_size, max_depth, func_set, term_set, growpct, fullpct )
	else:
		population = initial_pop
		
	print "RunData init: ", rundat[0][1], " final: ", rundat[len(rundat) - 1][1]
	generation_num = 0
	max_total_fitness = 0
	dump_fitness = 0
	while generation_num < max_generations:
		maxnodes = 0
		totalnodes = 0
		for p in population:
			nodes = count_nodes( p )
			totalnodes += nodes
			maxnodes = max( [maxnodes, nodes] )
		print "Population Stats Size: ", len(population) ,"max:", maxnodes, "total:", totalnodes, "avg:", int(totalnodes/pop_size)
	
		print "Evaluating Fitness Gen: ", generation_num
		totalfitness = 0
		maxfitness = 0
		i = 0
		starttime = time.time()
		for prog in population:
			realfitness, altfitness = evalFitness( prog, rundata, False )
			if generation_num < 10:
				prog.fitness = altfitness
			else:
				prog.fitness = realfitness
			totalfitness += prog.fitness
			maxfitness = max( [maxfitness, prog.fitness] )
			if maxfitness == prog.fitness:
				maxfitIndiv = copy.deepcopy( prog )
			i += 1
			if i % 5 == 0:
				#time.sleep(1)
				pass
			if i % 1 == 0:
				sys.stdout.write("*")
				sys.stdout.write(str(int(prog.fitness)))
    				sys.stdout.flush()

		elapsed = (time.time() - starttime)
    				
		print "Done [", elapsed,"]secs Gen", generation_num
		
		max_total_fitness = max( [max_total_fitness, maxfitness] )
		if max_total_fitness == maxfitness:
			max_total_fitness_indiv = copy.deepcopy( maxfitIndiv )
			if max_total_fitness > 150 and max_total_fitness > dump_fitness:
				dump_fitness = max_total_fitness
				dumpstate()
				
		if generation_num % 50 == 0 and generation_num != 0:
			dumpstate()
		
		print "Total Fitness: ", totalfitness, "Max: ", maxfitness, "Avg: ", totalfitness/pop_size ,"Gen: ", generation_num
		print "Getting top", topNcpy
		
		sortedpop = sorted(population, key = lambda x : x.fitness, reverse = True)
		top10_pop = []
		last_fit = 0
		topn = 0
		for p in sortedpop:
			if last_fit != p.fitness:
				top10_pop.append( copy.deepcopy( p ) )
				topn += 1
				lastfit = p.fitness
				if topn == topNcpy: break
		print "got top ", topn
		
		i = 0
		next_generation = []
		print "Creating Next Generation: ", generation_num + 1
		while i < pop_size:
			oper = select_operation(operations)
			gen_new_indivs = oper( population, func_set, term_set, max_depth )
			next_generation.extend( gen_new_indivs )
			i += len(gen_new_indivs)
		
		next_generation.extend( top10_pop )
		
		population = next_generation
		next_generation = []
		generation_num += 1
		pop_size = len( population )

	dumpstate()


sys.setrecursionlimit(5000)

if len(sys.argv) == 1:
	sys.exit()
elif len(sys.argv) == 2:
	fname_rundata = sys.argv[1]
	with open(fname_rundata, 'rb') as f:
    		rundat = pickle.load(f)
    	generate( None, rundat )
elif len(sys.argv) == 3: # Indiv, rundata
	# Playback file
	fname_indiv = sys.argv[1]
	fname_rundata = sys.argv[2]
	with open(fname_indiv, 'rb') as f:
    		indiv = pickle.load(f)
	with open(fname_rundata, 'rb') as f:
    		rundat = pickle.load(f)
    	
    	print evalFitness( indiv, rundat, True )
    	
elif len(sys.argv) == 4: # Population, Rundata, cantPrune
	#prune
	print "Loading data"
	fname_population = sys.argv[1]
	fname_rundata = sys.argv[2]
	with open(fname_population, 'rb') as f:
    		population = pickle.load(f)
	with open(fname_rundata, 'rb') as f:
    		rundat = pickle.load(f)
    	
    	i = 0
	for prog in population:
		if not hasattr(prog, 'fitness'):
			prog.fitness = evalFitness( prog, rundat, False )
		i += 1
		if i % 10 == 0:
			sys.stdout.write("*")
			sys.stdout.flush()

	total = int(sys.argv[3])
	print "Getting top", total
	
	sortedpop = sorted(population, key = lambda x : x.fitness, reverse = True)
	population = None
	topn = 0
	last_fit = 0
	topN_pop = []
	for p in sortedpop:
		if last_fit != p.fitness:
			topN_pop.append( p )
			topn += 1
			lastfit = p.fitness
			if topn == total: break
	print "Got top ", topn

	sortedpop = None
	
	generate( topN_pop )