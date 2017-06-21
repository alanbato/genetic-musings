import unittest
import datetime
import random

import genetic

class CardTests(unittest.TestCase):
    def test(self):
        gene_set = [i for i in range(1,11)]
        start_time = datetime.datetime.now()

        def display_fn(candidate):
            display(candidate, start_time)

        def fitness_fn(genes):
            return get_fitness(genes)

        def mutate_fn(genes):
            mutate(genes, gene_set)

        optimal_fitness = Fitness(36, 360, 0)
        best = genetic.get_best(fitness_fn, 10, optimal_fitness, gene_set,
                                display_fn, custom_mutate=mutate_fn)
        self.assertTrue(not optimal_fitness > best.fitness)

class Fitness:
    group1 = None
    group2 = None
    duplicates = None
    total_diff = None

    def __init__(self, group1, group2, duplicates):
        self.group1 = group1
        self.group2 = group2
        self.duplicates = duplicates
        sum_diff = abs(36 - group1)
        product_diff = abs(360 - group2)
        self.total_diff = sum_diff + product_diff

    def __gt__(self, other):
        if self.duplicates != other.duplicates:
            return self.duplicates < other.duplicates
        return self.total_diff < other.total_diff

    def __str__(self):
        return 'sum: {0} prod: {1} dups: {2}'.format(self.group1,
                                                     self.group2,
                                                     self.duplicates)

def mutate(genes, gene_set):
    if len(genes) == len(set(genes)):
        count = random.randint(1, 4)
        for _ in range(count):
            indexA, indexB = random.sample(range(len(genes)), 2)
            genes[indexA], genes[indexB] = genes[indexB], genes[indexA]
    else:
        indexA = random.randrange(0, len(genes))
        indexB = random.randrange(0, len(gene_set))
        genes[indexA] = gene_set[indexB]

def get_fitness(genes):
    group1 = sum(genes[0:5])
    group2 = 1
    for gene in genes[5:10]:
        group2 *= gene
    duplicates = len(genes) - len(set(genes))
    return Fitness(group1, group2, duplicates)

def display(candidate, start_time):
    time_diff = datetime.datetime.now() - start_time
    print('{0} - {1}\t{2}\t{3}'.format(
        ", ".join(str(gene) for gene in candidate.genes[0:5]),
        ", ".join(str(gene) for gene in candidate.genes[5:10]),
        candidate.fitness, str(time_diff)))
