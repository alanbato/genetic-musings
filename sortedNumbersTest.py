import unittest
import datetime
import genetic

class SortedNumbersTests(unittest.TestCase):

    def test_sort_ten_numbers(self):
        self.sort_numbers(10)

    def sort_numbers(self, total_numbers):
        gene_set = list(range(100))
        start_time = datetime.datetime.now()

        def display_fn(candidate):
            return display(candidate, start_time)

        def fitness_fn(candidate):
            return get_fitness(candidate)

        optimal_fitness = Fitness(total_numbers, 0)
        best = genetic.get_best(fitness_fn, total_numbers,
                                optimal_fitness, gene_set,
                                display_fn)
        self.assertTrue(not optimal_fitness > best.fitness)


class Fitness:
    numbers_in_seq_count = None
    total_gap = None
    def __init__(self, numbers_in_seq_count, total_gap):
        self.numbers_in_seq_count = numbers_in_seq_count
        self.total_gap = total_gap

    def __gt__(self, other):
        if self.numbers_in_seq_count != other.numbers_in_seq_count:
            return self.numbers_in_seq_count > other.numbers_in_seq_count
        return self.total_gap < other.total_gap

    def __str__(self):
        return '{0} Sequential, {1} Total Gap'.format(
            self.numbers_in_seq_count,
            self.total_gap)


def get_fitness(genes):
        fitness = 1  # The first number doesn't have a left partner
        gap = 0
        for i in range(1, len(genes)):  #Skip the first one
            if genes[i] > genes[i-1]:
                fitness += 1
            else:
                gap += genes[i-1] - genes[i]
        return Fitness(fitness, gap)

def display(candidate, start_time):
    time_diff = datetime.datetime.now() - start_time
    genes = ', '.join([str(gene) for gene in candidate.genes])
    print('{0}\t{1}\t{2}'.format(genes, candidate.fitness,
    time_diff))
