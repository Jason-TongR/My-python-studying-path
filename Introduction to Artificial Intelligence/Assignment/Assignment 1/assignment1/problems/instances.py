"""The instances of your team: they are generated from your team number, so every team has
its own. Do not change this file."""
import random

from problems.coloring import GraphColoring
from problems.knapsack import Knapsack


def team_random(team: int, part: str) -> random.Random:
    """A random generator that depends only on the team number and the part of the assignment."""
    return random.Random(f"team {team}, {part}")


def pancake_instances(team: int) -> dict[str, list[tuple[int, ...]]]:
    """Stacks of 7, 8 and 14 pancakes."""
    rng = team_random(team, "pancakes")
    result: dict[str, list[tuple[int, ...]]] = {}
    for name, n, count in (("small", 7, 3), ("medium", 8, 2), ("large", 14, 2)):
        stacks = []
        for _ in range(count):
            stack = list(range(1, n + 1))
            while stack == sorted(stack):
                rng.shuffle(stack)
            stacks.append(tuple(stack))
        result[name] = stacks
    return result


def knapsack_instance(team: int) -> Knapsack:
    """40 items; the capacity is half their total weight."""
    rng = team_random(team, "knapsack")
    weights = [rng.randint(5, 40) for _ in range(40)]
    values = [rng.randint(10, 100) for _ in range(40)]
    return Knapsack(weights, values, sum(weights) // 2)


def knapsack_optimum(problem: Knapsack) -> int:
    """The best total value, by dynamic programming (to measure how close local search gets)."""
    best = [0] * (problem.capacity + 1)
    for w, v in zip(problem.weights, problem.values):
        for c in range(problem.capacity, w - 1, -1):
            best[c] = max(best[c], best[c - w] + v)
    return best[problem.capacity]


def coloring_instance(team: int) -> GraphColoring:
    """A graph of 40 nodes that can be colored with 4 colors: edges are drawn at random, but
    only between nodes of different colors in a hidden 4-coloring."""
    rng = team_random(team, "coloring")
    n, k = 40, 4
    hidden = [rng.randrange(k) for _ in range(n)]
    edges = [(a, b) for a in range(n) for b in range(a + 1, n) if hidden[a] != hidden[b] and rng.random() < 0.25]
    return GraphColoring(n, edges, k)
