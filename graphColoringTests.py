import csv
import unittest
import datetime
from collections import Counter

import genetic

class Rule:
    node = None
    adjacent = None

    def __init__(self, node, adjacent):
        if node < adjacent:
            node, adjacent = adjacent, node
        self.node = node
        self.adjacent = adjacent

    def __eq__(self, other):
        return self.node == other.node and self.adjacent == other.adjacent

    def __hash__(self):
        return hash(self.node) * 397 ^ hash(self.adjacent)  # Hashing magics

    def __str__(self):
        return '{self.node} -> {self.adjacent}'.format(self=self)

    def is_valid(self, genes, node_index_lookup):
        index = node_index_lookup[self.node]
        adjacent_state_index = node_index_lookup[self.adjacent]
        return genes[index] != genes[adjacent_state_index]


class GraphColoringTests(unittest.TestCase):
    def test(self):
        states = load_data('states.csv')
        rules = build_rules(states)
        optimal_value = len(rules)
        state_index_lookup = {key:index for index, key
                              in enumerate(sorted(states))}
        colors = ['Orange', 'Yellow', 'Green', 'Blue']
        color_lookup = {color[0]: color for color in colors}
        gene_set = color_lookup.keys()
        start_time = datetime.datetime.now()

        def display_fn(candidate):
            display(candidate, start_time)

        def fitness_fn(genes):
            return get_fitness(genes, rules, state_index_lookup)

        best = genetic.get_best(fitness_fn, len(states), optimal_value,
                                gene_set, display_fn)
        self.assertTrue(not optimal_value > best.fitness)
        keys = sorted(states.keys())
        for state, color_key in zip(keys, best.genes):
            color = color_lookup[color_key]
            print('{state} is {color}'.format(state=state,
                                              color=color))


def load_data(filename):
    lookup = None
    with open(filename, mode='r') as input_file:
        reader = csv.reader(input_file)
        lookup = {row[0]: row[1].split(';') for row in reader if row}
    return lookup

def build_rules(items):
    rules_counter = Counter()
    for state, adjacent in items.items():
        for adjacent_state in adjacent:
            if adjacent_state == "":
                continue
            rule = Rule(state, adjacent_state)
            rules_counter.update([rule])
    for rule, count in rules_counter.items():
        if count != 2:
            print("Rule {0} is not bidirectional".format(rule))
    return rules_counter.keys()

def display(candidate, start_time):
    time_diff = datetime.datetime.now() - start_time
    genes = ''.join(candidate.genes)
    print('{0}\t{1}\t{2}'.format(genes, candidate.fitness, time_diff))

def get_fitness(genes, rules, state_index_lookup):
    rules_ok = sum(1 for rule in rules
                   if rule.is_valid(genes, state_index_lookup))
    return rules_ok
