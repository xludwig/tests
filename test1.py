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

def Operation_CrossOver( population ):
	result = []
	result.append( weighted_choice( population, lambda indiv: indiv.fitness ) )
	return result

def Operation_Mutation( population ):
	result = []
	result.append( weighted_choice( population, lambda indiv: indiv.fitness ) )
	return result


#### Problem Specific


def evalFitness( prog, rundata ):
	context_gen_funcs_and_terms = []
	
	b_bal = 1
	d_bal = .1
	
	# Tomo -100 a -10 como % ven
	# Tomo 10 a 100 como % comp
	# Tomo -10 a 10 como no action
	# fuera de rango redondeo a max o min
	
	runnum = 0
	for d in rundata:
		for cont in context_gen_funcs_and_terms:
			context.update( cont.gen_context( rundata, runnum, b_bal, d_bal) ) 
		res = prog.execute( cont )
		
		if res < -10:
			if res < -100: res = -100
			if b_bal >= 0.01:
				delta = b_bal * ( -res / 100 )
				d_bal += delta * d * 0.998
				b_bal -= delta
		elif res > 10:
			if res > 100: res = 100
			if d_val >= 0.01 * d:
				delta = d_bal * ( res / 100 )
				b_bal += (delta / d) * 0.998
				d_bal -= delta
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

#Funcs: ( 3, ( if ), 2, ( + - * / ) 


class func_plus(generic_func):
	def __init__(self):
		generic_func.__init__(self)
	def execute( context ):
		return child[0].execute( context ) + child[1].execute( context )

class term_one(generic_term):
	def __init__(self):
		generic_term.__init__(self)
	def execute( context ):
		return 1

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
