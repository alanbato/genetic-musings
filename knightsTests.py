from collections import defaultdict
import unittest
import datetime
import random

import genetic


class Position:
    x = None
    y = None

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return '{0},{1}'.format(self.x, self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return self.x * 1000 + self.y

class Board:
    def __init__(self, positions, width, height):
        board = [['.'] * width for _ in range(height)]
        for index in range(len(positions)):
            knight_position = positions[index]
            board[knight_position.y][knight_position.x] = 'K'
        self._board = board
        self._width = width
        self._height = height

    def get(self, row, column):
        return self._board[column][row]

    def show(self):
        # 0, 0 is bottom left corner
        print() #  padding
        for	i in reversed(range(self._height)):
            print(i, ' '.join(self._board[i]))
        print(' ', ' '.join(str(j) for j in range(self._width)))
        print()

class KnightTests(unittest.TestCase):
    # def test_3x4(self):
    #     self.find_knight_positions(4, 3, expected_knights=6)

    # def test_8x8(self):
    #     self.find_knight_positions(8, 8, expected_knights=14)

    def test_10x10(self):
        self.find_knight_positions(10, 10, expected_knights=22)

    def find_knight_positions(self, board_width, board_height, expected_knights):
        start_time = datetime.datetime.now()
        def display_fn(candidate):
            display(candidate, start_time, board_width, board_height)

        def fitness_fn(genes):
            return get_fitness(genes, board_width, board_height)

        all_positions = [Position(x, y)
                         for y in range(board_height)
                         for x in range(board_width)]

        if board_width < 6 or board_height < 6:
            non_edge = all_positions
        else:
            non_edge = [i for i in all_positions
                        if 0 < i.x < board_width - 1
                        and 0 < i.y < board_height -1]

        def get_random_position_fn():
            return random.choice(non_edge)

        def mutate_fn(genes):
            mutate(genes, board_width, board_height, all_positions,
                   non_edge)

        def create_fn():
            return create(get_random_position_fn, expected_knights)

        optimal_fitness = board_width * board_height
        best = genetic.get_best(fitness_fn, None, optimal_fitness, None,
                                display_fn, mutate_fn, create_fn)
        self.assertTrue(not optimal_fitness > best.fitness)

def get_attacks(location, board_width, board_height):
    possible_coords = [-2, -1, 1, 2]
    return [i for i in set(Position(x + location.x, y + location.y)
                        for x in possible_coords
                            if 0 <= x + location.x < board_width
                        for y in possible_coords
                            if 0 <= y + location.y < board_height
                        and abs(y) != abs(x))]

def create(get_random_position_fn, expected_knights):
    genes = [get_random_position_fn() for _ in range(expected_knights)]
    return genes

def mutate(genes, board_width, board_height, all_positions, non_edge):
    count = 2 if random.randint(0, 10) == 0 else 1
    while count > 0:
        count -= 1
        position_to_idx = defaultdict(list)
        for i, knight in enumerate(genes):
            for position in get_attacks(knight, board_width, board_height):
                position_to_idx[position].append(i)
        knight_idxs = set(i for i in range(len(genes)))
        unattacked = []
        for kvp in position_to_idx.items():
            if len(kvp[1]) > 1:
                continue
            if len(kvp[1]) == 0:
                unattacked.append(kvp[0])
                continue
            for p in kvp[1]:  # in this case len(kvp[1]) == 1
                if p in knight_idxs:
                    knight_idxs.remove(p)
        if len(unattacked) > 0:
            potential_positions = [p for positions
                                   in (get_attacks(pos, board_width, board_height)
                                       for pos in unattacked)
                                   if p in non_edge]
        else:
            potential_positions = non_edge

        if len(knight_idxs) == 0:
            gene_index = random.randrange(0, len(genes))
        else:
            gene_index = random.choice([i for i in knight_idxs])
        position = random.choice(potential_positions)
        genes[gene_index] = position

def get_fitness(genes, board_width, board_height):
    attacked = set(pos
                   for knight in genes
                   for pos in get_attacks(knight, board_width, board_height))
    return len(attacked)

def display(candidate, start_time, board_width, board_height):
    time_diff = datetime.datetime.now() - start_time
    board = Board(candidate.genes, board_width, board_height)
    board.show()
    genes = (str(gene) for gene in candidate.genes)
    print(' '.join(genes), candidate.fitness, str(time_diff))
