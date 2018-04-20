def maxone_fitness(state,feasibility_minimum):
	""" Fitness = no. of 1s """
	solution = state.solution
	score = sum(solution.values())
	# always add feasibility_minimum, since there are no constraints
	return feasibility_minimum + score

def knapsack_fitness(state,feasibility_minimum):
	problem = state.problem
	solution = state.solution


	chromosome = state
	Weight = problem.capacity
	totalWeight = 0

	if problem.find_hard_violation(solution) is not None: 
		# has violation: total weight exceeds capacity
		max_score = int(feasibility_minimum * 0.75)

		# INSERT CODE HERE
		# Idea: less excess weight = higher score
		# Hint: use item.weight, problem.capacity

		takenItems = [item for item in problem.variables if solution[item] == 1 ]
		Weight = problem.capacity
		weight = 0

		# Check weight of items in knapsack
		for item in takenItems:
			weight += item.weight

		excessWeight =  abs(Weight - weight)
		
		score = abs(max_score - excessWeight)
		return score

	else: 
		# no violations
		score = feasibility_minimum # min score for being valid solution

		# INSERT CODE HERE
		# Idea: higher total item value = higher score
		# Hint: use item.value
		takenItems = [item for item in problem.variables if solution[item] == 1 ]
		itemValue = 0

		for item in takenItems:
			itemValue += item.value

		score = feasibility_minimum + itemValue
		
	return score

def vertex_cover_fitness(state,feasibility_minimum):
	# print("--------------------------The beginning of Vertex Cover!-----------------------------")
	problem = state.problem
	solution = state.solution

	if problem.find_hard_violation(solution) is not None:  
		# has violation: some edges are not covered
		max_score = int(feasibility_minimum * 0.75)
		used_vertices = [v for v in problem.variables if solution[v] == 1]
		

		# INSERT CODE HERE
		# Idea: less uncovered edges = higher score
		# Hint: use problem.edges, used_vertices

		problem_edges_length = len(problem.edges)
		uncovered_edges = 0

		# Check if that edge contains a vertex from the used_vertices
		for edge in problem.edges:
			if not (edge[0] in used_vertices or edge[1] in used_vertices):
				uncovered_edges = uncovered_edges + 1

		
		score = max_score - uncovered_edges
		return score


	else:	
	
		# no violations
		score = feasibility_minimum # min score for being valid solution

		# INSERT CODE HERE
		# Idea: less vertices used = better
		# So, higher no. of unused vertices in solution = higher score

		used_vertices = [v for v in problem.variables if solution[v] == 1]

		# Get the opposite of used_vertices to fulfill the idea of "less vertices = better" scoring.
		used_vertices_length = len(used_vertices_length)
		problem_vertices_length = len(problem.variables)
		unused_vertices_length = problem_vertices_length - used_vertices_length
		

		# If the computed score is less than the assumed min score, return the computed score 
		score = feasibility_minimum + unused_vertices_length
		

	return score
			

