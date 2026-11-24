"""The 0/1 knapsack problem: choose items of greatest total value whose total weight does not
exceed the capacity. A candidate is a list of 0s and 1s, one per item: 1 means "take it".
"""
import random

from core.optimization import GeneticProblem, OptimizationProblem

Selection = list[int]


class Knapsack(OptimizationProblem[Selection], GeneticProblem[Selection]):
    """For local search, the cost is minus the fitness."""

    def __init__(self, weights: list[int], values: list[int], capacity: int) -> None:
        self.weights = weights
        self.values = values
        self.capacity = capacity

    def total_weight(self, s: Selection) -> int:
        return sum(w for w, take in zip(self.weights, s) if take)

    def total_value(self, s: Selection) -> int:
        return sum(v for v, take in zip(self.values, s) if take)

    def fitness(self, s: Selection) -> float:
        """The total value if the items fit; if they do not, minus the excess weight, so that
        any candidate that fits beats any candidate that does not."""
        # TODO:
        raise NotImplementedError("fitness")   # remove this line when you are done

    def cost(self, s: Selection) -> float:
        # TODO:
        raise NotImplementedError("cost")   # remove this line when you are done

    def random_state(self) -> Selection:
        # TODO: each item taken with probability 1/2.
        raise NotImplementedError("random_state")   # remove this line when you are done

    def neighbors(self, s: Selection) -> list[Selection]:
        # TODO: take or leave one item more: one neighbor per item.
        raise NotImplementedError("neighbors")   # remove this line when you are done

    def random_individual(self) -> Selection:
        return self.random_state()

    def crossover(self, parent1: Selection, parent2: Selection) -> Selection:
        # TODO: one-point crossover.
        raise NotImplementedError("crossover")   # remove this line when you are done

    def mutate(self, s: Selection) -> Selection:
        # TODO: take or leave one random item.
        raise NotImplementedError("mutate")   # remove this line when you are done
