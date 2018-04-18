import random


def first_unassigned(state):
	problem = state.problem
	solution = state.solution

	unassigned_vars = problem.unassigned_variables(solution)	
	return unassigned_vars[0]

def random_unassigned(state):
	problem = state.problem
	solution = state.solution

	unassigned_vars = problem.unassigned_variables(solution)	
	return random.choice(unassigned_vars)

def custom_variable_selector(state):
	problem = state.problem
	solution = state.solution
	domain = state.domain  #remaining values

	# INSERT CODE HERE
	# Write your variable selection code here 
	# Return an unassigned variable 

	unassigned_vars = problem.unassigned_variables(solution)
	min_var = unassigned_vars[0]

	#get number of constraints of each unassigned var
	num_constraints = get_num_constraints(state, unassigned_vars)
	print("num_constraints:",num_constraints)
	for var in unassigned_vars:
		#num of remaining values for var and min
		num_remaining_dom = len(domain[var])
		num_remaining_min = len(domain[min_var])

		if num_remaining_dom < num_remaining_min:
			min_var = var

		elif num_remaining_dom == num_remaining_min:
			# if domain and min have same number of remaining values
			if num_constraints[var] >= num_constraints[min_var]:
				#Select variable with max constraints
				min_var = var

	return min_var

def get_num_constraints(state, unassigned_vars):
	problem = state.problem
	const_counter = {}

	for var in unassigned_vars:
		count = 0

		for constraint in problem.constraints:
			for key in constraint.variables:
				if (key != var) and key in unassigned_vars:
					count += 1
				const_counter[key] = count

	return const_counter

def default_order(state,variable):
	problem = state.problem
	domain = state.domain[variable]

	values = domain
	return values # return as-is

def random_order(state,variable):
	problem = state.problem
	domain = state.domain[variable]

	values = domain[:] # make copy
	random.shuffle(values)
	return values

def custom_value_ordering(state,variable):
	problem = state.problem
	domain = state.domain[variable]

	# return default_order(state,variable)
	# INSERT CODE HERE
	# Write your value ordering code here 
	# Return sorted values, accdg. to some heuristic
	if(len(domain) != 0): # Disregard deadend
		print("*****"*5)
		print("variable: ",variable)
		# print("problem: ",problem)
		print("variable domain:: ",domain)
		curr_num_val = len(domain) 

		num=0
		dom_val_count=[]

		pos_val_dict = dict()
		
		for dom,vals in state.domain.items():
			num = num + len(vals)

		# print("STATE DOM: ",state.domain)
		# print("CUR_LEN_DOM: ",num)

		# Count the current state's domain values
		for dom_val in domain:
			new_num=0
			# Create new state for testing each possible value in the domain
			new_state = state.copy()
			new_state.assign(variable,dom_val)
			print("NEW_STATE: ",new_state)

			# Check if it is a valid solution
			forward_checking(new_state,variable)

			# Count the new state's domain values
			for dom,vals in new_state.domain.items():
				new_num = new_num + len(vals)
			# print("NEW_LEN_DOM: ",new_num)
			dom_val_count.append(new_num)
		# print("Counts: ",dom_val_count)

		# Get the difference of the new state's count and current state's count
		differences = [num-val for val in dom_val_count]
		# print("DIFFERENCES: ", differences)
		# print(type(differences[0]))
		# print(type(dom))

		# Create a dictionary to sort corresponding position and value 
		for i,dom in enumerate(domain):
			pos_val_dict[dom] = differences[i]

		print(pos_val_dict)
		# Sort dictionary based on the values
		print("sorted dictionary: ",sorted(pos_val_dict.items(), key=lambda x:x[1]))
		# Get the sorted keys which are the LCV 
		answer = sorted(pos_val_dict, key=pos_val_dict.get)
		print("FINAL ANSWER: ",answer)
		return answer
	else: # Handle deadends
		return default_order(state,variable)





	# print("domain: ",state.domain)
	# for dom,vals in state.domain.items():
	# 	print("-----"*5)
	# 	print("dom :",dom)
	# 	print("values :",vals)
	# 	new_state = state.copy()
	# 	new_state.assign(dom,vals)
	# 	for new_dom,new_vals in new_state.domain.items():
	# 		print("new_dom : ",new_dom)
	# 		print("new_vals : ",new_vals)



		# print("length of dom",dom,len(vals))
	# get domain of other variables
	# check the sum of count of their domain values
	# choose the combination that will produce higher sum

	
	# print("FWD: ",forward_checking(new_state,variable))
	# print("CURR: ",)




	# Suggestions:
	# Heuristic: least constraining value (LCV)
	# LCV = prioritize values that filter out fewer values in other variables' domains
	# Hint: you will use state.copy() for new_state, use new_state.assign, and use forward_checking() on new_state
	# Count the number of filtered values by comparing the total from current state and new_state


### FILTERING FUNCTIONS ###

def do_nothing(state,variable):
	problem = state.problem
	return # do nothing

def forward_checking(state,variable):
	problem = state.problem
	solution = state.solution
	print("SOLUTION: ",solution)
	for constraint in problem.constraints:
		if variable not in constraint.variables:
			continue # skip if unrelated to variable

		for other_var in constraint.variables:
			if other_var == variable: continue # skip self
			if other_var in solution: continue # skip assigned 

			valid_values = []
			for value in state.domain[other_var]:
				new_solution = solution.copy()
				new_solution[other_var] = value 

				pass_test = constraint.test(new_solution)
				if pass_test:
					valid_values.append(value)

			state.domain[other_var] = valid_values
			# print("Number of valid values: ",len(valid_values))


