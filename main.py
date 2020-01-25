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
power_requirement = power_requirement[:450]

generators_param = np.loadtxt(data_generators, delimiter=' ')

# print(np.array(generators_param[0]))
generators = np.array([Generator(np.array(generators_param[0, 5:455]),
                       int(generators_param[0, 4]), int(generators_param[0, 3]), int(generators_param[0, 2]),
                       bool(generators_param[0, 1]), int(0))])

for i in range(1, len(generators_param)):
    generators = np.append(generators, np.array([Generator(np.array(generators_param[i, 5:455]),
                                                           int(generators_param[i, 4]), int(generators_param[i, 3]),
                                                           int(generators_param[i, 2]),
                                                           bool(generators_param[i, 1]), int(i))]), axis=0)

generators = generators[:45]
taboo_list = {'economically': [], 'renewably': [], 'more_power': [], 'too_much_power': []}

# work_matrix = np.array(np.random.randint(0, 2, size=(len(generators), len(power_requirement))))
work_matrix = np.zeros((len(generators), len(power_requirement)))

# for generator in generators:
#     if generator.renewable:
#         for index, hour in enumerate(generator.power_production):
#             if hour > 0:
#                 work_matrix[generator.ID][index] = 1
renewable_quota = 0.2
penalty = 1e8
grid_cost = 200
iterations = 10

generators = list(generators)

# Generator list sorting
renewability_bonus = 50
generators.sort(key=lambda generator: generator.production_to_cost_ratio, reverse=True)

generators_for_renewable = sorted(generators,
                                  key=lambda generator: generator.production_to_cost_ratio +
                                                        int(generator.renewable) * renewability_bonus,
                                  reverse=True)

# Starting solution
solution = Solution(generators, work_matrix, renewable_quota, penalty, grid_cost, power_requirement, generators_for_renewable)
best_solution = solution
best_cost = solution.calculate_cost()[0]
best_cost_vector = [best_cost]
plot_data = {'neighbourhood': {'economically': 0,
                               'renewably': 0,
                               'more power': 0,
                               'too_much_power': 0},
             'taboo forbidden': {'economically': np.zeros(len(generators)),
                                 'renewably': np.zeros(len(generators)),
                                 'more power': np.zeros(len(generators)),
                                 'too_much_power': np.zeros(len(generators)) },
             'renewable energy ratio': [],
             'underproduction percent': [],
             'overproduction percent': [],
             'active generators': [0 for i in range(iterations)]
             }

for j in range(iterations):
    solution, used_neighbourhood, taboo_forbids = solution.generate_neighborhood(taboo_list)
    plot_data['neighbourhood'][used_neighbourhood] += 1
    plot_data['taboo forbidden'][used_neighbourhood] += taboo_forbids
    solution_cost, underproduction_ratio, renewable_ratio, overproduction = solution.calculate_cost()
    plot_data['renewable energy ratio'].append(renewable_ratio)
    plot_data['underproduction percent'].append(underproduction_ratio)
    plot_data['overproduction percent'].append(overproduction)
    for row in best_solution.work_matrix:
        if np.any(row):
            plot_data['active generators'][j] += 1

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
plt.title('Koszt najlepszego znalezionego rozwiązania')
plt.xlabel('Iteracja')
plt.show()
plt.plot(plot_data['active generators'])
plt.title('Aktywne generatory')
plt.xlabel('Iteracja')
plt.show()
plt.plot(plot_data['renewable energy ratio']*100)
plt.title('Procent energii odnawialnej')
plt.xlabel('Iteracja')
plt.show()
plt.plot(plot_data['underproduction percent'])
plt.title('Procent energii dokupionej z sieci')
plt.xlabel('Iteracja')
plt.show()
fig, axs = plt.subplots(ncols=2)
fig.suptitle('Zabronienia dla każdego z sąsiedztw cz. 1')
axs[0].bar(range(len(plot_data['taboo forbidden']['economically'])), plot_data['taboo forbidden']['economically'])
axs[0].set_title('Economically')
axs[0].set_xlabel('Iteracja')
axs[0].set_ylabel('Ilość zabronień')
axs[1].bar(range(len(plot_data['taboo forbidden']['renewably'])), plot_data['taboo forbidden']['renewably'])
axs[1].set_title('Renewably')
axs[1].set_xlabel('Iteracja')
axs[1].set_ylabel('Ilość zabronień')
fig, axs = plt.subplots(ncols=2)
fig.suptitle('Zabronienia dla każdego z sąsiedztw cz. 2')
axs[0].bar(range(len(plot_data['taboo forbidden']['more power'])), plot_data['taboo forbidden']['more power'])
axs[0].set_title('More power')
axs[0].set_xlabel('Iteracja')
axs[0].set_ylabel('Ilość zabronień')
axs[1].bar(range(len(plot_data['taboo forbidden']['too_much_power'])), plot_data['taboo forbidden']['too_much_power'])
axs[1].set_title('Too_much_power')
axs[1].set_xlabel('Iteracja')
axs[1].set_ylabel('Ilość zabronień')
plt.show()