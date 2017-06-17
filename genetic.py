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
    best_genes = _generate_genes(target_len, gene_set, get_fitness)
    display(best_genes)
    if not optimal_fitness > best_genes.fitness:
        return best_genes
    while True:
        child = _mutate(best_genes, gene_set, get_fitness)
        if best_genes.fitness > child.fitness:
            continue
        if not child.fitness > best_genes.fitness:
            best_genes = child
            continue
        display(child)
        if not optimal_fitness > child.fitness:
            return child
        best_genes = child
