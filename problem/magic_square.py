from problem.problem import Problem 
from problem.constraints import *

def problem(N):
	""" Create an NxN magic square """

	# Magic square numbers
	min_number = 1
	max_number = N*N
	numbers = range(min_number,max_number+1)

	# Variables
	variables = []
	for y in range(N): 
		for x in range(N):
			square = '%d,%d' % (x,y) # x,y coords
			variables.append(square)

	# Domain 
	domain = {}
	for var in variables:
		domain[var] = list(numbers)

	# Constraints 
	# Note: Use ExactSum, where sum is magic_sum
	constraints = []
	# Hint: Find out how to solve for magic sum or magic constant
	# magic_sum = ???

	# 1) Different number per square
	# INSERT CODE HERE
	c = AllDifferent(variables)
	c.name = "AllDiff"
	constraints.append(c)

	# 2) Each column has same total (ExactSum: magic_sum)
	# Note: separate constraint for each column
	# INSERT CODE HERE
	target_sum = N * (((N**2)+1) / 2)
	print(target_sum)
	for num in range(0, N):
		row_list = []
		for var in variables:
			x, y = var.split(",")
			if y == str(num):
				row_list.append(var)
		c = ExactSum(row_list, target_sum)
		c.name = 'Exact Sum:Row %d' % num
		constraints.append(c)


	# 3) Each row has same total (ExactSum: magic_sum)
	# Note: separate constraint for each row
	# INSERT CODE HERE
	for num in range(0, N):
		col_list = []
		for var in variables:
			x, y = var.split(",")
			if x == str(num):
				col_list.append(var)
		c = ExactSum(col_list, target_sum)
		c.name = 'Exact Sum:Col %d' % num
		constraints.append(c)

	# 4) Forward diagonal has same total (ExactSum: magic_sum)
	# e.g. (0,0), (1,1), ..., (N-1,N-1)
	# INSERT CODE HERE
	diagonal_list = []
	for var in variables:
		x, y = var.split(",")
		if x == y:
			diagonal_list.append(var)
	c = ExactSum(diagonal_list, target_sum)
	c.name = 'Exact Sum:Forward Diagonal'
	constraints.append(c)
		

	# 5) Backward diagonal has same total (ExactSum: magic_sum)
	# e.g. N = 3, (0,2), (1,1), (2,0)
	# INSERT CODE HERE
	b_diagonal_list = []
	for var in variables:
		x, y = var.split(",")
		if int(y) == (N-1)-int(x):
			b_diagonal_list.append(var)
	c = ExactSum(b_diagonal_list, target_sum)
	c.name = 'Exact Sum:Backward Diagonal'
	constraints.append(c)

	# All hard constraints
	for c in constraints:
		c.penalty = float('inf')

	# Create problem
	problem = Problem(variables,domain,constraints)
	problem.name = 'Magic Square'
	problem.N = N
	problem.solution_format = solution_format

	return problem


def solution_format(problem,solution):
	output = []
	N = problem.N
	for y in range(N):
		output.append('\t')
		for x in range(N):
			var = '%d,%d' % (x,y)
			output.append(str(solution[var]).ljust(5))
		output.append('\n')

	return ''.join(output)
