import unittest
import datetime
import fractions

import genetic


def get_fitness(genes, equations):
    fitness = Fitness(sum(abs(e(genes)) for e in equations))
    return fitness


def display(candidate, startTime, fnGenesToInputs):
    timeDiff = datetime.datetime.now() - startTime
    symbols = "xyz"
    result = ", ".join(
        "{} = {}".format(s, v)
        for s, v in zip(symbols, fnGenesToInputs(candidate.Genes))
    )
    print("{}\t{}\t{}".format(result, candidate.Fitness, timeDiff))


class Fitness:
    def __init__(self, totalDiffrence):
        self.TotalDiffrence = totalDiffrence

    def __gt__(self, other):
        return self.TotalDiffrence < other.TotalDiffrence

    def __str__(self):
        return "diff: {:0.2f}".format(float(self.TotalDiffrence))


class LinearEquationTests(unittest.TestCase):
    def solve_unknowns(self, numUnknows, geneset, equations, fnGenesToInputs):
        startTime = datetime.datetime.now()

        def fnDisplay(candidate):
            display(candidate, startTime, fnGenesToInputs)

        def fnGetFitness(genes):
            return get_fitness(genes, equations)

        optimalFitness = Fitness(0)
        best = genetic.get_best(
            fnGetFitness,
            numUnknows,
            optimalFitness,
            geneset,
            fnDisplay,
            maxAge=50,
        )
        self.assertTrue(not optimalFitness > best.Fitness)

    def test_2_unknowns(self):
        geneset = [i for i in range(-5, 5) if i != 0]

        def fnGenesToInputs(genes):
            return genes[0], genes[1]

        def e1(genes):
            x, y = fnGenesToInputs(genes)
            return x + 2 * y - 4

        def e2(genes):
            x, y = fnGenesToInputs(genes)
            return 4 * x + 4 * y - 12

        equations = [e1, e2]
        self.solve_unknowns(2, geneset, equations, fnGenesToInputs)

    def test_3_unknowns(self):
        geneset = [i for i in range(-5, 5) if i != 0]

        def fnGenesToInputs(genes):
            return [
                fractions.Fraction(genes[i], genes[i + 1])
                for i in range(0, len(genes), 2)
            ]

        def e1(genes):
            x, y, z = fnGenesToInputs(genes)
            return 6 * x - 2 * y + 8 * z - 20

        def e2(genes):
            x, y, z = fnGenesToInputs(genes)
            return y + 8 * x * z + 1

        def e3(genes):
            x, y, z = fnGenesToInputs(genes)
            return (
                2 * z * fractions.Fraction(6, x)
                + 3 * fractions.Fraction(y, 2)
                - 6
            )

        equations = [e1, e2, e3]
        self.solve_unknowns(6, geneset, equations, fnGenesToInputs)


if __name__ == "__main__":
    unittest.main()
