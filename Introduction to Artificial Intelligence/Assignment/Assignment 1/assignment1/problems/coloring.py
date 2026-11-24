"""Graph coloring: give each node of a graph one of k colors, so that no edge joins two nodes
of the same color. A candidate is a list of colors (0 to k - 1), one per node.
"""
import random

from core.optimization import GeneticProblem, OptimizationProblem

Coloring = list[int]


class GraphColoring(OptimizationProblem[Coloring], GeneticProblem[Coloring]):
    """The cost is the number of conflicts: edges whose two ends have the same color. The
    fitness is the number of edges without a conflict."""

    def __init__(self, n: int, edges: list[tuple[int, int]], k: int) -> None:
        self.n = n
        self.edges = edges
        self.k = k

    def conflicts(self, c: Coloring) -> int:
        # TODO:
        raise NotImplementedError("conflicts")   # remove this line when you are done

    def cost(self, c: Coloring) -> float:
        return self.conflicts(c)

    def fitness(self, c: Coloring) -> float:
        return len(self.edges) - self.conflicts(c)

    def random_state(self) -> Coloring:
        # TODO:
        raise NotImplementedError("random_state")   # remove this line when you are done

    def neighbors(self, c: Coloring) -> list[Coloring]:
        # TODO: give one node another color: n * (k - 1) neighbors.
        raise NotImplementedError("neighbors")   # remove this line when you are done

    def random_individual(self) -> Coloring:
        return self.random_state()

    def crossover(self, parent1: Coloring, parent2: Coloring) -> Coloring:
        # TODO: uniform crossover: each node takes its color from either parent,
        #       at random.
        raise NotImplementedError("crossover")   # remove this line when you are done

    def mutate(self, c: Coloring) -> Coloring:
        # TODO: give one random node a random color.
        raise NotImplementedError("mutate")   # remove this line when you are done
