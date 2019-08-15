import unittest
import datetime
import genetic


def get_fitness(genes):
    x, y = genes[0:2]

    e1 = x + 2 * y - 4
    e2 = 4 * x + 4 * y - 12
    fitness = Fitness(abs(e1) + abs(e2))

    return fitness


def display(candidate, startTime):
    timeDiff = datetime.datetime.now() - startTime
    x, y = candidate.Genes[0:2]
    print("x = {}, y = {}\t{}\t{}".format(
        x, y, candidate.Fitness, timeDiff))


class Fitness:
    def __init__(self, totalDiffrence):
        self.TotalDiffrence = totalDiffrence

    def __gt__(self, other):
        return self.TotalDiffrence < other.TotalDiffrence

    def __str__(self):
        return "diff: {:0.2f}".format(float(self.TotalDiffrence))


class LinearEquationTests(unittest.TestCase):
    def test(self):
        geneset = [i for i in range(10)]
        startTime = datetime.datetime.now()

        def fnDisplay(candidate):
            display(candidate, startTime)

        def fnGetFitness(genes):
            return get_fitness(genes)

        optimalFitness = Fitness(0)
        best = genetic.get_best(fnGetFitness, 2, optimalFitness,
                                geneset, fnDisplay, maxAge=50)
        self.assertTrue(not optimalFitness > best.Fitness)


if __name__ == "__main__":
    unittest.main()
