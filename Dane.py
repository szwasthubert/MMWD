import numpy as np
from typing import List

#TODO: vectorize everything

class Generator:

    def __init__(self, power_production: np.ndarray, production_cost: int,
                 startup_cost: int, minimal_working_time: int, renewable: bool, ID: int):
        self.power_production = power_production
        self.production_cost = production_cost
        self.startup_cost = startup_cost
        self.minimal_working_time = minimal_working_time
        self.renewable = renewable
        self.production_to_cost_ratio = np.mean(power_production/production_cost)
        self.ID = ID


class Solution:

    def __init__(self, generators: List[Generator], work_matrix: np.ndarray,
                 renewable_quota: float, penalty: int, grid_cost: int, power_requirement: np.ndarray):

        self.generators = generators
        self.work_matrix = work_matrix
        self.renewable_quota = renewable_quota
        self.penalty = penalty
        self.grid_cost = grid_cost
        self.power_requirement = power_requirement
        if len(generators) != work_matrix.shape[0]:
            raise ValueError('generator data size mismatch')
        if len(power_requirement) != work_matrix.shape[1]:
            raise ValueError('time data size mismatch')

    def calculate_cost(self):
        cost = 0
        produced_total_energy = 0
        produced_renewable_energy = 0

        for generator, row in zip(self.generators, self.work_matrix):
            generator_state = 0
            for state in row:
                cost += state * generator.production_cost
                produced_total_energy += generator.power_production * state
                if generator.renewable:
                    produced_renewable_energy += generator.power_production * state
                if generator_state == 0 and state == 1:
                    generator_state = 1
                    cost += generator.startup_cost
                if generator_state == 1 and state == 0:
                    generator_state = 0

        cost += (np.sum(self.power_requirement) - produced_total_energy) * self.grid_cost

        if produced_renewable_energy/produced_total_energy < self.renewable_quota:
            cost += self.penalty

        return cost

    def generate_neighborhood(self, taboo_list: dict):

        def generate_neighborhood_economically(self: Solution, taboo_list):
            self.generators.sort(key=lambda generator: generator.production_to_cost_ratio)
            best_generator = next(self.generators)
            # Aspiration criterion
            try:
                while best_generator.ID in taboo_list['economically']:
                    best_generator = next(self.generators)
            except StopIteration:  # Everything in taboo list
                pass
            reversed_generators = reversed(self.generators)
            worst_generator = next(reversed_generators)
            # Aspiration criterion
            try:
                while worst_generator.ID in taboo_list['economically']:
                    worst_generator = next(reversed_generators)
            except StopIteration:  # Everything in taboo list
                pass
            if worst_generator.ID == best_generator.ID:
                raise Exception('Taboo list forbids for too long')  # TODO: define exception

            random_intervals = np.array([np.random.randint(0, high=len(self.work_matrix[best_generator.ID]) - best_generator.minimal_working_time)])
            for i in range(9):
                np.append(random_intervals, np.array([np.random.randint(0, high=len(self.work_matrix[best_generator.ID]) - best_generator.minimal_working_time)]))
            new_work_matrices = []

        def generate_neighborhood_renewably(self):
            pass

        def generate_more_power(self):
            pass








# def is_taboo(taboo_list, solution: Solution):
#     pass
