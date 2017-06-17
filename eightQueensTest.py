import unittest
import datetime
import genetic

class EightQueensTests(unittest.TestCase):
    def test(self, size=8):
        gene_set = list(range(size))
        start_time = datetime.datetime.now()

        def display_fn(candidate):
            display(candidate, start_time, size)

        def fitness_fn(genes):
            return get_fitness(genes, size)

        optimal_fitness = Fitness(0)
        best = genetic.get_best(fitness_fn, 2*size, optimal_fitness,
                                gene_set, display_fn)
        self.assertTrue(not optimal_fitness > best.fitness)


class Board:
    def __init__(self, genes, size):
        board = [['.'] * size for _ in range(size)]
        for index in range(0, len(genes), 2):
            row = genes[index]
            column = genes[index+1]
            board[column][row] = 'Q'
        self._board = board

    def get(self, row, column):
        return self._board[column][row]

    def show(self):
        # 0, 0 is bottom left corner
        for	i in reversed(range(len(self._board))):
            print(' '.join(self._board[i]))


class Fitness:
    total = None

    def __init__(self, total):
        self.total = total

    def __gt__(self, other):
        return self.total < other.total

    def __str__(self):
        return str(self.total)


def get_fitness(genes, size):
    board = Board(genes, size)
    rows_with_queens = set()
    cols_with_queens = set()
    NE_diags_with_queens = set()
    SE_diags_with_queens = set()
    for row in range(size):
        for col in range(size):
            if board.get(row, col) == 'Q':
                rows_with_queens.add(row)
                cols_with_queens.add(col)
                NE_diags_with_queens.add(row + col)
                SE_diags_with_queens.add(size - 1 - row + col)
    total = (size - len(rows_with_queens)
             + size - len(cols_with_queens)
             + size - len(NE_diags_with_queens)
             + size - len(SE_diags_with_queens))
    return Fitness(total)

def display(candidate, start_time, size):
    time_diff = datetime.datetime.now() - start_time
    board = Board(candidate.genes, size)
    board.show()
    genes = ' '.join(str(gene) for gene in candidate.genes)
    print('{0}\t- {1}\t{2}'.format(genes, candidate.fitness,
                                   str(time_diff)))
