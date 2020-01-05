from random import randrange, choice
import numpy as np


def prepare_generator(size: str, gen_type: str, ID: int, length: int):

    # ID
    output_str = f'{ID} '
    # Renewability (nuclear treated as renewable)
    output_str += '1 ' if gen_type in ['Wind', 'Solar', 'Nuclear', 'Hydro'] else '0 '
    # Minimal working time
    output_str += '1 ' if gen_type in ['Wind', 'Solar', 'Hydro'] else '4 ' if gen_type in ['Gas', 'Oil'] else \
                  '72 ' if gen_type == 'Coal' else '504 '
    production_cost = {'Wind': 55, 'Coal': 100, 'Solar': 73, 'Hydro': 64, 'Gas': 90, 'Nuclear': 95, 'Oil': 87}
    size_multipliers = {'Medium': 1, 'Large': 1.7, 'Huge': 2.9}
    startup_cost = production_cost[gen_type] * size_multipliers[size]
    output_str += str(startup_cost)
    output_str += str(production_cost[gen_type])

    production_boundaries = {'Wind': (250, 1500), 'Coal': (350, 1000), 'Solar': (100, 550), 'Hydro': (100, 300),
                             'Gas': (400, 700), 'Nuclear': (800, 1200), 'Oil': (400, 700)}

    upper_bound = production_boundaries[gen_type][1]
    lower_bound = production_boundaries[gen_type][0]
    production_range = upper_bound - lower_bound

    if size == 'Medium':
        max_production = randrange(lower_bound, lower_bound + int(production_range/3))
    elif size == 'Large':
        max_production = randrange(lower_bound + int(production_range/3), lower_bound + int(2*production_range/3))
    else:
        max_production = randrange(lower_bound + int(2*production_range/3), upper_bound)

    power_production = np.full(length, max_production)

    if gen_type == 'Solar':
        time = np.linspace(0, length - 1, length)
        availability = np.sin(2*np.pi*time/24 - np.pi/2)
        availability[availability < 0] = 0
        power_production = np.multiply(power_production, availability)

    if gen_type in ['Hydro', 'Wind']:
        availability = np.random.randint(2, size=length)
        power_production = np.multiply(power_production, availability)

    for elem in power_production:
        output_str += str(elem) + ' '

    return output_str[:-1] + '\n'


for i in range(1,13):
    row_count = sum(1 for line in open(f'2016_{str(i)}.csv', 'r'))
    with open(f'2016_{str(i)}_generators.csv', 'w') as f:
        f.write(prepare_generator('Huge', 'Nuclear', 0, row_count))
        f.write(prepare_generator('Huge', 'Coal', 1, row_count))
        for j in range(10):
            f.write(prepare_generator('Medium', 'Solar', 2+j, row_count))
        for j in range(10):
            f.write(prepare_generator('Large', 'Coal', 12+j, row_count))
        for j in range(10):
            f.write(prepare_generator('Medium', 'Wind', 22+j, row_count))
        for j in range(10):
            f.write(prepare_generator('Large', 'Oil', 32+j, row_count))

for i in range(1, 13):
    row_count = sum(1 for line in open(f'2017_{str(i)}.csv', 'r'))
    with open(f'2017_{str(i)}_generators.csv', 'w') as f:
        for j in range(45):
            f.write(prepare_generator(choice(['Medium', 'Large', 'Huge']),
                                      choice(['Wind', 'Coal', 'Solar', 'Hydro', 'Gas', 'Oil']), j, row_count))

for i in range(1, 9):
    row_count = sum(1 for line in open(f'2018_{str(i)}.csv', 'r'))
    with open(f'2018_{str(i)}_generators.csv', 'w') as f:
        for j in range(55):
            f.write(prepare_generator('Medium', choice(['Wind', 'Coal', 'Solar', 'Hydro', 'Gas', 'Oil']), j, row_count))
