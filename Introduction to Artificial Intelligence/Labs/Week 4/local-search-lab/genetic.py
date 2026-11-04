"""A genetic algorithm, and the selection schemes it can use. Individuals can be of any
type: the problem provides the fitness (to maximize), crossover and mutation.
"""
import random
from collections.abc import Callable
from typing import TypeVar

I = TypeVar("I")   # the type of the individuals

Selection = Callable[[list[I], list[float]], I]


def tournament_selection(k: int) -> Selection[I]:
    """Selection by tournaments of k individuals: the fittest of k random ones wins."""
    def select(population: list[I], scores: list[float]) -> I:
        # TODO: choose k different positions at random (random.sample(range(len(population)), k)),
        #       and return the individual with the best score among them.
        raise NotImplementedError("tournament_selection")   # remove this line when you are done
    return select


def roulette_selection(population: list[I], scores: list[float]) -> I:
    """Fitness-proportionate selection: each individual is chosen with a probability
    proportional to its fitness (which must be positive)."""
    return random.choices(population, weights=scores)[0]


def genetic_algorithm(population: list[I], fitness: Callable[[I], float],
                      select: Selection[I], crossover: Callable[[I, I], I],
                      mutate: Callable[[I], I], mutation_rate: float, generations: int,
                      elite: int = 1, target: float | None = None) -> tuple[I, int, list[tuple[float, float]]]:
    """Evolve the population for at most the given number of generations, or until an
    individual reaches the target fitness. The elite best individuals pass unchanged to the
    next generation. Returns the best individual, the number of generations, and the best
    and average fitness of every generation."""
    history: list[tuple[float, float]] = []
    for generation in range(generations + 1):
        scores = [fitness(individual) for individual in population]
        best = max(range(len(population)), key=lambda i: scores[i])
        history.append((scores[best], sum(scores) / len(scores)))
        if (target is not None and scores[best] >= target) or generation == generations:
            return population[best], generation, history
        ranked = sorted(range(len(population)), key=lambda i: scores[i], reverse=True)
        next_population = [population[i] for i in ranked[:elite]]
        while len(next_population) < len(population):
            child = crossover(select(population, scores), select(population, scores))
            if random.random() < mutation_rate:
                child = mutate(child)
            next_population.append(child)
        population = next_population
    raise AssertionError("unreachable")


# ---- operators for N-queens: a board is a list of rows, one per column -------------------

def one_point_crossover(parent1: list[int], parent2: list[int]) -> list[int]:
    """The child takes the columns before a random cut from parent1, and the rest from parent2."""
    # TODO: choose a cut between 1 and len(parent1) - 1, and join the two parts.
    raise NotImplementedError("one_point_crossover")   # remove this line when you are done


def mutate_queens(board: list[int]) -> list[int]:
    """Move one random queen to a random row of its column."""
    # TODO: return a copy of board with one random column given a random row.
    raise NotImplementedError("mutate_queens")   # remove this line when you are done


# ---- operators for the TSP: a tour is a permutation of the cities -------------------------

def order_crossover(parent1: list[int], parent2: list[int]) -> list[int]:
    """The child keeps a random segment of parent1 in place, and fills the other positions
    with the remaining cities in the order they appear in parent2."""
    # TODO (extra): choose positions a < b at random, keep parent1[a:b] at the same positions,
    #       and fill the others with the remaining cities in the order of parent2.
    raise NotImplementedError("order_crossover")   # remove this line when you are done


def reverse_mutation(tour: list[int]) -> list[int]:
    """Reverse a random segment of the tour (a random 2-opt move)."""
    i, j = sorted(random.sample(range(len(tour)), 2))
    return tour[:i] + tour[i:j + 1][::-1] + tour[j + 1:]
