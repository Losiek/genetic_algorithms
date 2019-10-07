# Circuit Tests
import unittest
import datetime
import random

import genetic
import circuits


class Node:
    def __init__(self, createGate, indexA=None, indexB=None):
        self.CreateGate = createGate
        self.IndexA = indexA
        self.IndexB = indexB


def nodes_to_circuit(nodes):
    circuit = []
    usedIndexes = []
    for i, node in enumerate(nodes):
        used = {i}
        inputA = inputB = None
        if node.IndexA is not None and i > node.IndexA:
            inputA = circuit[node.IndexA]
            used.update(usedIndexes[node.IndexA])
            if node.IndexB is not None and i > node.IndexB:
                inputB = circuit[node.IndexB]
                used.update(usedIndexes[node.IndexB])
        circuit.append(node.CreateGate(inputA, inputB))
        usedIndexes.append(used)
    return circuit[-1], usedIndexes[-1]


def get_fitness(genes, rules, inputs):
    circuit = nodes_to_circuit(genes)[0]
    sourceLabels = "AB"
    rulesPassed = 0
    for rule in rules:
        inputs.clear()
        inputs.update(zip(sourceLabels, rule[0]))
        if circuit.get_output() == rule[1]:
            rulesPassed += 1
    return rulesPassed


def display(candidate, startTime):
    circuit = nodes_to_circuit(candidate.Genes)[0]
    timeDiff = datetime.datetime.now() - startTime
    print("{}\t{}\t{}".format(
        circuit,
        candidate.Fitness,
        timeDiff))


def create_gene(index, geneset):
    gateType = random.choice(geneset)
    indexA = indexB = None
    if gateType[1].input_count() > 0:
        indexA = random.randint(0, index)
    if gateType[1].input_count() > 1:
        indexB = random.randint(0, index) if index > 1 else 0
        if indexB == indexA:
            indexB = random.randint(0, index)
    return Node(gateType[0], indexA, indexB)


def mutate(childGenes, fnCreateGene):
    count = random.randint(1, 5)
    while count > 0:
        count -= 1
        indexesUsed = [i for i in nodes_to_circuit(childGenes)[1]]
        index = random.choice(indexesUsed)
        childGenes[index] = fnCreateGene(index)


class CircuitTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.inputs = dict()
        cls.geneset = [[circuits.And, circuits.And],
                       [lambda i1, i2: circuits.Not(i1), circuits.Not],
                       [lambda i1, i2: circuits.Source('A', cls.inputs), circuits.Source],
                       [lambda i1, i2: circuits.Source('B', cls.inputs), circuits.Source]]

    def test_generate_OR(self):
        rules = [[[False, False], False],
                 [[False, True], True],
                 [[True, False], True],
                 [[True, True], True]]

        optimalLenght = 6
        self.find_circuit(rules, optimalLenght)


    def test_generate_XOR(self):
        rules = [[[False, False], False],
                 [[False, True], True],
                 [[True, False], True],
                 [[True, True], False]]

        optimalLenght = 9
        self.find_circuit(rules, optimalLenght)


    def find_circuit(self, rules, expectedLength):
        startTime = datetime.datetime.now()
        maxLength = expectedLength

        def fnCreate():
            return [fnCreateGene(i) for i in range(maxLength)]

        def fnDisplay(candidate):
            display(candidate, startTime)

        def fnCreateGene(index):
            return create_gene(index, self.geneset)

        def fnMutate(genes):
            mutate(genes, fnCreateGene)

        def fnGetFitness(genes):
            return get_fitness(genes, rules, self.inputs)

        best = genetic.get_best(fnGetFitness, None, len(rules), None, fnDisplay,
                                fnMutate, fnCreate, poolSize=3)
        self.assertTrue(best.Fitness == len(rules))
        self.assertTrue(not len(nodes_to_circuit(best.Genes)[1]) > expectedLength)


if __name__ == '__main__':
    unittest.main()
