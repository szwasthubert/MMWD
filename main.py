from Dane import *

taboo_list = {'economically': [], 'renewably': [], 'more_power': []}

generators = []
work_matrix = np.array([])
renewable_quota = 0.4
penalty = 1000
grid_cost = 120
power_requirement = np.ones(24)

#Starting solution
solution = Solution(generators, work_matrix, renewable_quota, penalty, grid_cost, power_requirement)
best_solution = solution
best_cost = solution.calculate_cost()

for i in range(1000):
    solution = solution.generate_neighborhood(taboo_list,timeout=10)
    solution_cost = solution.calculate_cost()
    if solution_cost <= best_cost:
        best_solution = solution
        best_cost = solution_cost

    for key,value in taboo_list.items():
        indicies_to_remove = []
        for index, attribute in enumerate(value):
            attribute[1]-=1
            if attribute[1]==0:
               indicies_to_remove.append(index)
        for index in indicies_to_remove:
            del value[index]







