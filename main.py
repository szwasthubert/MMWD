from Dane import *
import matplotlib.pyplot as plt
import numpy as np
import datetime

start = datetime.datetime.now()
print('starting operation: ', start)
# Read data from file
data_generators = open('data/2018_5_generators.csv', 'rt')
data_requirements = open('data/2018_5.csv', 'rt')

power_requirement = np.loadtxt(data_requirements)

generators_param = np.loadtxt(data_generators, delimiter=' ')

# print(np.array(generators_param[0]))
generators = np.array([Generator(np.array(generators_param[0, 5:]),
                       int(generators_param[0, 4]), int(generators_param[0, 3]), int(generators_param[0, 2]),
                       bool(generators_param[0, 1]), int(0))])

for i in range(1, len(generators_param)):
    generators = np.append(generators, np.array([Generator(np.array(generators_param[i, 5:]),
                                                           int(generators_param[i, 4]), int(generators_param[i, 3]),
                                                           int(generators_param[i, 2]),
                                                           bool(generators_param[i, 1]), int(i))]), axis=0)


taboo_list = {'economically': [], 'renewably': [], 'more_power': [], 'too_much_power': []}

#work_matrix = np.array(np.random.randint(0, 2, size=(len(generators), len(power_requirement))))
work_matrix = np.zeros((len(generators), len(power_requirement)))
renewable_quota = 0.3
penalty = 1e8
grid_cost = 200
iterations = 1000

generators = list(generators)

# Generator list sorting
generators.sort(key=lambda generator: generator.production_to_cost_ratio, reverse=True)


# Starting solution
solution = Solution(generators, work_matrix, renewable_quota, penalty, grid_cost, power_requirement)
best_solution = solution
best_cost = solution.calculate_cost()[0]
best_cost_vector = [best_cost]
plot_data = {'neighbourhood': {'economically': 0,
                               'renewably': 0,
                               'more power': 0},
             'taboo forbidden': {'economically': np.zeros(len(generators)),
                                 'renewably': np.zeros(len(generators)),
                                 'more power': np.zeros(len(generators))},
             'renewable energy ratio': [],
             'underproduction percent': [],
             'active generators': [0 for i in range(iterations)]
             }

for j in range(100):
    solution = solution.generate_neighborhood(taboo_list)
    solution_cost = solution.calculate_cost()[0]
    if solution_cost <= best_cost:
        best_solution = solution
        best_cost = solution_cost
    for key, value in taboo_list.items():
        indicies_to_remove = []
        i = 0
        for ID, timeout in value:
            timeout -= 1
            value[i][1] = timeout
            i += 1
            if timeout == 0:
                indicies_to_remove.append(ID)
        for index in indicies_to_remove:
            i = 0
            while index != value[i][0]:
                i += 1
            del value[i]

    best_cost_vector.append(best_cost)
    print("Iteracja nr: ", j)

stop = datetime.datetime.now()
print('stopping operation: ', stop)
print('time taken: ', stop - start)

plt.plot(best_cost_vector)
plt.show()
plt.plot(plot_data['active generators'])
plt.show()
plt.plot(plot_data['renewable energy ratio'])
plt.show()
plt.plot(plot_data['underproduction percent'])
plt.show()