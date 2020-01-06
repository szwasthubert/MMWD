import numpy as np
from typing import List
from random import random
import datetime

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
        print("Cost calc beginning: ", datetime.datetime.now())
        cost = 0
        produced_total_energy = 0
        produced_renewable_energy = 0

        for generator, row in zip(self.generators, self.work_matrix):
            generator_state = 0
            produced_total_energy += generator.power_production * row
            produced_renewable_energy += generator.power_production * row * generator.renewable
            for state in row:
                cost += state * generator.production_cost
                if generator_state == 0 and state == 1:
                    generator_state = 1
                    cost += generator.startup_cost
                if generator_state == 1 and state == 0:
                    generator_state = 0

        ##Grid power purchase in the case of deficit from generator derrived electicity
        underproduction = np.max([np.sum(self.power_requirement) - np.sum(produced_total_energy),0])
        cost += underproduction * self.grid_cost

        ##Checking if renewability ratio requirement is met, otherwise adding to penalty
        renewable_ratio = np.sum(produced_renewable_energy)/np.sum(produced_total_energy)

        if renewable_ratio< self.renewable_quota:
            cost += self.penalty
        print("Cost calc end: ", datetime.datetime.now())
        return cost, underproduction/np.sum(self.power_requirement), renewable_ratio

    def generate_neighborhood(self, taboo_list: dict, timeout :int  = 10):

        def generate_neighborhood_economically(self: Solution, taboo_list,timeout):

            best_generator = self.generators[0]
            i = 0

            while best_generator.ID in (x[0] for x in taboo_list['economically']) and i!=len(self.generators):
                i+=1
                best_generator = self.generators[i]

            worst_generator = self.generators[-1]
            j=0

            # Aspiration criterion
            while worst_generator.ID in (x[0] for x in taboo_list['economically']) and j!=len(self.generators):
                j+=1
                worst_generator = self.generators[-j-1]

            if worst_generator.ID == best_generator.ID:
                raise Exception('Taboo list forbids for too long')  # TODO: define exception

            taboo_list['economically'].extend([[best_generator.ID, timeout], [worst_generator.ID, timeout]])
            if best_generator.renewable:
                intervals = generate_random_intervals_renewable(best_generator.minimal_working_time,
                                                                self.work_matrix.shape[0],4,
                                                                best_generator.power_production)
            else:
                intervals = generate_random_intervals(best_generator.minimal_working_time,self.work_matrix.shape[0],4)

            new_work_matrices = []
            for interval in intervals:
                new_work_matrix = np.copy(self.work_matrix)
                new_work_matrix[best_generator.ID,interval[0]:interval[0]+interval[1]] = 1
                new_work_matrix[worst_generator.ID, interval[0]:interval[0] + interval[1]] = 0
                new_work_matrices.append(new_work_matrix)

            best_cost = np.inf
            best_solution = self
            for matrix in new_work_matrices:
                solution = Solution(self.generators, matrix, self.renewable_quota, self.penalty,
                                    self.grid_cost, self.power_requirement)
                solution_cost = solution.calculate_cost()[0]
                if solution_cost <= best_cost:
                    best_cost = solution_cost
                    best_solution = solution

            return best_solution


        def generate_neighborhood_renewably(self, taboo_list,timeout):

            renewable_generators = [generator for generator in self.generators if generator.renewable]
            best_generator = renewable_generators[0]
            i=0

            while best_generator.ID in (x[0] for x in taboo_list['renewably']) and i!=len(renewable_generators):
                i+=1
                best_generator = renewable_generators[i]

            taboo_list['renewably'].append([best_generator.ID, timeout])

            intervals = generate_random_intervals_renewable(best_generator.minimal_working_time,
                                                            self.work_matrix.shape[0], 10,
                                                            best_generator.power_production)
            new_work_matrices = []

            for interval in intervals:
                new_work_matrix = np.copy(self.work_matrix)
                new_work_matrix[best_generator.ID, interval[0]:interval[0] + interval[1]] = 1
                new_work_matrices.append(new_work_matrix)

            best_cost = np.inf
            best_solution = self
            for matrix in new_work_matrices:
                solution = Solution(self.generators, matrix, self.renewable_quota, self.penalty,
                                    self.grid_cost, self.power_requirement)
                solution_cost = solution.calculate_cost()[0]
                if solution_cost <= best_cost:
                    best_cost = solution_cost
                    best_solution = solution

            return best_solution


        def generate_more_power(self, taboo_list, timeout, renewability_bonus):

            self.generators.sort(key=lambda generator: generator.production_to_cost_ratio+int(generator.renewable)*renewability_bonus,
                                 reverse=True)
            best_generator = self.generators[0]
            i = 0

            # Aspiration criterion
            while best_generator.ID in (x[0] for x in taboo_list['more_power']) and i!=len(self.generators):
                i+=1
                best_generator = self.generators[i]

            taboo_list['more_power'].append([best_generator.ID, timeout])

            if best_generator.renewable:
                intervals = generate_random_intervals_renewable(best_generator.minimal_working_time,
                                                                self.work_matrix.shape[0], 2,
                                                                best_generator.power_production)
            else:
                intervals = generate_random_intervals(best_generator.minimal_working_time, self.work_matrix.shape[0], 2)

            new_work_matrices = []
            for interval in intervals:
                new_work_matrix = np.copy(self.work_matrix)
                new_work_matrix[best_generator.ID, interval[0]:interval[0] + interval[1]] = 1
                new_work_matrices.append(new_work_matrix)

            best_cost = np.inf
            best_solution = self
            for matrix in new_work_matrices:
                solution = Solution(self.generators, matrix, self.renewable_quota, self.penalty,
                                    self.grid_cost, self.power_requirement)
                solution_cost = solution.calculate_cost()[0]
                if solution_cost <= best_cost:
                    best_cost = solution_cost
                    best_solution = solution

            return best_solution

        #TODO:consolidate intervals

        cost, underproduction, renewable_ratio = self.calculate_cost()

        probabilities_coefficients = {'economically': 0.4,
                                      'renewably': max(0, self.renewable_quota - renewable_ratio)/self.renewable_quota,
                                      'more_power': underproduction}

        coefficients_sum = sum(probabilities_coefficients.values())

        for key, value in probabilities_coefficients.items():
            probabilities_coefficients[key] = value/coefficients_sum

        random_value = random()

        if random_value < probabilities_coefficients['economically']:
            return generate_neighborhood_economically(self,taboo_list,timeout)
        elif random_value < probabilities_coefficients['economically'] + probabilities_coefficients['renewably']:
            return generate_neighborhood_renewably(self,taboo_list,timeout)
        else:
            return generate_more_power(self,taboo_list,timeout,renewability_bonus=200)


def generate_random_intervals(minimal_working_time, time_size, interval_quantity):

    try:
        interval_beginning = 0;
        interval_duration = 0;

        if minimal_working_time == time_size:
            interval_beginning = 0
            interval_duration = 1
        else:
            position = np.random.randint(0, time_size - minimal_working_time + 1)
            if position + minimal_working_time == time_size:
                interval_beginning = position
                interval_duration = minimal_working_time
            else:
                nterval_beginning = position
                interval_duration = np.random.randint(minimal_working_time, time_size - position + 2)


        random_intervals = np.array([[interval_beginning,interval_duration]]) #TODO append -> concatenate

        for i in range(interval_quantity-1):
            if minimal_working_time == time_size:
                random_intervals=np.append(random_intervals,np.array([[0,1]]),axis=0)
            else:
                position = np.random.randint(0, time_size - minimal_working_time + 1)
                if position + minimal_working_time == time_size:
                    random_intervals = np.append(random_intervals,[[position,minimal_working_time]],axis=0)
                else:
                    random_intervals = np.append(random_intervals,[[position, np.random.randint(minimal_working_time, time_size - position+2)]], axis=0)
    except ValueError:
        random_intervals = np.array([(0,time_size)])

    return random_intervals


def generate_random_intervals_renewable(minimal_working_time, time_size, interval_quantity, power_production):

    is_nonzero = np.concatenate(([0], np.not_equal(power_production, 0).view(np.int8), [0]))
    absdiff = np.abs(np.diff(is_nonzero))
    ranges = np.where(absdiff == 1)[0].reshape(-1, 2)
    starts = ranges[:, 0]
    stops = ranges[:, 1]
    lengths = stops - starts

    interval_sum = []

    for start, length in zip(starts, lengths):
        interval_set = generate_random_intervals(minimal_working_time, length, int(interval_quantity / len(starts)))
        interval_set[:,0] += start
        interval_sum.extend(list(interval_set))
    interval_sum = np.array(interval_sum)

    return interval_sum







