import random 
import itertools

### NEIGHBORHOOD FUNCTIONS ###

def change_one_value(state):
	problem = state.problem
	solution = state.solution

	neighbors = []
	for var in problem.variables:			# Try each variable
		for value in problem.domain[var]:	# Try each value
			if value == solution[var]: 
				continue 					# dont reassign to current value

			neighbor = state.copy()
			neighbor.solution[var] = value
			neighbor.changes = [(var,value)]	# remember what changed from state to neighbor
			neighbors.append(neighbor)

	return neighbors

def change_upto_two_values(state):
	problem = state.problem
	solution = state.solution

	neighbors = change_one_value(state)
	# INSERT CODE HERE
	# could change one value or two values
	# Hints for changing 2 values: 
	# use itertools.combinations and itertools.product
	# dont reassign to current values
	# update neighbor.changes
	neighbor_comb = list(itertools.combinations(problem.domain, 2))
	for item in neighbor_comb:
		var1, var2 = item
		domain1 = problem.domain[var1]
		domain2 = problem.domain[var2]
		for value in list(itertools.product(domain1, domain2)):
			value1, value2 = value
			if value1 == solution[var1] and value2 == solution[var2]:
				continue
			neighbor = state.copy()
			neighbor.solution[var1] = value1
			neighbor.solution[var2] = value2
			neighbor.changes = [(var1, value1), (var2, value2)]
			neighbors.append(neighbor)

	return neighbors


def swap_two_values(state):
	problem = state.problem
	solution = state.solution

	neighbors = []

	# INSERT CODE HERE
	# Hints: 
	# use itertools.combinations
	# dont swap same values
	# update neighbor.changes 
	neighbor_comb = list(itertools.combinations(problem.domain, 2))
	for item in neighbor_comb:
		var1, var2 = item
		value2 = solution[var1]
		value1 = solution[var2]
		# temp = solution[var1]
		# solution[var1] = solution[var2]
		# solution[var2] = temp
		# print(solution[var1], "\t", solution[var2])
		if value1 == solution[var1] and value2 == solution[var2]:
			continue

		neighbor = state.copy()
		neighbor.solution[var1] = value1
		neighbor.solution[var2] = value2
		neighbor.changes = [(var1, value1), (var2, value2)]
		neighbors.append(neighbor)

	return neighbors


### NEIGHBOR GENERATORS ###

def change_one_value_generator(state):
	problem = state.problem
	solution = state.solution

	while True:
		var = random.choice(problem.variables)			# Randomly select variable
		value = random.choice(problem.domain[var])		# Randomly select value

		neighbor = state.copy()
		neighbor.solution[var] = value
		neighbor.changes = [(var,value)]				# Remember what changed from state to neighbor
		yield neighbor

def change_upto_two_values_generator(state):
	problem = state.problem
	solution = state.solution

	# INSERT CODE HERE
	# Hints: 
	# Randomly select variables & values
	# update neighbor.changes 
	# yield neighbor

	while True:
		var1 = random.choice(problem.variables)
		var2 = random.choice(problem.variables)

		value1 = random.choice(problem.domain[var1])
		value2 = random.choice(problem.domain[var2])

		neighbor = state.copy()
		neighbor.solution[var1] = value1
		neighbor.solution[var2] = value2
		neighbor.changes = [(var1, value1), (var2, value2)]
		yield neighbor

def swap_two_values_generator(state):
	problem = state.problem
	solution = state.solution

	# INSERT CODE HERE
	# Hints: 
	# Randomly select variables to swap
	# update neighbor.changes 
	# yield neighbor

	while True:
		var1 = random.choice(problem.variables)
		var2 = random.choice(problem.variables)

		value1 = solution[var2]
		value2 = solution[var1]

		neighbor = state.copy()
		neighbor.solution[var1] = value1
		neighbor.solution[var2] = value2
		neighbor.changes = [(var1, value1), (var2, value2)]
		yield neighbor

### MAX-MIN CONFLICT ###

def min_conflict(state,var=None):
	problem = state.problem
	solution = state.solution

	if var is None:
		# Variable: random
		var = random.choice(problem.variables)

	# Value: min-conflict
	neighbors = []
	for value in problem.domain[var]:
		if value == solution[var]:
			continue # dont reassign to current value

		neighbor = state.copy()
		neighbor.solution[var] = value
		neighbor.changes = [(var,value)]

		# Get violations related to var
		violations = problem.all_hard_violations(neighbor.solution,var)
		neighbor.num_conflicts = len(violations)

		neighbors.append(neighbor)

	# Built-in legal neighbor function: min-conflict
	min_conflict = min(neighbors,key=lambda neighbor: neighbor.num_conflicts).num_conflicts
	legal_neighbors = [neighbor for neighbor in neighbors if neighbor.num_conflicts == min_conflict]

	return legal_neighbors

def max_min_conflict(state):
	problem = state.problem
	solution = state.solution

	# Variable: max-conflict
	num_conflicts = []
	for var in problem.variables:
		violations = problem.all_hard_violations(solution,var)
		num_conflicts.append(len(violations))
	max_conflict = max(num_conflicts)

	max_conflict_vars = []
	for i,var in enumerate(problem.variables):
		if num_conflicts[i] == max_conflict:
			max_conflict_vars.append(var)
	var = random.choice(max_conflict_vars)

	return min_conflict(state,var)

### LEGAL NEIGHBOR FUNCTIONS ###

def legal_neighbors(state,neighbors,comparison_fn):
	legal_neighbors = []
	for neighbor in neighbors:
		if comparison_fn(state,neighbor): 
			legal_neighbors.append(neighbor)
	return legal_neighbors

def all_neighbors(state,neighbors):
	comparison_fn = no_checking
	return legal_neighbors(state,neighbors,comparison_fn)

def strictly_decreasing(state,neighbors):
	comparison_fn = less_than
	return legal_neighbors(state,neighbors,comparison_fn)

def strictly_increasing(state,neighbors):
	comparison_fn = greater_than
	return legal_neighbors(state,neighbors,comparison_fn)

def non_increasing(state,neighbors):
	comparison_fn = less_than_equal
	return legal_neighbors(state,neighbors,comparison_fn)

def non_decreasing(state,neighbors):
	comparison_fn = greater_than_equal
	return legal_neighbors(state,neighbors,comparison_fn)

### COMPARISON FUNCTIONS ###

def no_checking(state,neighbor):
	return True
	
def less_than(state,neighbor):
	return neighbor.score < state.score

def less_than_equal(state,neighbor):
	return neighbor.score <= state.score

def greater_than(state,neighbor):
	return neighbor.score > state.score

def greater_than_equal(state,neighbor):
	return neighbor.score >= state.score

### SELECTION FUNCTIONS ###

def select_min(neighbors):
	best_neighbor = min(neighbors,key=lambda neighbor: neighbor.score)
	min_score = best_neighbor.score
	qualified = [neighbor for neighbor in neighbors if neighbor.score == min_score]
	return random.choice(qualified)

def select_max(neighbors):
	best_neighbor = max(neighbors,key=lambda neighbor: neighbor.score)
	max_score = best_neighbor.score
	qualified = [neighbor for neighbor in neighbors if neighbor.score == max_score]
	return random.choice(qualified)

def select_random(neighbors):
	qualified = neighbors
	return random.choice(qualified)

def select_first(neighbors):
	qualified = neighbors
	return qualified[0]
