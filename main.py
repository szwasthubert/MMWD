from Dane import *
import matplotlib.pyplot as plt
import numpy as np
from random import random

##Read data from file
data_generators = open('data/2018_8_generators.csv','rt')
data_requirements = open('data/2018_8.csv','rt')

power_requirement = np.loadtxt(data_requirements)

generators_param = np.loadtxt(data_generators, delimiter=' ')

print(np.array(generators_param[0]))
generators = np.array([Generator(np.array(generators_param[0,5:]),int(generators_param[0,4]),int(generators_param[0,3]),int(generators_param[0,2]),
                                      bool(generators_param[0,1]),int(0))])

for i in range(1,len(generators_param)):
    generators = np.append(generators,np.array([Generator(np.array(generators_param[i,5:]),int(generators_param[i,4]),int(generators_param[i,3]),int(generators_param[i,2]),
                                   bool(generators_param[i,1]),int(i))]),axis=0)


taboo_list = {'economically': [], 'renewably': [], 'more_power': []}

work_matrix = np.array(np.random.randint(0,2,size=(len(generators),len(power_requirement))))
renewable_quota = 0.3
penalty = 50
grid_cost = 150

generators = list(generators)

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
plt.savefig('figures/fig_1.png')




