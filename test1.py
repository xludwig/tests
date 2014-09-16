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
		print "Creating FULL", i
		indiv = func_root()
		indiv.addchild(gen_indiv(max_depth, func_set, term_set, "FULL", thresh))
		populat.append( indiv )
	for i in range(int(pop_size*growpct)):
		print "Creating GROW", i
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
	
def Operation_Copy( population, func_list, term_list, max_d ):
	result = []
	result.append( weighted_choice( population, lambda indiv: indiv.fitness ) )
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
def gen_context( rundata, runnum, b_bal, d_bal, last_b_d, last_s_d, last_b_b, last_s_b, last_b_cot, last_s_cot, last_res, last_cot ):
	context = {}
	context["last_data"] = rundata[:runnum]
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
	return context
	
def evalFitness( prog, rundata, print_data ):
	b_bal = .1
	d_bal = 1
	
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
	for d in rundata:
		cont = gen_context( rundata, runnum, b_bal, d_bal, last_b_d, last_s_d, last_b_b, last_s_b, last_b_cot, last_s_cot, last_res, last_cot ) 
		res = prog.execute( cont )
		if res < -10:
			if res < -100: res = -100
			if b_bal >= 0.01:
				delta = b_bal * ( -res / 100 )
				d_bal += delta * d * 0.998
				b_bal -= delta
				last_s_cot = d
				last_s_d = delta * d
				last_s_b = delta
				if print_data: print runnum, "V: ", res, "cot: ", d ,"D: ", d_bal, "B: ", b_bal
		elif res > 10:
			if res > 100: res = 100
			if d_bal >= 0.01 * d:
				delta = d_bal * ( res / 100 )
				b_bal += (delta / d) * 0.998
				d_bal -= delta
				last_b_cot = d
				last_b_d = delta
				last_b_b = (delta / d)
				if print_data: print runnum, "C: ", res, "cot: ", d ,"D: ", d_bal, "B: ", b_bal
		last_res = res
		last_cot = d
		runnum += 1

	return b_bal * rundata[len(rundata)-1] + d_bal

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
		if len(last_data) < 1:
			return 0
		len_data = len(last_data) - 1
		if x < 0: x = 0
		if y < 0: y = 0
		if x > len_data: x = len_data
		if y > len_data: y = len_data
		return last_data[int(y)] - last_data[int(x)]

#### 1 par

class func_prev_cot(generic_func):
	def __init__(self):
		generic_func.__init__(self)
		self.num_childs = 1

	def execute( self, context ):
		x = self.child[0].execute( context )
		last_data = context["last_data"]
		if len(last_data) < 1:
			return 0
		len_data = len(last_data) - 1
		if x < 0: x = 0
		if x > len_data: x = len_data
		return last_data[int(x)]

class func_prev_delta(generic_func):
	def __init__(self):
		generic_func.__init__(self)
		self.num_childs = 1

	def execute( self, context ):
		x = self.child[0].execute( context )
		last_data = context["last_data"]
		if len(last_data) < 1:
			return 0
		len_data = len(last_data) - 1
		if x < 0: x = 0
		if x > len_data - 1: x = len_data - 1
		a = last_data[len_data]
		b = last_data[int(x)]
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

max_total_fitness = 0
max_total_fitness_indiv = None
rand_state = None
rundata = None

import sys

def dumpstate():
	global max_total_fitness
	global max_total_fitness_indiv
	global rand_state
	global rundata

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

	print "Dump Finished"
	sys.exit()

import signal

def signal_handler(signal, frame):
	dumpstate()

def generate():
	global max_total_fitness
	global max_total_fitness_indiv
	global rand_state
	global rundata

	rand_state = random.getstate()
	signal.signal(signal.SIGINT, signal_handler)
	
	pop_size = 70
	max_depth = 8
	max_generations = 100
	##rundata = [100, 100, 100.2, 100.5, 101, 1000, 1010, 1020, 900, 500, 200, 90, 80, 50]
	## daily 2014 hasta el 09-09
	rundata = [770.4357, 808.0485, 830.0240, 858.9833, 940.0972, 951.3865, 810.5833, 859.9485, 860.8950, 884.6667, 930.9050, 873.2635, 857.9564, 851.8280, 874.7130, 847.3735, 828.2220, 843.7583, 878.6807, 871.0483, 874.2885, 863.9500, 854.3475, 825.1221, 861.8516, 880.1523, 814.5302, 833.9395, 837.5148, 845.8467, 848.2875, 853.0164, 854.3750, 846.9048, 842.0123, 820.8670, 783.6211, 703.5670, 676.9094, 681.9371, 679.7338, 669.4418, 648.3835, 598.4075, 656.6068, 645.4300, 610.6525, 621.4940, 621.2235, 617.7100, 552.2138, 569.0425, 604.7473, 604.5823, 545.3225, 534.7108, 577.0858, 576.6980, 543.9265, 563.7358, 560.3045, 661.1225, 663.5980, 661.7858, 658.7245, 625.8278, 615.2400, 633.1825, 625.8285, 628.9543, 631.3913, 638.1650, 626.7067, 633.6652, 630.7167, 621.2225, 613.6315, 608.8157, 586.5898, 570.7705, 564.4215, 561.3534, 586.2718, 582.2802, 579.0722, 478.1595, 502.4399, 493.1803, 461.8695, 458.4972, 478.7163, 437.5150, 447.0822, 448.8792, 464.8259, 460.7028, 446.2195, 450.4638, 440.1983, 360.8407, 420.0563, 420.6600, 414.9495, 457.6338, 520.1233, 529.1625, 494.4000, 478.2312, 501.5515, 497.3177, 493.0921, 484.4290, 486.9317, 500.2568, 459.6104, 456.1395, 429.6537, 437.0587, 444.2533, 445.8655, 456.2673, 446.6438, 436.9381, 434.0643, 429.7242, 426.9920, 436.9605, 435.3430, 448.2350, 452.7108, 436.5420, 438.4278, 437.4130, 441.7498, 444.3162, 445.0133, 446.3583, 444.8090, 444.3128, 485.8305, 489.1625, 526.0577, 519.0392, 525.6332, 570.0950, 581.8267, 569.6332, 574.4547, 565.5058, 616.4700, 623.2567, 629.0242, 658.7860, 665.7300, 636.7837, 656.0598, 645.5647, 652.7083, 653.6402, 645.3410, 649.8068, 627.9098, 581.8033, 597.4267, 571.6902, 591.9718, 588.0600, 607.3427, 604.8752, 592.2648, 588.5215, 591.0298, 598.8765, 587.4598, 575.0667, 562.1263, 579.3842, 600.8645, 591.9940, 598.6032, 639.3623, 635.5905, 647.3400, 640.6879, 626.9575, 628.3313, 631.7065, 617.9918, 620.2193, 620.5496, 615.1129, 631.1804, 634.4775, 627.5759, 618.3798, 619.3558, 615.2039, 622.6234, 628.2156, 625.8011, 621.3725, 620.0103, 618.8076, 617.9274, 600.0065, 599.9280, 593.8526, 590.9454, 584.6931, 582.2034, 564.3700, 581.3501, 595.0845, 587.2878, 585.5078, 586.7639, 583.1125, 583.0355, 587.3971, 590.5324, 588.0950, 589.4500, 573.3066, 568.2099, 544.5681, 508.5536, 496.6164, 519.8314, 492.9513, 460.6719, 486.7360, 511.9259, 516.1605, 513.9419, 497.2185, 508.5735, 501.6296, 513.4704, 510.4300, 507.0154, 508.4224, 501.2031, 478.0734, 474.1346, 475.3181, 474.5370, 489.0865, 480.5010, 482.2371, 479.4833, 472.1479, 471.5576]
	
	func_set = [func_ifless, func_iflesseq, func_ifmore, func_ifmoreeq, func_ifeq, func_if, func_plus, func_minus, func_por, func_div, func_less, func_lesseq, func_more, func_moreeq, func_eq, func_and, func_or, func_prev_delta_x_y, func_prev_cot, func_prev_delta]
	term_set = [term_zero, term_one, term_two, term_three, term_random_const_100, term_random_const_1000, term_last_b_d, term_last_s_d, term_last_b_b, term_last_s_b, term_last_b_cot, term_last_s_cot, term_last_res, term_last_cot, term_bal_b, term_bal_d, term_runnum]

	copy_probability = 0.05
	crossover_probability = 0.60
	mutation_probability = 0.05
	mutationgen_probability = 0.06
	newindivgrow_probability = 0.12
	newindivfull_probability = 0.12
	operations = [( Operation_Copy, copy_probability), ( Operation_CrossOver, crossover_probability), ( Operation_Mutation, mutation_probability ), ( Operation_MutationGen, mutationgen_probability ), ( Operation_NewIndivFull, newindivfull_probability ), ( Operation_NewIndivGrow, newindivgrow_probability ) ]

	growpct = 0.5
	fullpct = 0.5

	print "Creating Initial Population"
	population = init_population( pop_size, max_depth, func_set, term_set, growpct, fullpct )
	generation_num = 0
	max_total_fitness = 0
	while generation_num < max_generations:
		maxnodes = 0
		totalnodes = 0
		for p in population:
			nodes = count_nodes( p )
			totalnodes += nodes
			maxnodes = max( [maxnodes, nodes] )
		print "Population Stats: Size: ", len(population) ,"max:", maxnodes, "total:", totalnodes, "avg:", int(totalnodes/pop_size)
	
		print "Evaluating Fitness Gen: ", generation_num
		totalfitness = 0
		maxfitness = 0
		i = 0
		for prog in population:
			prog.fitness = evalFitness( prog, rundata, False ) 
			totalfitness += prog.fitness
			maxfitness = max( [maxfitness, prog.fitness] )
			if maxfitness == prog.fitness:
				maxfitIndiv = prog
			i += 1
			if i % 5 == 0:
				time.sleep(1)
			if i % 10 == 0:
				sys.stdout.write("*")
    				sys.stdout.flush()
    				
		print "Done Gen", generation_num
		
		max_total_fitness = max( [max_total_fitness, maxfitness] )
		if max_total_fitness == maxfitness:
			max_total_fitness_indiv = maxfitIndiv
		print "Total Fitness: ", int(totalfitness), "Max: ", int(maxfitness), "Avg: ", int(totalfitness/pop_size) ,"Gen: ", generation_num
		print "Getting top 10"
		
		sortedpop = sorted(population, key = lambda x : x.fitness, reverse = True)
		top10_pop = []
		last_fit = 0
		topn = 0
		for p in sortedpop:
			if last_fit != p.fitness:
				top10_pop.append(p)
				topn += 1
				lastfit = p.fitness
				if topn == 10: break
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

if len(sys.argv) == 1:
	generate()
else:
	# Playback file
	fname_indiv = sys.argv[1]
	fname_rundata = sys.argv[2]
	with open(fname_indiv, 'rb') as f:
    		indiv = pickle.load(f)
	with open(fname_rundata, 'rb') as f:
    		rundat = pickle.load(f)
    	
    	print evalFitness( indiv, rundat, True )