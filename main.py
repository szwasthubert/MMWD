from Dane import *
import matplotlib.pyplot as plt
import pandas as pd


##Read data from file
generators_param = pd.read_csv('data/2018_8_generators.csv', sep = ' ')

for i in range(0,len(generators_param)):
    generators_param.append(Generator(generators_param[i,3:],generators_param[i,2],generators_param[i,1],
                                      generators_param[i,0],i))
taboo_list = {'economically': [], 'renewably': [], 'more_power': []}
generators = []
work_matrix = []

renewable_quota = 0.3
penalty = 50
grid_cost = 150
power_requirement = np.array([12, 8, 10])

#Starting solution
solution = Solution(generators, work_matrix, renewable_quota, penalty, grid_cost, power_requirement)
best_solution = solution
best_cost = solution.calculate_cost()[0]
best_cost_vector = [best_cost]

for i in range(1000):
    solution = solution.generate_neighborhood(taboo_list)
    solution_cost = solution.calculate_cost()[0]
    if solution_cost <= best_cost:
        best_solution = solution
        best_cost = solution_cost
    for key,value in taboo_list.items():
        indicies_to_remove = []
        i = 0
        for ID, timeout in value:
            timeout-=1
            value[i][1] = timeout
            i+=1
            if timeout==0:
               indicies_to_remove.append(ID)
        for index in indicies_to_remove:
             i = 0
             while index != value[i][0]:
                 i+=1
             del value[i]

    best_cost_vector.append(best_cost)

plt.plot(best_cost_vector)
plt.show()





