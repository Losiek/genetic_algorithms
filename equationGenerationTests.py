# Equation Generation Test
import unittest
import datetime
import genetic
import random


def evaluate(genes, prioritizedOperations):
    equation = genes[:]
    for operationSet in prioritizedOperations:
        iOffset = 0
        for i in range(1, len(equation), 2):
            i += iOffset
            opToken = equation[i]
            if opToken in operationSet:
                leftOperand = equation[i - 1]
                rightOperand = equation[i + 1]

                if opToken == '+':
                    leftOperand += rightOperand
                elif opToken == '-':
                    leftOperand -= rightOperand
                elif opToken == '*':
                    leftOperand *= rightOperand
                equation[i - 1] = leftOperand
                del equation[i + 1]
                del equation[i]
                iOffset -= 2
    return equation[0]


def create(numbers, operations, minNumbers, maxNumbers):
    genes = [random.choice(numbers)]
    count = random.randint(minNumbers, 1 + maxNumbers)
    while count > 1:
        count -= 1
        genes.append(random.choice(operations))
        genes.append(random.choice(numbers))
    return genes


def mutate(genes, numbers, operations, minNumbers, maxNumbers):
    numberCount = (1 + len(genes)) / 2
    appending = numberCount < maxNumbers and \
                random.randint(0, 100) == 0
    if appending:
        genes.append(random.choice(operations))
        genes.append(random.choice(numbers))
        return
    # Remove operation-number pair
    removing = numberCount > minNumbers and \
               random.randint(0, 20) == 0
    if removing:
        index = random.randrange(0, len(genes) - 1)
        del genes[index]
        del genes[index]
        return
    # And mutate an operation or number
    index = random.randrange(0, len(genes))
    genes[index] = random.choice(operations) \
            if (index & 1) == 1 else random.choice(numbers)


def display(candidate, startTime):
    timeDiff = datetime.datetime.now() - startTime
    print("{}\t{}\t{}".format(
        (' '.join(map(str, [i for i in candidate.Genes]))),
        candidate.Fitness,
        timeDiff))


def get_fitness(genes, expectedTotal, fnEvaluate):
    result = fnEvaluate(genes)

    if result != expectedTotal:
        fitness = expectedTotal - abs(result - expectedTotal)
    else:
        fitness = 1000 - len(genes)

    return fitness


class EquationGenerationTest(unittest.TestCase):
    def test_addition(self):
        operations = ['+', '-']
        prioritizedOperations = [['+', '-']]
        optimalLengthSolution = [7, '+', 7, '+', 7, '+', 7, '+', 7, '-', 6]
        self.solve(operations, prioritizedOperations, optimalLengthSolution)

    def solve(self, operations, prioritizedOperations, optimalLengthSolution):
        numbers = [1, 2, 3, 4, 5, 6, 7]
        expectedTotal = evaluate(optimalLengthSolution, prioritizedOperations)
        minNumbers = (1 + len(optimalLengthSolution)) / 2
        maxNumbers = 6 * minNumbers
        startTime = datetime.datetime.now()

        def fnEvaluate(genes):
            return evaluate(genes, prioritizedOperations)

        def fnDisplay(candidate):
            display(candidate, startTime)

        def fnGetFitness(genes):
            return get_fitness(genes, expectedTotal, fnEvaluate)

        def fnCreate():
            return create(numbers, operations, minNumbers, maxNumbers)

        def fnMutate(child):
            mutate(child, numbers, operations, minNumbers, maxNumbers)

        optimalFitness = fnGetFitness(optimalLengthSolution)
        best = genetic.get_best(fnGetFitness, None, optimalFitness, None,
                                fnDisplay, fnMutate, fnCreate, maxAge=50)
        self.assertTrue(not optimalFitness > best.Fitness)

    def test_multiplication(self):
        operations = ['+', '-', '*']
        prioritizedOperations = [['*'], ['+', '-']]
        optimalLengthSolution = [6, '*', 3, '*', 3, '*', 6, '-', 7]
        self.solve(operations, prioritizedOperations, optimalLengthSolution)


if __name__ == '__main__':
    unittest.main()