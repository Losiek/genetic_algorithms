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
        totalWeight += iq.Weight * count
        totalVolume += iq.Volume * count
        totalValue += iq.Value * count

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
        index = randrange(0, len(genes))
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


class Resource:
    def __init__(self, name, value, weight, volume):
        self.Name = name
        self.Value = value
        self.Weight = weight
        self.Volume = volume


class KnapsackTests(unittest.TestCase):
    def test_cookies(self):
        items = [
                Resource("Flour", 1680, 0.265, .41),
                Resource("Butter", 1440, 0.5, .13),
                Resource("Sugar", 1840, 0.441, .29)
            ]


class ItemQuantity:
    def __init__(self, item, quantity):
        self.Item = items
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
            return self.TotalValue > other.totalValue
        if self.TotalWeight != other.TotalWeight:
            return self.TotalWeight < other.TotalWeight
        return self.TotalVolume < self.TotalVolume

    def __str__(self):
        return "wt: {:0.2f} vol: {:0.2f} value: {}".format(
                self.TotalWeight,
                self.TotalVolume,
                self.TotalValue)
