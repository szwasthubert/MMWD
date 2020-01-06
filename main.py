from Dane import *
import matplotlib.pyplot as plt

taboo_list = {'economically': [], 'renewably': [], 'more_power': []}


type_1_power = np.array([4, 4, 4])
type_2_power = np.array([7, 0, 7])
type_3_power = np.array([1, 1, 1])

gen_1 = Generator(type_1_power, 250, 50, 2, False, 0)
gen_2 = Generator(type_2_power, 150, 70, 1, True, 1)
gen_3 = Generator(type_2_power, 150, 70, 1, True, 2)
gen_4 = Generator(type_3_power, 40, 10, 1, False, 3)
gen_5 = Generator(type_3_power, 40, 10, 1, False, 4)

generators = [gen_1, gen_2, gen_3, gen_4, gen_5]
work_matrix = np.array([[1,1,0],
                        [1,0,1],
                        [0,0,1],
                        [0,1,1],
                        [1,1,1]])

renewable_quota = 0.2
penalty = 50
grid_cost = 140
power_requirement = np.array([3, 4, 2])

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
        for index, attribute in value:
            attribute-=1
            value[i][1] = attribute
            i+=1
            if attribute==0:
               indicies_to_remove.append(index)
        for index in indicies_to_remove:
            del value[index]
    best_cost_vector.append(best_cost)

plt.plot(best_cost_vector)
plt.show()





