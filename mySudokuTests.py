# Solving sudoku excercise
import unittest
import datetime
import random

import genetic


def get_fitness(genes):
    board = SudokuBoard(genes)
    total = 0
    for i in range(0, 9):
        unique_row = set()
        unique_col = set()
        [unique_row.add(j) for j in board.get_row(i)]
        [unique_col.add(j) for j in board.get_col(i)]
        total += 9 - len(unique_row)
        total += 9 - len(unique_col)
    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            unique_sq = set()
            [unique_sq.add(j) for j in board.get_sq(i, j)]
            total += 9 - len(unique_sq)

    return Fitness(total)


def display(candidate, startTime):
    timeDiff = datetime.datetime.now() - startTime
    board = SudokuBoard(candidate.Genes)
    board.print()
    print("{}\t- {}\t{}".format(
        ' '.join(map(str, candidate.Genes)),
        candidate.Fitness,
        timeDiff))


class SudokuBoard:
    def __init__(self, genes):
        board = [[] * 9 for _ in range(9)]
        for index in range(0, len(genes), 9):
            row = genes[index:index+9]
            board[int(index/9)] = row
        self._board = board

    def get_row(self, row):
        return self._board[row]

    def get_col(self, col):
        col = [self._board[i][col] for i in range(0, len(self._board))]
        return col

    def get_sq(self, row, col):
        sq = [self._board[i][j] for i in range(row, row+3)
              for j in range(col, col+3)]
        return sq

    def print(self):
        def print_row_separator():
            print(('+' + 7*'-')*3 + '+')
        for i in range(0, len(self._board)):
            if i % 3 == 0:
                print_row_separator()
            row = self.get_row(i)
            row_str = ''
            for j, v in enumerate(row):
                if j % 3 == 0:
                    row_str += '|' if j == 0 else ' |'
                row_str += ' ' + str(v)
            row_str += ' |'
            print(row_str)
        print_row_separator()


def remove_from_index(index, indexes):
    row = int(index/9)
    col = index % 9
    indexes = [i for i in indexes if i not in list(range(row, row+9))]
    indexes = [i for i in indexes if i not in list(range(col, 9*9, 9))]
    sq_indexes = []
    for i in range(row, row+3):
        for j in range(int(col/3), int(col/3)+3):
            sq_indexes.append(j+9*i)
    indexes = [i for i in indexes if i not in sq_indexes]
    return indexes


def check_index(index, board):
    total = 0
    row = int(index/9)
    col = index % 9
    unique_row = set()
    unique_col = set()
    [unique_row.add(j) for j in board.get_row(row)]
    [unique_col.add(j) for j in board.get_col(col)]
    total += 9 - len(unique_row)
    total += 9 - len(unique_col)
    unique_sq = set()
    [unique_sq.add(j) for j in board.get_sq(int(row/3)*3, int(col/3)*3)]
    total += 9 - len(unique_sq)
    if total == 0:
        return True
    else:
        return False


def mutate(genes, indexes):
    board = SudokuBoard(genes)

    idxs = indexes
    indexA, indexB = idxs[0], idxs[0]
    while(genes[indexA] == genes[indexB]):
        if check_index(indexA, board):
            idxs = remove_from_index(indexA, idxs)
        #if check_index(indexB, board):
        #    idxs = remove_from_index(indexB, idxs)
        indexA, indexB = random.sample(idxs, 2)
    genes[indexA], genes[indexB] = genes[indexB], genes[indexA]


class Fitness:
    def __init__(self, total):
        self.Total = total

    def __gt__(self, other):
        return self.Total < other.Total

    def __str__(self):
        return "{}".format(self.Total)


class mySudokuTests(unittest.TestCase):
    def test(self):
        geneset = [j for i in range(1, 10) for j in range(1, 10)]
        startTime = datetime.datetime.now()

        def fnDisplay(candidate):
            display(candidate, startTime)

        def fnGenFitness(genes):
            return get_fitness(genes)

        geneIndexes = [i for i in range(0, len(geneset))]

        def fnMutate(genes):
            mutate(genes, geneIndexes)

        optimalFitness = Fitness(0)
        best = genetic.get_best(fnGenFitness, 9*9, optimalFitness, geneset,
                                fnDisplay, fnMutate, maxAge=1000)
        self.assertTrue(not optimalFitness > best.Fitness)

    def test_benchmark(self):
        genetic.Benchmark.run(self.test)


if __name__ == '__main__':
    unittest.main()
