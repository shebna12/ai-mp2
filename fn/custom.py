import random
import itertools

### CUSTOM NEIGHBOR GENERATORS ###

def maxone_neighbor_generator(state):
    problem = state.problem
    solution = state.solution

    while True:
        neighbor = state.copy()

        # Flip a random 0 to 1
        value = None
        while value != 0:
            # randomly select var with value 0 assigned in solution
            var = random.choice(problem.variables)
            value = solution[var]

        new_value = 1
        neighbor.solution[var] = new_value
        neighbor.changes = [(var,new_value)]
        yield neighbor


def knapsack_neighbor_generator(state):
    problem = state.problem
    solution = state.solution
    constraint = problem.constraints[0]

    while True:
        neighbor = state.copy()

        # INSERT CODE HERE
        # Idea: If knapsack is already full, neighbor = remove a random item from current solution (try to remove excess)
        #       If knapsack is not yet full, neighbor = randomly change up to 2 values (includes adding item, removing item, swapping)
        # Hint: use constraint.test(solution)
        # Hint: check the pattern of maxone_neigbor_generator
        # Dont forget to update neighbor.changes
        if not constraint.test(solution):
            new_value = 0
            while True:
                var = random.choice(problem.variables)
                value = solution[var]
                if value:
                    break
            neighbor.solution[var] = new_value
            neighbor.changes = [(var, new_value)]
        else:
            # while True:
                # var_comb = list(itertools.combinations(problem.variables, 2))
                # var1, var2 = random.choice(var_comb)
                # value_prod = list(itertools.product(problem.domain[var1], problem.domain[var2]))
                # value1, value2 = random.choice(value_prod)
            var1 = random.choice(problem.variables)
            var2 = random.choice(problem.variables)
            value1 = random.choice(problem.domain[var1])
            value2 = random.choice(problem.domain[var2])
                # if not ((value2 == solution[var1] and value1 == solution[var2]) or (value1 == solution[var1] and value2 == solution[var2])):
                # if (value2 != solution[var1] and value1 != solution[var2]) or (value1 != solution[var1] and value2 != solution[var2]):
                #     break
            
            neighbor.solution[var1] = value1
            neighbor.solution[var2] = value2
            neighbor.changes = [(var1, value1), (var2, value2)]
        yield neighbor
        

def vertex_cover_neighbor_generator(state):
    problem = state.problem
    solution = state.solution
    constraint = problem.constraints[0]
    # print(constraint.test(solution))

    while True:
    

        neighbor = state.copy()
        # INSERT CODE HERE
        # Idea: If all edges not yet covered, neighbor = add a random vertex to current solution (try to add more edges covered)
        #       If all edges already covered, neighbor = remove a random vertex from current solution (try to minimize no. of vertex used)
        # Hint: use constraint.test(solution)
        # Hint: check the pattern of maxone_neigbor_generator
        # Dont forget to update neighbor.changes
        # yield neighbor
        new_value = 1
        if constraint.test(solution):
            new_value = 0
            while True:
                var = random.choice(problem.variables)
                value = solution[var]
                if value:
                    break
        else:
            while True:
                var = random.choice(problem.variables)
                value = solution[var]
                if not value:
                    break
        
        # print(constraint.test(solution), var, new_value)
        neighbor.solution[var] = new_value
        neighbor.changes = [(var, new_value)]

        yield neighbor
