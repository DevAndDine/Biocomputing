import random


def _evaluate_population(population, toolbox):
    for individual in population:
        individual.fitness.values = toolbox.evaluate(individual)


def eaSimple(population, toolbox, cxpb, mutpb, ngen, halloffame=None, verbose=False):
    _evaluate_population(population, toolbox)
    if halloffame is not None:
        halloffame.update(population)

    for _ in range(ngen):
        offspring = [toolbox.clone(ind) for ind in toolbox.select(population, len(population))]

        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < cxpb:
                toolbox.mate(child1, child2)

        for mutant in offspring:
            if random.random() < mutpb:
                toolbox.mutate(mutant)

        _evaluate_population(offspring, toolbox)
        population[:] = offspring

        if halloffame is not None:
            halloffame.update(population)

    return population, []
