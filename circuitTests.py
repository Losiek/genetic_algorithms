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
    sourceLabels = "ABCD"
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
    print("{}\t{}\t{}".format(circuit, candidate.Fitness, timeDiff))


def create_gene(index, gates, sources):
    if index < len(sources):
        gateType = sources[index]
    else:
        gateType = random.choice(gates)
    indexA = indexB = None
    if gateType[1].input_count() > 0:
        indexA = random.randint(0, index)
    if gateType[1].input_count() > 1:
        indexB = (
            random.randint(0, index)
            if index > 1 and index >= len(sources)
            else 0
        )
        if indexB == indexA:
            indexB = random.randint(0, index)
    return Node(gateType[0], indexA, indexB)


def mutate(childGenes, fnCreateGene, fnGetFitness, sourceCount):
    count = random.randint(1, 5)
    initialFitness = fnGetFitness(childGenes)
    while count > 0:
        count -= 1
        indexesUsed = [
            i for i in nodes_to_circuit(childGenes)[1] if i >= sourceCount
        ]
        if len(indexesUsed) == 0:
            return
        index = random.choice(indexesUsed)
        childGenes[index] = fnCreateGene(index)
        if fnGetFitness(childGenes) > initialFitness:
            return


class CircuitTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.inputs = dict()
        cls.gates = [
            [circuits.And, circuits.And],
            [lambda i1, i2: circuits.Not(i1), circuits.Not],
        ]
        cls.sources = [
            [lambda i1, i2: circuits.Source("A", cls.inputs), circuits.Source],
            [lambda i1, i2: circuits.Source("B", cls.inputs), circuits.Source],
        ]

    def test_generate_OR(self):
        rules = [
            [[False, False], False],
            [[False, True], True],
            [[True, False], True],
            [[True, True], True],
        ]

        optimalLenght = 6
        self.find_circuit(rules, optimalLenght)

    def test_generate_XOR(self):
        rules = [
            [[False, False], False],
            [[False, True], True],
            [[True, False], True],
            [[True, True], False],
        ]

        optimalLenght = 9
        self.find_circuit(rules, optimalLenght)

    def test_generate_AxBxC(self):
        rules = [
            [[False, False, False], False],
            [[False, False, True], True],
            [[False, True, False], True],
            [[False, True, True], False],
            [[True, False, False], True],
            [[True, False, True], False],
            [[True, True, False], False],
            [[True, True, True], True],
        ]
        self.sources.append(
            [lambda l, r: circuits.Source("C", self.inputs), circuits.Source]
        )
        self.gates.append([circuits.Or, circuits.Or])
        self.find_circuit(rules, 12)

    def test_2_bit_adder_1s_bit(self):
        rules = self.get_2_bit_adder_rules_for_bit(0)
        self.find_circuit(rules, 3)

    def test_2_bit_adder_2s_bit(self):
        rules = self.get_2_bit_adder_rules_for_bit(1)
        self.find_circuit(rules, 7)

    def test_2_bit_adder_4s_bit(self):
        rules = self.get_2_bit_adder_rules_for_bit(2)
        self.find_circuit(rules, 9)

    def get_2_bit_adder_rules_for_bit(self, bit):
        rules = [
            [[False, False, False, False], [False, False, False]],  # 0 + 0 = 0
            [[False, False, False, True], [False, False, True]],  # 0 + 1 = 1
            [[False, False, True, False], [False, True, False]],  # 0 + 2 = 2
            [[False, False, True, True], [False, True, True]],  # 0 + 3 = 3
            [[False, True, False, False], [False, False, True]],  # 1 + 0 = 1
            [[False, True, False, True], [False, True, False]],  # 1 + 1 = 2
            [[False, True, True, False], [False, True, True]],  # 1 + 2 = 3
            [[False, True, True, True], [True, False, False]],  # 1 + 3 = 4
            [[True, False, False, False], [False, True, False]],  # 2 + 0 = 2
            [[True, False, False, True], [False, True, True]],  # 2 + 1 = 3
            [[True, False, True, False], [True, False, False]],  # 2 + 2 = 4
            [[True, False, True, True], [True, False, True]],  # 2 + 3 = 5
            [[True, True, False, False], [False, True, True]],  # 3 + 0 = 3
            [[True, True, False, True], [True, False, False]],  # 3 + 1 = 4
            [[True, True, True, False], [True, False, True]],  # 3 + 2 = 5
            [[True, True, True, True], [True, True, False]],
        ]  # 3 + 3 = 6
        bitNRules = [[rule[0], rule[1][2 - bit]] for rule in rules]

        self.gates.append([circuits.Or, circuits.Or])
        self.gates.append([circuits.Xor, circuits.Xor])
        self.sources.append(
            [lambda l, r: circuits.Source("C", self.inputs), circuits.Source]
        )
        self.sources.append(
            [lambda l, r: circuits.Source("D", self.inputs), circuits.Source]
        )
        return bitNRules

    def find_circuit(self, rules, expectedLength):
        startTime = datetime.datetime.now()
        maxLength = 50

        def fnCreate():
            return [fnCreateGene(i) for i in range(maxLength)]

        def fnDisplay(candidate, length=None):
            if length is not None:
                print(
                    "-- distinct nodes in circuit:",
                    len(nodes_to_circuit(candidate.Genes)[1]),
                )
            display(candidate, startTime)

        def fnCreateGene(index):
            return create_gene(index, self.gates, self.sources)

        def fnMutate(genes):
            mutate(genes, fnCreateGene, fnGetFitness, len(self.sources))

        def fnGetFitness(genes):
            return get_fitness(genes, rules, self.inputs)

        def fnOptimizationFunction(variableLength):
            nonlocal maxLength
            maxLength = variableLength
            return genetic.get_best(
                fnGetFitness,
                None,
                len(rules),
                None,
                fnDisplay,
                fnMutate,
                fnCreate,
                poolSize=3,
                maxSeconds=15,
            )

        def fnIsImprovement(currentBest, child):
            return child.Fitness == len(rules) and len(
                nodes_to_circuit(child.Genes)[1]
            ) < len(nodes_to_circuit(currentBest.Genes)[1])

        def fnIsOptimal(child):
            return (
                child.Fitness == len(rules)
                and len(nodes_to_circuit(child.Genes)[1]) <= expectedLength
            )

        def fnGetNextFeatureValue(currentBest):
            return len(nodes_to_circuit(currentBest.Genes)[1])

        best = genetic.hill_climbing(
            fnOptimizationFunction,
            fnIsImprovement,
            fnIsOptimal,
            fnGetNextFeatureValue,
            fnDisplay,
            maxLength,
        )

        self.assertTrue(best.Fitness == len(rules))
        self.assertTrue(
            not len(nodes_to_circuit(best.Genes)[1]) > expectedLength
        )


if __name__ == "__main__":
    unittest.main()
