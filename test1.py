##### Generic Funcs

def gen_indiv(max_d, func_set, term_set ,method, thresh):
	if max_d = 0 or (method = "GROW" and random.random() < thresh:
		elem = random.choice( term_set )
	else:
		elem = random.choice( func_set )
		
	for i in range(elem.child_qty):
		elem.addchild( gen_indiv(max_d - 1, func_set, term_set ,method, thresh) )

	return elem

def init_population( pop_size, max_depth, func_set, term_set ):
	thresh = len(term_set) / ( len(term_set) + len(func_set) )

	pop = []
	for i in range(pop_size/2):
		pop.append( gen_indiv(max_depth, func_set, term_set, "FULL", thresh) )
	for i in range(pop_size/2):
		pop.append( gen_indiv(max_depth, func_set, term_set, "GROW", thresh) )
	return 

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
	
def Operation_Copy( population ):
	result = []
	result.append( weighted_choice( population, lambda indiv: indiv.fitness ) )
	return result
	
def sel_random_node( indiv ):
### TODO


def Operation_CrossOver( population ):
### TODO
	result = []
	result.append( weighted_choice( population, lambda indiv: indiv.fitness ) )
	return result

def Operation_Mutation( population ):
### TODO
	result = []
	result.append( weighted_choice( population, lambda indiv: indiv.fitness ) )
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
	
def evalFitness( prog, rundata ):
	b_bal = 1
	d_bal = .1
	
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
		gen_context( rundata, runnum, b_bal, d_bal, last_b_d, last_s_d, last_b_b, last_s_b, last_b_cot, last_s_cot, last_res, last_cot ) 
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
		elif res > 10:
			if res > 100: res = 100
			if d_val >= 0.01 * d:
				delta = d_bal * ( res / 100 )
				b_bal += (delta / d) * 0.998
				d_bal -= delta
				last_b_cot = d
				last_b_d = delta
				last_b_b = (delta / d)
		last_res = res
		last_cot = d
		runnum += 1

	return b_bal * rundata[len(rundata)-1] + d_bal

class generic_func:
	def __init__(self):
		self.num_childs = 2
		self.childs = []

	def addchild( self, child ):
		self.childs.append( child )

class generic_term:
	def __init__(self):
		self.num_childs = 0
	def addchild( self, child ):
		pass

#Funcs: ( 4: ( ifless, iflesseq, ifmore, ifmoreeq, ifeq), 3: ( if ), 2: ( + - * / > < >= <= == && || prev_delta_x_y), 1 : ( prev_cot, prev_delta ) )

##### 4 pars

class func_ifless(generic_func):
	def __init__(self):
		self.num_childs = 4
		generic_func.__init__(self)
	def execute( self, context ):
		if child[0].execute( context ) < child[1].execute( context ):
			return child[2].execute( context )
		else:
			return child[3].execute( context )

class func_iflesseq(generic_func):
	def __init__(self):
		self.num_childs = 4
		generic_func.__init__(self)
	def execute( self, context ):
		if child[0].execute( context ) <= child[1].execute( context ):
			return child[2].execute( context )
		else:
			return child[3].execute( context )


class func_ifmore(generic_func):
	def __init__(self):
		self.num_childs = 4
		generic_func.__init__(self)
	def execute( self, context ):
		if child[0].execute( context ) > child[1].execute( context ):
			return child[2].execute( context )
		else:
			return child[3].execute( context )

class func_ifmoreeq(generic_func):
	def __init__(self):
		self.num_childs = 4
		generic_func.__init__(self)
	def execute( self, context ):
		if child[0].execute( context ) >= child[1].execute( context ):
			return child[2].execute( context )
		else:
			return child[3].execute( context )

class func_ifeq(generic_func):
	def __init__(self):
		self.num_childs = 4
		generic_func.__init__(self)
	def execute( self, context ):
		if child[0].execute( context ) == child[1].execute( context ):
			return child[2].execute( context )
		else:
			return child[3].execute( context )

#### 3 pars

class func_if(generic_func):
	def __init__(self):
		self.num_childs = 3
		generic_func.__init__(self)
	def execute( self, context ):
		if child[0].execute( context ) != 0:
			return child[1].execute( context )
		else:
			return child[2].execute( context )

#### 2 pars

class func_plus(generic_func):
	def __init__(self):
		generic_func.__init__(self)
	def execute( self, context ):
		a = child[0].execute( context )
		b = child[1].execute( context )
		try:		
			return a + b
		except:
			return a


class func_minus(generic_func):
	def __init__(self):
		generic_func.__init__(self)
	def execute( self, context ):
		a = child[0].execute( context )
		b = child[1].execute( context )
		try:		
			return a - b
		except:
			return b

class func_por(generic_func):
	def __init__(self):
		generic_func.__init__(self)
	def execute( self, context ):
		a = child[0].execute( context )
		b = child[1].execute( context )
		try:		
			return a * b
		except:
			return a

class func_div(generic_func):
	def __init__(self):
		generic_func.__init__(self)
	def execute( self, context ):
		a = child[0].execute( context )
		b = child[1].execute( context )
		try:		
			return a / b
		except:
			return b

class func_less(generic_func):
	def __init__(self):
		generic_func.__init__(self)
	def execute( self, context ):
		if child[0].execute( context ) < child[1].execute( context ):
			return 1
		else:
			return 0
		
class func_lesseq(generic_func):
	def __init__(self):
		generic_func.__init__(self)
	def execute( self, context ):
		if child[0].execute( context ) <= child[1].execute( context ):
			return 1
		else:
			return 0

class func_more(generic_func):
	def __init__(self):
		generic_func.__init__(self)
	def execute( self, context ):
		if child[0].execute( context ) > child[1].execute( context ):
			return 1
		else:
			return 0

class func_moreeq(generic_func):
	def __init__(self):
		generic_func.__init__(self)
	def execute( self, context ):
		if child[0].execute( context ) >= child[1].execute( context ):
			return 1
		else:
			return 0

class func_eq(generic_func):
	def __init__(self):
		generic_func.__init__(self)
	def execute( self, context ):
		if child[0].execute( context ) == child[1].execute( context ):
			return 1
		else:
			return 0

class func_and(generic_func):
	def __init__(self):
		generic_func.__init__(self)
	def execute( self, context ):
		if ( child[0].execute( context ) != 0 ) and ( child[1].execute( context ) != 0 ):
			return 1
		else:
			return 0

class func_or(generic_func):
	def __init__(self):
		generic_func.__init__(self)
	def execute( self, context ):
		if ( child[0].execute( context ) != 0 ) or ( child[1].execute( context ) != 0 ):
			return 1
		else:
			return 0

class func_prev_delta_x_y(generic_func):
	def __init__(self):
		generic_func.__init__(self)
	def execute( self, context ):
		x = child[0].execute( context )
		y = child[1].execute( context )
		last_data = context["last_data"]
		len_data = len(last_data) - 1
		if x < 0: x = 0
		if y < 0: y = 0
		if x > len_data: x = len_data
		if y > len_data: y = len_data
		return last_data[y] - last_data[x]

#### 1 par

class func_prev_cot(generic_func):
	def __init__(self):
		self.num_childs = 1
		generic_func.__init__(self)
	def execute( self, context ):
		x = child[0].execute( context )
		last_data = context["last_data"]
		len_data = len(last_data) - 1
		if x < 0: x = 0
		if x > len_data: x = len_data
		return last_data[x]

class func_prev_delta(generic_func):
	def __init__(self):
		self.num_childs = 1
		generic_func.__init__(self)
	def execute( self, context ):
		x = child[0].execute( context )
		last_data = context["last_data"]
		len_data = len(last_data) - 1
		if x < 0: x = 0
		if x > len_data - 1: x = len_data - 1
		return last_data[len_data] - last_data[x]

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

def main():

	pop_size = 1000
	max_depth = 30
	max_generations = 1000
	rundata = []
	func_set = []
	term_set = []

	copy_probability = 0.1
	crossover_probability = 0.85
	mutation_probability = 0.05
	operations = [( Opeartion_Copy, copy_probability), ( Operation_CrossOver, crossover_probability), ( Operation_Mutation, mutation_probability ) ]


	population = init_population( pop_size )
	generation_num = 0
	while generation_num < max_generations:
		for prog in population:
			prog.fitness = evalFitness( prog, rundata ) 
		i = 0
		next_generation = []
		while i < pop_size:
			oper = select_operation(operations)
			gen_new_indiv = oper( population )
			next_generation.extend( gen_new_indiv )
			i += len(new_indivs)
		population = next_generation
		next_generation = []
		generation_num += 1


	print max(population, key=lambda item: item.fitness)

main()
