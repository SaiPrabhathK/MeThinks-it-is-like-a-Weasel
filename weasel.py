#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Assignment 01:

READ:
https://en.wikipedia.org/wiki/Weasel_program
http://rationalwiki.org/wiki/Dawkins_weasel

In the way I've engineerd this program,
we'll use a powerful general purpose chainsaw,
to accomplish the special-purose task of mowing the lawn...

This program uses:
* a full population of randomly initialized strings
* recombination
* mutation
* parent selection
* survivor selection
* fitness evalution
* etc.
While all that is overkill for this particular problem,
it does serve to illustrate the framework we will build onu
"""

# TODO unit tests (copy doc)
# TODO std tests
# TODO arg tests (with json output)

# %%
import sys
import string
import random
from typing import TypedDict


class Individual(TypedDict):
    genome: str
    fitness: int


Population = list[Individual]


def initialize_individual(genome: str, fitness: int) -> Individual:
    """
    Purpose:        Create one individual
    Parameters:     genome as string, fitness as integer (higher better)
    User Input:     no
    Prints:         no
    Returns:        One Individual, as a dict[str, int]
    Modifies:       Nothing
    Calls:          Basic python only
    Tests:          ./unit_tests/*
    Status:         Do this one!
    Example doctest:
    >>> initialize_individual("EC is fun", 10)
    {'genome': 'EC is fun', 'fitness': 10}
    >>> initialize_individual("Fun is EC", 9)
    {'genome': 'Fun is EC', 'fitness': 9}
    """
    return Individual({"genome": genome, "fitness": fitness})


def initialize_pop(objective: str, pop_size: int) -> Population:
    """
    Purpose:        Create population to evolve
    Parameters:     Goal string, population size as int
    User Input:     no
    Prints:         no
    Returns:        a population, as a list of Individuals
    Modifies:       Nothing
    Calls:          random.choice, string.ascii_letters, initialize_individual
    Tests:          ./unit_tests/*
    Status:         Do this one!
    Example doctest:
    >>> import random
    >>> random.seed(42)
    >>> for _ in range(4):
    ...     initialize_pop("EC is easy", 2)
    [{'genome': 'OhbVrpoiVg', 'fitness': 0}, {'genome': 'RVIfLBcbfn', 'fitness': 0}]
    [{'genome': 'oGMbJmTPSI', 'fitness': 0}, {'genome': 'AoCLrZaWZk', 'fitness': 0}]
    [{'genome': 'SBvrjnWvgf', 'fitness': 0}, {'genome': 'ygwwMqZcUD', 'fitness': 0}]
    [{'genome': 'IhyfJsONxK', 'fitness': 0}, {'genome': 'mTecQoXsfo', 'fitness': 0}]
    """
    population = []
    for i in range(pop_size):
        new_genome = ""
        for i in range(len(objective)):
            new_genome = new_genome + random.choice(string.ascii_letters + " ")
        new_individual = initialize_individual(new_genome, 0)
        # print(new_individual)
        population.append(new_individual)
    # print(population)
    return population
    # print('Delete this and write your code')


def recombine_pair(parent1: Individual, parent2: Individual) -> Population:
    """
    Purpose:        Recombine two parents to produce two children
    Parameters:     Two parents as Individuals
    User Input:     no
    Prints:         no
    Returns:        Two Individuals, as a TypedDict[str, int]
    Modifies:       Nothing
    Calls:          Basic python, random.choice, initialize_individual
    Tests:          ./unit_tests/*
    Status:         Do this one!
    Example doctest:
    >>> import random
    >>> random.seed(42)
    >>> i1 = initialize_individual("EC is great", 10)
    >>> i2 = initialize_individual("Great is EC", 10)
    >>> for _ in range(4):
    ...     recombine_pair(i1, i2)
    [{'genome': 'EC is greaC', 'fitness': 0}, {'genome': 'Great is Et', 'fitness': 0}]
    [{'genome': 'Ereat is EC', 'fitness': 0}, {'genome': 'GC is great', 'fitness': 0}]
    [{'genome': 'Great is EC', 'fitness': 0}, {'genome': 'EC is great', 'fitness': 0}]
    [{'genome': 'EC it is EC', 'fitness': 0}, {'genome': 'Greas great', 'fitness': 0}]
    """
    crossover_point = random.choice(range(len(parent1["genome"])))
    offspring1 = ""
    offspring2 = ""
    offspring1 += parent1["genome"][0:crossover_point]
    offspring2 += parent2["genome"][0:crossover_point]
    offspring1 += parent2["genome"][crossover_point:]
    offspring2 += parent1["genome"][crossover_point:]
    # for x in range(crossover_point):
    #  offspring1 += parent1['genome'][x]
    # offspring2 += parent2['genome'][x]

    # for y in range(crossover_point, len(parent1['genome'])):
    #  offspring1 += parent2['genome'][y]
    # offspring2 += parent1['genome'][y]

    # print(offspring1, offspring2)
    # print(initialize_individual(offspring1, 0))
    return list(
        (initialize_individual(offspring1, 0), initialize_individual(offspring2, 0))
    )
    # print('Delete this and write your code')


def recombine_group(parents: Population, recombine_rate: float) -> Population:
    """
    Purpose:        Recombines a whole group, returns the new population
    Parameters:     genome as string, fitness as integer (higher better)
    User Input:     no
    Prints:         no
    Returns:        New population of children
    Modifies:       Nothing
    Calls:          Basic python, recombine pair
    Tests:          ./unit_tests/*
    Status:         Do this one!
    Example doctest:
    >>> import random
    >>> random.seed(42)
    >>> i1 = initialize_individual("EC is great", 10)
    >>> i2 = initialize_individual("Great is EC", 10)
    >>> pop = [i1, i2]
    >>> for _ in range(4):
    ...     recombine_group(pop, 0.8)
    [{'genome': 'Great is EC', 'fitness': 0}, {'genome': 'EC is great', 'fitness': 0}]
    [{'genome': 'EC at is EC', 'fitness': 0}, {'genome': 'Greis great', 'fitness': 0}]
    [{'genome': 'Ereat is EC', 'fitness': 0}, {'genome': 'GC is great', 'fitness': 0}]
    [{'genome': 'EC is gr EC', 'fitness': 0}, {'genome': 'Great iseat', 'fitness': 0}]
    """
    recombined_population = []
    # print(parents)
    for i in range(0, len(parents) - 1, 2):

        if recombine_rate > random.random():
            recombined_population.extend(recombine_pair(parents[i], parents[i + 1]))
        else:
            recombined_population.append(parents[i])
            recombined_population.append(parents[i + 1])
    # print(recombined_population)
    return recombined_population
    # print('Delete this and write your code')


def mutate_individual(parent: Individual, mutate_rate: float) -> Individual:
    """
    Purpose:        Mutate one individual
    Parameters:     One parents as Individual, mutation rate as float (0-1)
    User Input:     no
    Prints:         no
    Returns:        One Individual, as a TypedDict[str, int]
    Modifies:       Nothing
    Calls:          Basic python, initialize_individual
    Tests:          ./unit_tests/*
    Status:         Do this one!
    Example doctest:
    >>> import random
    >>> random.seed(42)
    >>> ind = initialize_individual("EC is fun", 10)
    >>> for _ in range(4):
    ...     mutate_individual(ind, 0.3)
    {'genome': 'Eriis BfG', 'fitness': 0}
    {'genome': 'EC is auB', 'fitness': 0}
    {'genome': 'EW gs cun', 'fitness': 0}
    {'genome': 'EC is fuo', 'fitness': 0}
    """
    mutated_genome = ""
    for i in parent["genome"]:
        if random.random() < mutate_rate:
            mutated_genome += random.choice(string.ascii_letters + " ")
        else:
            mutated_genome += i
    # print(mutated_genome)
    return initialize_individual(mutated_genome, 0)


def mutate_group(children: Population, mutate_rate: float) -> Population:
    """
    Purpose:        Mutates a whole Population, returns the mutated group
    Parameters:     Population, mutation rate as float (0-1)
    User Input:     no
    Prints:         no
    Returns:        One Individual, as a TypedDict[str, int]
    Modifies:       Nothing
    Calls:          Basic python, mutate_individual
    Tests:          ./unit_tests/*
    Status:         Do this one!
    Example doctest:
    >>> import random
    >>> random.seed(42)
    >>> i1 = initialize_individual("EC is great", 10)
    >>> i2 = initialize_individual("Great is EC", 10)
    >>> pop = [i1, i2]
    >>> for _ in range(4):
    ...     mutate_group(pop, 0.3)
    [{'genome': 'Eriis BfGat', 'fitness': 0}, {'genome': 'Greaa BsWEg', 'fitness': 0}]
    [{'genome': 'ECcis great', 'fitness': 0}, {'genome': 'Groat is Ew', 'fitness': 0}]
    [{'genome': 'rC OUDgreat', 'fitness': 0}, {'genome': 'GrcatKis EC', 'fitness': 0}]
    [{'genome': 'Ep is greFd', 'fitness': 0}, {'genome': 'Gkeay iJ UI', 'fitness': 0}]
    """
    mutated_population = []
    for x in children:
        mutated_population.append(mutate_individual(x, mutate_rate))
    # print(mutated_population)
    return mutated_population


def evaluate_individual(objective: str, individual: Individual) -> None:
    """
    Purpose:        Computes and modifies the fitness for one individual
    Parameters:     Objective string, One Individual
    User Input:     no
    Prints:         no
    Returns:        None
    Modifies:       The individual (mutable object)
    Calls:          Basic python only
    Tests:          ./unit_tests/*
    Status:         Do this one!
    Example doctest:
    >>> i1 = initialize_individual("This assignment is hard!", 0)
    >>> i2 = initialize_individual("This assignment is good!", 0)
    >>> objective = "This assignment is easy!"
    >>> evaluate_individual(objective=objective, individual=i1)
    >>> evaluate_individual(objective=objective, individual=i2)
    >>> i1
    {'genome': 'This assignment is hard!', 'fitness': 21}
    >>> i2
    {'genome': 'This assignment is good!', 'fitness': 20}
    """
    matching_genes = 0
    for i in range(len(individual["genome"])):
        if individual["genome"][i] == objective[i]:
            matching_genes += 1
    individual["fitness"] = matching_genes
    # print(matching_genes)


def evaluate_group(objective: str, individuals: Population) -> None:
    """
    Purpose:        Computes and modifies the fitness for population
    Parameters:     Objective string, Population
    User Input:     no
    Prints:         no
    Returns:        None
    Modifies:       The Individuals, all mutable objects
    Calls:          Basic python, evaluate_individual
    Tests:          ./unit_tests/*
    Status:         Do this one!
    Example doctest:
    >>> import random
    >>> random.seed(42)
    >>> i1 = initialize_individual("This assignment is work!", 0)
    >>> i2 = initialize_individual("This assignment is hard!", 0)
    >>> objective = "This assignment is easy!"
    >>> pop = [i1, i2]
    >>> evaluate_group(objective=objective, individuals=pop)
    >>> pop[0]
    {'genome': 'This assignment is work!', 'fitness': 20}
    >>> pop[1]
    {'genome': 'This assignment is hard!', 'fitness': 21}
    """
    for x in individuals:
        evaluate_individual(objective, x)
        # print()


def rank_group(individuals: Population) -> None:
    """
    Purpose:        Create one individual
    Parameters:     Population of Individuals
    User Input:     no
    Prints:         no
    Returns:        None
    Modifies:       The population's order (a mutable object)
    Calls:          Basic python only
    Tests:          ./unit_tests/*
    Status:         Do this one!
    Example doctest:
    >>> import random
    >>> random.seed(42)
    >>> i1 = initialize_individual("Zhis glass it isabeesting!", 2)
    >>> i2 = initialize_individual("This class is motivating!!", 6)
    >>> objective = "This class is captivating!"
    >>> pop = [i1, i2]
    >>> rank_group(pop)
    >>> pop
    [{'genome': 'This class is motivating!!', 'fitness': 6}, {'genome': 'Zhis glass it isabeesting!', 'fitness': 2}]
    """
    ranked_individuals = []
    ranked_individuals = sorted(
        individuals, key=lambda individual: individual["fitness"], reverse=True
    )
    for x in range(len(ranked_individuals)):
        individuals[x] = ranked_individuals[x]
    # individuals
    # print(individuals)
    # return individuals


def parent_select(individuals: Population, number: int) -> Population:
    """
    Purpose:        Choose parents in direct probability to their fitness
    Parameters:     Population, the number of individuals to pick.
    User Input:     no
    Prints:         no
    Returns:        Sub-population
    Modifies:       Nothing
    Calls:          Basic python, random.choices (hint)
    Tests:          ./unit_tests/*
    Status:         Do this one!
    Example doctest:
    >>> import random
    >>> random.seed(42)
    >>> i1 = initialize_individual("gene", 5)
    >>> i2 = initialize_individual("meme", 6)
    >>> i3 = initialize_individual("heme", 4)
    >>> pop = [i1, i2, i3]
    >>> for _ in range(4):
    ...     parent_select(pop, 2)
    [{'genome': 'meme', 'fitness': 6}, {'genome': 'gene', 'fitness': 5}]
    [{'genome': 'gene', 'fitness': 5}, {'genome': 'gene', 'fitness': 5}]
    [{'genome': 'heme', 'fitness': 4}, {'genome': 'meme', 'fitness': 6}]
    [{'genome': 'heme', 'fitness': 4}, {'genome': 'gene', 'fitness': 5}]
    """
    fitness_list = []
    for x in individuals:
        fitness_list.append(x["fitness"])
    # print(random.choices(individuals, weights = fitness_list, k = number))
    selected_parents = random.choices(individuals, weights=fitness_list, k=number)
    # print("printing selected_parents")
    # print(selected_parents)
    return selected_parents


def survivor_select(individuals: Population, pop_size: int) -> Population:
    """
    Purpose:        Picks who gets to live!
    Parameters:     Population, and population size to return.
    User Input:     no
    Prints:         no
    Returns:        Population, of pop_size
    Modifies:       Nothing
    Calls:          Basic python only
    Tests:          ./unit_tests/*
    Status:         Do this one!
    Example doctest:
    >>> import random
    >>> random.seed(42)
    >>> i1 = initialize_individual("meme", 6)
    >>> i2 = initialize_individual("gene", 5)
    >>> i3 = initialize_individual("heme", 4)
    >>> pop = [i1, i2, i3]
    >>> for _ in range(4):
    ...     survivor_select(pop, 2)
    [{'genome': 'meme', 'fitness': 6}, {'genome': 'gene', 'fitness': 5}]
    [{'genome': 'meme', 'fitness': 6}, {'genome': 'gene', 'fitness': 5}]
    [{'genome': 'meme', 'fitness': 6}, {'genome': 'gene', 'fitness': 5}]
    [{'genome': 'meme', 'fitness': 6}, {'genome': 'gene', 'fitness': 5}]
    """
    return individuals[:pop_size]
    print("Delete this and write your code")


def evolve(objective: str, pop_size: int) -> Population:
    """
    Purpose:        A whole EC run, main driver
    Parameters:     The evolved population of solutions
    User Input:     No
    Prints:         Updates every time fitness switches.
    Returns:        Population
    Modifies:       Various data structures
    Calls:          Basic python only, all your functions
    Tests:          ./stdio_tests/* and ./arg_tests/
    Status:         Giving you this one.
    """
    # To debug doctest test in pudb
    # Highlight the line of code below below
    # Type 't' to jump 'to' it
    # Type 's' to 'step' deeper
    # Type 'n' to 'next' over
    # Type 'f' or 'r' to finish/return a function call and go back to caller
    population = initialize_pop(objective=objective, pop_size=pop_size)
    evaluate_group(objective=objective, individuals=population)
    rank_group(individuals=population)
    best_fitness = population[0]["fitness"]
    perfect_fitness = len(objective)
    counter = 0
    while best_fitness < perfect_fitness:
        counter += 1
        parents = parent_select(individuals=population, number=80)
        children = recombine_group(parents=parents, recombine_rate=0.8)
        mutate_rate = (1 - (best_fitness / perfect_fitness)) / 5
        mutants = mutate_group(children=children, mutate_rate=mutate_rate)
        evaluate_group(objective=objective, individuals=mutants)
        everyone = population + mutants
        rank_group(individuals=everyone)
        population = survivor_select(individuals=everyone, pop_size=pop_size)
        if best_fitness != population[0]["fitness"]:
            best_fitness = population[0]["fitness"]
            print("Iteration number", counter, "with best individual", population[0])
    return population


if __name__ == "__main__":
    # Execute doctests to protect main:
    import doctest
    import json

    # This seeds, so can be commented for random runs
    doctest.testmod()
    # doctest.testmod(verbose=True)

    if len(sys.argv) == 3:
        with open(file=sys.argv[1]) as finput:
            obj_name = finput.readlines()
            OBJECTIVE = obj_name[0].strip()
            POP_SIZE = int(obj_name[1])
        with open(file=sys.argv[2], mode="w") as foutput:
            population = evolve(OBJECTIVE, POP_SIZE)
            foutput.write(json.dumps(population) + "\n")
    else:
        OBJECTIVE = input("What string would you like to evolve?\n")
        POP_SIZE = int(input("How many individuals would you like to evolve?\n"))
        population = evolve(OBJECTIVE, POP_SIZE)
