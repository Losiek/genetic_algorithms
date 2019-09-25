# Traveling Salesman Problem
import unittest
import datetime
import math
import random

import genetic


def get_distance(locationA, locationB):
    sideA = locationA[0] - locationB[0]
    sideB = locationA[1] - locationB[1]
    sideC = math.sqrt(sideA * sideA + sideB * sideB)
    return sideC


def get_fitness(genes, idToLocationLookup):
    fitness = get_distance(idToLocationLookup[genes[0]],
                           idToLocationLookup[genes[-1]])

    for i in range(len(genes) - 1):
        start = idToLocationLookup[genes[i]]
        end = idToLocationLookup[genes[i + 1]]
        fitness += get_distance(start, end)

    return Fitness(round(fitness, 2))


def display(candidate, startTime):
    timeDiff = datetime.datetime.now() - startTime
    print("{}\t{}\t{}".format(
        ' '.join(map(str, candidate.Genes)),
        candidate.Fitness,
        timeDiff))


def mutate(genes, fnGetFitness):
    count = random.randint(2, len(genes))
    initialFitness = fnGetFitness(genes)
    while count > 0:
        count -= 1
        indexA, indexB = random.sample(range(len(genes)), 2)
        genes[indexA], genes[indexB] = genes[indexB], genes[indexA]
        fitness = fnGetFitness(genes)
        if fitness > initialFitness:
            return


def load_data(localFileName):
    """ expects:
    HEADER section before DATA section, all lines start in column 0
    DATA section elment all have space in column 0
        <space>1 23.45 67.89
    last line fo file is: " EOF"
    """
    with open(localFileName, mode='r') as infile:
        content = infile.read().splitlines()
    idToLocationLookup = {}
    for row in content:
        if row[0] != ' ':  # HEADERS
            continue
        if row == " EOF":
            break

        id, x, y = row.split(' ')[1:4]
        idToLocationLookup[int(id)] = [float(x), float(y)]
    return idToLocationLookup


class Fitness:
    def __init__(self, totalDistance):
        self.TotalDistance = totalDistance

    def __gt__(self, other):
        return self.TotalDistance < other.TotalDistance

    def __str__(self):
        return "{:0.2f}".format(self.TotalDistance)


class TravelingSalesmanTests(unittest.TestCase):
    def test_8_queens(self):
        idToLocationLookup = {
                # id:  x, y (0, 0) - bottom left
                'A': [4, 7],
                'B': [2, 6],
                'C': [0, 5],
                'D': [1, 3],
                'E': [3, 0],
                'F': [5, 1],
                'G': [7, 2],
                'H': [6, 4]
                }
        optimalSequence = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        self.solve(idToLocationLookup, optimalSequence)

    def test_ulysses16(self):
        idToLocationLookup = load_data("ulysses16.tsp")
        optimalSequence = [14, 13, 12, 16, 1, 3, 2, 4,
                           8, 15, 5, 11, 9, 10, 7, 6]
        self.solve(idToLocationLookup, optimalSequence)

    def solve(self, idToLocationLookup, optimalSequence):
        geneset = [i for i in idToLocationLookup.keys()]

        def fnCreate():
            return random.sample(geneset, len(geneset))

        def fnDisplay(candidate):
            display(candidate, startTime)

        def fnGetFitness(genes):
            return get_fitness(genes, idToLocationLookup)

        def fnMutate(genes):
            mutate(genes, fnGetFitness)

        optimalFitness = fnGetFitness(optimalSequence)
        startTime = datetime.datetime.now()
        best = genetic.get_best(fnGetFitness, None, optimalFitness, None,
                                fnDisplay, fnMutate, fnCreate, maxAge=500,
                                poolSize=25)
        self.assertTrue(not optimalFitness > best.Fitness)


if __name__ == '__main__':
    unittest.main()
