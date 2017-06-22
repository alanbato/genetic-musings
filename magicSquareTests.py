import unittest
import datetime
import random

import genetic

class MagicSquareTests(unittest.TestCase):
    def test_size_3(self):
        self.generate(3, 50)

    def test_size_5(self):
        self.generate(5, 500)

    def generate(self, diagonal_size, max_age):
        square = diagonal_size ** 2
        gene_set = [i for i in range(1, square+1)]
        expected_sum = diagonal_size * (square+1) / 2

        def fitness_fn(genes):
            return get_fitness(genes, diagonal_size, expected_sum)

        gene_indexes = [i for i in range(len(gene_set))]
        def mutate_fn(genes):
            mutate(genes, gene_indexes)

        def create_fn():
            return random.sample(gene_set, len(gene_set))

        def display_fn(candidate):
            display(candidate, diagonal_size, start_time)

        optimal_value = Fitness(0)
        start_time = datetime.datetime.now()
        best = genetic.get_best(fitness_fn, square, optimal_value,
                                gene_set, display_fn, mutate_fn,
                                create_fn, max_age)


class Fitness:
    sum_of_differences = None

    def __init__(self, sum_of_differences):
        self.sum_of_differences = sum_of_differences

    def __gt__(self, other):
        return self.sum_of_differences < other.sum_of_differences

    def __str__(self):
        return '{0}'.format(self.sum_of_differences)


def get_sums(genes, size):
    row_sums = [0] * size
    column_sums = [0] * size
    southeast = 0
    northeast = 0

    for row in range(size):
        for column in range(size):
            value = genes[row * size + column]
            row_sums[row] += value
            column_sums[column] += value
        southeast += genes[row * size + row]
        northeast += genes[row * size + (size-1-row)]
    return row_sums, column_sums, northeast, southeast

def get_fitness(genes, size, expected_sum):
    row_sums, column_sums, northeast, southeast = get_sums(genes, size)

    sum_of_differences = sum(int(abs(s - expected_sum))
                             for s in (row_sums + column_sums +
                                       [southeast, northeast])
                             if s != expected_sum)
    return Fitness(sum_of_differences)

def mutate(genes, indexes):
    indexA, indexB = random.sample(indexes, 2)
    genes[indexA], genes[indexB] = genes[indexB], genes[indexA]

def display(candidate, size, start_time):
    time_diff = datetime.datetime.now() - start_time

    rows, columns, northeast, southeast = get_sums(candidate.genes, size)

    for row_num in range(size):
        row = candidate.genes[row_num * size:(row_num+1) * size]
        print('\t ', row, '=', rows[row_num])
    print('   ', northeast, ' ', columns, '\t', southeast)
    print(' - - - - - - - - - - -', candidate.fitness, str(time_diff))
