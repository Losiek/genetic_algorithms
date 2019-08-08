import unittest
import datetime
import sys
import random

import genetic

def get_fitness(genes):
    totalWeight = 0
    totalVolume = 0
    totalValue = 0
    for iq in genes:
        count = iq.Quantity
        totalWeight += iq.Item.Weight * count
        totalVolume += iq.Item.Volume * count
        totalValue += iq.Item.Value * count

    return Fitness(totalWeight, totalVolume, totalValue)


def max_quantity(item, maxWeight, maxVolume):
    return min(int(maxWeight / item.Weight)
            if item.Weight > 0 else sys.maxsize,
            int(maxVolume / item.Volume)
            if item.Volume > 0 else sys.maxsize)


def add(genes, items, maxWeight, maxVolume):
    usedItems = {iq.Item for iq in genes}
    item = random.choice(items)
    while item in usedItems:
        item = random.choice(items)

    maxQuantity = max_quantity(item, maxWeight, maxVolume)
    return ItemQuantity(item, maxQuantity) if maxQuantity > 0 else None

def create(items, maxWeight, maxVolume):
    genes = []
    remainingWeight, remainingVolume = maxWeight, maxVolume
    for i in range(random.randrange(1, len(items))):
        newGene = add(genes, items, remainingWeight, remainingVolume)
        if newGene is not None:
            genes.append(newGene)
            remainingWeight -= newGene.Quantity * newGene.Item.Weight
            remainingVolume -= newGene.Quantity * newGene.Item.Volume

    return genes


def mutate(genes, items, maxWeight, maxVolume):
    fitness = get_fitness(genes)
    remainingWeight = maxWeight - fitness.TotalWeight
    remainingVolume = maxVolume - fitness.TotalVolume

    removing = len(genes) > 1 and random.randint(0, 10) == 0
    if removing:
        index = random.randrange(0, len(genes))
        iq = genes[index]
        item = iq.Item
        remainingWeight += item.Weight * iq.Quantity
        remainingVolume += item.Volume * iq.Quantity
        del genes[index]

    adding = (remainingWeight > 0 or remainingVolume > 0) and \
             (len(genes) == 0 or \
             (len(genes) < len(items) and random.randint(0, 100) == 0))
    if adding:
        newGene = add(genes, items, remainingWeight, remainingVolume)
        if newGene is not None:
            genes.append(newGene)
            return

    index = random.randrange(0, len(genes))
    iq = genes[index]
    item = iq.Item
    remainingWeight += item.Weight * iq.Quantity
    remainingVolume += item.Volume * iq.Quantity

    changeItem = len(genes) < len(items) and random.randint(0, 4) == 0
    if changeItem:
        itema, itemb = random.sample(items, 2)
        item = itema if itema != item else itemb

    maxQuantity = max_quantity(item, remainingWeight, remainingVolume)
    if maxQuantity > 0:
        quantity = random.randint(1, maxQuantity)
        genes[index] = ItemQuantity(item, quantity)
    else:
        del genes[index]

def display(candidate, startTime):
    timeDiff = datetime.datetime.now() - startTime
    genes = candidate.Genes[:]
    genes.sort(key=lambda iq: iq.Quantity, reverse=True)

    descriptions = [str(iq.Quantity) + "x" + iq.Item.Name for iq in genes]
    if len(descriptions) == 0:
        descriptions.append("Empty")
    print("{}\t{}\t{}".format(
        ', '.join(descriptions),
        candidate.Fitness,
        timeDiff))

class Resource:
    def __init__(self, name, value, weight, volume):
        self.Name = name
        self.Value = value
        self.Weight = weight
        self.Volume = volume


class ItemQuantity:
    def __init__(self, item, quantity):
        self.Item = item
        self.Quantity = quantity

    def __eq__(self, other):
        return self.Item == other.Item and self.Quantity == other.Quantity


class Fitness:
    def __init__(self, totalWeight, totalVolume, totalValue):
        self.TotalWeight = totalWeight
        self.TotalVolume = totalVolume
        self.TotalValue = totalValue

    def __gt__(self, other):
        if self.TotalValue != other.TotalValue:
            return self.TotalValue > other.TotalValue
        if self.TotalWeight != other.TotalWeight:
            return self.TotalWeight < other.TotalWeight
        return self.TotalVolume < self.TotalVolume

    def __str__(self):
        return "wt: {:0.2f} vol: {:0.2f} value: {}".format(
                self.TotalWeight,
                self.TotalVolume,
                self.TotalValue)


class KnapsackTests(unittest.TestCase):
    def test_cookies(self):
        items = [
                Resource("Flour", 1680, 0.265, .41),
                Resource("Butter", 1440, 0.5, .13),
                Resource("Sugar", 1840, 0.441, .29)
            ]
        maxWeight = 10
        maxVolume = 4
        optimal = get_fitness([ItemQuantity(items[0], 1),
                               ItemQuantity(items[1], 14),
                               ItemQuantity(items[2], 6)])
        self.fill_knapsack(items, maxWeight, maxVolume, optimal)

    def fill_knapsack(self, items, maxWeight, maxVolume, optimalFitness):
        startTime = datetime.datetime.now()

        def fnDisplay(candidate):
            display(candidate, startTime)

        def fnGetFitness(genes):
            return get_fitness(genes)

        def fnCreate():
            return create(items, maxWeight, maxVolume)

        def fnMutate(genes):
            mutate(genes, items, maxWeight, maxVolume)

        best = genetic.get_best(fnGetFitness, None, optimalFitness, None,
                                fnDisplay, fnMutate, fnCreate, maxAge=50)
        self.assertTrue(not optimalFitness > best.Fitness)


if __name__ == '__main__':
    unittest.main()
