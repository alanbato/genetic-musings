import random


class Chromosome:
    """A simple pair of genes and fitness"""
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

def _get_improvement(new_child, new_parent):
    best_parent = new_parent()
    yield best_parent
    while True:
        child = new_child(best_parent)
        if best_parent.fitness > child.fitness:
            continue
        if not child.fitness > best_parent.fitness:
            best_parent = child
            continue
        yield child
        best_parent = child

def _mutate(parent, gene_set, get_fitness):
    index = random.randrange(0, len(parent.genes))
    child_genes = parent.genes[:]
    new_gene, alternate_gene = random.sample(gene_set, 2)
    child_genes[index] = (new_gene if new_gene != child_genes[index]
                          else alternate_gene)
    fitness = get_fitness(child_genes)
    return Chromosome(child_genes, fitness)


def get_best(get_fitness, target_len, optimal_fitness, gene_set, display):
    random.seed()

    def mutate_fn(parent):
        return _mutate(parent, gene_set, get_fitness)

    def generate_parent_fn():
        return _generate_genes(target_len, gene_set, get_fitness)

    for improvement in _get_improvement(mutate_fn, generate_parent_fn):
        display(improvement)
        if not optimal_fitness > improvement.fitness:
            return improvement
