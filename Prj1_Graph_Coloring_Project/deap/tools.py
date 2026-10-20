import copy
import random


def initRepeat(container, func, n):
    return container(func() for _ in range(n))


def cxTwoPoint(ind1, ind2):
    size = min(len(ind1), len(ind2))
    if size < 2:
        return ind1, ind2
    cxpoint1 = random.randint(1, size - 1)
    cxpoint2 = random.randint(1, size - 1)
    if cxpoint2 < cxpoint1:
        cxpoint1, cxpoint2 = cxpoint2, cxpoint1
    if cxpoint1 == cxpoint2:
        cxpoint2 = min(size, cxpoint1 + 1)
    ind1[cxpoint1:cxpoint2], ind2[cxpoint1:cxpoint2] = ind2[cxpoint1:cxpoint2], ind1[cxpoint1:cxpoint2]
    return ind1, ind2


def mutFlipBit(individual, indpb):
    for i in range(len(individual)):
        if random.random() < indpb:
            individual[i] = 0 if individual[i] else 1
    return (individual,)


def _fitness_value(individual):
    values = getattr(individual.fitness, "values", ())
    return values[0] if values else float("-inf")


def selTournament(individuals, k, tournsize, fit_attr="fitness"):
    selected = []
    for _ in range(k):
        aspirants = [random.choice(individuals) for _ in range(tournsize)]
        selected.append(max(aspirants, key=_fitness_value))
    return selected


class HallOfFame:
    def __init__(self, maxsize):
        self.maxsize = maxsize
        self.items = []

    def update(self, population):
        candidates = list(self.items) + [copy.deepcopy(ind) for ind in population]
        candidates.sort(key=_fitness_value, reverse=True)
        self.items = candidates[: self.maxsize]

    def __getitem__(self, index):
        return self.items[index]

    def __len__(self):
        return len(self.items)
