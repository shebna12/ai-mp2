import random

### VARIABLE ORDERING FUNCTIONS ###

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
	# Write your variable ordering code here 
	# Return an unassigned variable 

	# Suggestions: 
	# Heuristic 1: minimum remaining values = select variables with fewer values left in domain
	# Heuristic 2: degree heuristic = select variables related to more constraints
	# Can use just one heuristic, or chain together heuristics (tie-break)


	#----------USING MRV HEURISTIC-------------
	unassigned_vars = problem.unassigned_variables(solution)
	min_var = unassigned_vars[0]

	#get number of constraints of each unassigned var
	for var in unassigned_vars:
		#number of remaining values for domain and min
		num_remaining_dom = len(domain[var])
		num_remaining_min = len(domain[min_var])

		#for checking. can be omitted soon.
		# print("DOM-remaining for ", var, ":", num_remaining_dom)
		# print("DOM-remaining for min var", var, ":", num_remaining_min)

		if num_remaining_dom < num_remaining_min:
			min_var = var

		elif num_remaining_dom == num_remaining_min:
			#if domain and min have same number of remaining values
			if len(var) > len(min_var):
				#Select variable with max constraints
				min_var = var

	return min_var


### VALUE ORDERING FUNCTIONS ###

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

	# INSERT CODE HERE
	# Write your value ordering code here 
	# Return sorted values, accdg. to some heuristic
	return random_order(state, variable)

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

