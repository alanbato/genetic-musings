import random
from bisect import bisect_left
from math import exp

class Chromosome:
    """A simple pair of genes and fitness"""
    genes = None
    fitness = None
    age = 0
    def __init__(self, genes, fitness):
        self.genes = genes
        self.fitness = fitness

def _generate_genes(length, gene_set, get_fitness):
    genes = []
    while len(genes) < length:
        sample_size = min(length - len(genes), len(gene_set))
        genes.extend(random.sample(gene_set, sample_size))
    fitness = get_fitness(genes)
    return Chromosome(genes, fitness)

def _get_improvement(new_child, new_parent, max_age):
    parent = best_parent = new_parent()
    yield best_parent
    historical_fitnesses = [best_parent.fitness]
    while True:
        child = new_child(parent)
        if parent.fitness > child.fitness:
            if max_age is None:
                continue
            parent.age += 1
            if max_age > parent.age:
                continue
            index = bisect_left(historical_fitnesses, child.fitness)
            difference = len(historical_fitnesses) - index
            similarity = difference / len(historical_fitnesses)
            if random.random() < exp(-similarity):
                parent = child
            else:
                parent = best_parent
                parent.age = 0
        elif not child.fitness > parent.fitness:
            # Same fitness
            child.age = parent.age + 1
            parent = child
        else:
            parent = child
            parent.age = 0
        if child.fitness > best_parent.fitness:
            yield child
            best_parent = child
            historical_fitnesses.append(child.fitness)

def _mutate(parent, gene_set, get_fitness):
    index = random.randrange(0, len(parent.genes))
    child_genes = parent.genes[:]
    new_gene, alternate_gene = random.sample(gene_set, 2)
    child_genes[index] = (new_gene if new_gene != child_genes[index]
                          else alternate_gene)
    fitness = get_fitness(child_genes)
    return Chromosome(child_genes, fitness)

def _mutate_custom(parent, custom_mutate, get_fitness):
    child_genes = parent.genes[:]
    custom_mutate(child_genes)
    fitness = get_fitness(child_genes)
    return Chromosome(child_genes, fitness)

def get_best(get_fitness, target_len, optimal_fitness, gene_set, display,
             custom_mutate=None, custom_create=None, max_age=None):
    random.seed()
    if custom_mutate is None:
        def mutate_fn(parent):
            return _mutate(parent, gene_set, get_fitness)
    else:
        def mutate_fn(parent):
            return _mutate_custom(parent, custom_mutate, get_fitness)

    if custom_create is None:
        def generate_parent_fn():
            return _generate_genes(target_len, gene_set, get_fitness)
    else:
        def generate_parent_fn():
            genes = custom_create()
            return Chromosome(genes, get_fitness(genes))

    for improvement in _get_improvement(mutate_fn, generate_parent_fn, max_age):
        display(improvement)
        if not optimal_fitness > improvement.fitness:
            return improvement
