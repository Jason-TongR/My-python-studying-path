import random
import unittest

from algorithms.genetic import evolve, rank_selection, tournament_selection
from algorithms.local_search import hill_climbing, local_beam_search, random_restart, stochastic_hill_climbing
from problems.coloring import GraphColoring
from problems.knapsack import Knapsack


def small_knapsack() -> Knapsack:
    return Knapsack([4, 6, 3, 8, 5, 2, 7, 9], [10, 13, 7, 15, 9, 4, 12, 16], 20)


def cycle(n: int) -> GraphColoring:
    """A cycle of n nodes, to color with 3 colors."""
    return GraphColoring(n, [(i, (i + 1) % n) for i in range(n)], 3)


class TestProblems(unittest.TestCase):
    def test_knapsack_fitness_and_cost(self) -> None:
        k = small_knapsack()
        fits = [1, 1, 1, 0, 0, 1, 0, 0]           # weight 15, value 34
        too_heavy = [1, 1, 1, 1, 1, 1, 1, 1]      # weight 44: 24 too much
        self.assertEqual(k.fitness(fits), 34)
        self.assertEqual(k.fitness(too_heavy), -24)
        self.assertEqual(k.cost(fits), -34)

    def test_knapsack_neighbors_and_operators(self) -> None:
        k = small_knapsack()
        s = [0] * 8
        self.assertEqual(len(k.neighbors(s)), 8)
        self.assertTrue(all(sum(n) == 1 for n in k.neighbors(s)))
        child = k.mutate(s)
        self.assertEqual(sum(child), 1)
        self.assertEqual(s, [0] * 8, "mutate must not modify its argument")
        mix = k.crossover([0] * 8, [1] * 8)
        self.assertEqual(len(mix), 8)
        self.assertTrue(set(mix) <= {0, 1})

    def test_coloring(self) -> None:
        triangle = GraphColoring(3, [(0, 1), (1, 2), (0, 2)], 3)
        self.assertEqual(triangle.conflicts([0, 0, 0]), 3)
        self.assertEqual(triangle.conflicts([0, 1, 2]), 0)
        self.assertEqual(triangle.fitness([0, 0, 1]), 2)
        self.assertEqual(len(triangle.neighbors([0, 1, 2])), 6)
        child = triangle.mutate([0, 1, 2])
        self.assertTrue(all(0 <= c < 3 for c in child))
        mix = triangle.crossover([0, 0, 0], [1, 1, 1])
        self.assertTrue(set(mix) <= {0, 1})


class TestLocalSearch(unittest.TestCase):
    def test_stochastic_hill_climbing_reaches_a_local_optimum(self) -> None:
        random.seed(1)
        k = small_knapsack()
        for _ in range(20):
            start = k.random_state()
            end, moves = stochastic_hill_climbing(k, start)
            self.assertLessEqual(k.cost(end), k.cost(start))
            self.assertTrue(all(k.cost(n) >= k.cost(end) for n in k.neighbors(end)))

    def test_random_restart_keeps_the_best_and_stops_at_cost_0(self) -> None:
        random.seed(2)
        problem = cycle(20)
        best, moves = random_restart(problem, hill_climbing, 200)
        self.assertEqual(problem.cost(best), 0)

    def test_local_beam_search(self) -> None:
        random.seed(3)
        problem = cycle(20)
        best, steps = local_beam_search(problem, 10)
        self.assertEqual(problem.cost(best), 0)
        k = small_knapsack()
        best_k, _ = local_beam_search(k, 5)
        self.assertGreater(k.fitness(best_k), 0, "the result should fit in the knapsack")


class TestGenetic(unittest.TestCase):
    def test_rank_selection_follows_the_ranks(self) -> None:
        random.seed(4)
        population, scores = ["worst", "middle", "best"], [-5.0, 0.0, 10.0]
        counts = {p: 0 for p in population}
        for _ in range(6000):
            counts[rank_selection(population, scores)] += 1
        # ranks 1, 2, 3: probabilities 1/6, 2/6, 3/6
        self.assertAlmostEqual(counts["worst"] / 6000, 1 / 6, delta=0.03)
        self.assertAlmostEqual(counts["best"] / 6000, 3 / 6, delta=0.03)

    def test_evolve_keeps_the_best_and_improves(self) -> None:
        random.seed(5)
        k = small_knapsack()
        best, history = evolve(k, 30, 40, tournament_selection(3), 0.3, elite=1)
        self.assertEqual(len(history), 41)
        self.assertTrue(all(a <= b for a, b in zip(history, history[1:])), "with elitism the best never gets worse")
        self.assertEqual(k.fitness(best), history[-1])
        self.assertGreaterEqual(history[-1], 40)

    def test_evolve_works_for_coloring_unchanged(self) -> None:
        random.seed(6)
        problem = cycle(16)
        best, history = evolve(problem, 40, 150, tournament_selection(3), 0.5, elite=2)
        self.assertEqual(problem.conflicts(best), 0)


if __name__ == "__main__":
    unittest.main()
