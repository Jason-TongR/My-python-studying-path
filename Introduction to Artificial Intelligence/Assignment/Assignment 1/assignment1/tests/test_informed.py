import random
import unittest

from algorithms.informed import a_star_search, best_first_search, greedy_search, ida_star_search, weighted_a_star_search
from algorithms.uninformed import breadth_first_search
from problems.pancakes import PancakeProblem, gap_heuristic
from tests.helpers import RoadMap, straight_line


def random_stacks(n: int, count: int, seed: int) -> list[tuple[int, ...]]:
    rng = random.Random(seed)
    stacks = []
    for _ in range(count):
        stack = list(range(1, n + 1))
        rng.shuffle(stack)
        stacks.append(tuple(stack))
    return stacks


class TestInformedSearch(unittest.TestCase):
    def test_best_first_with_path_cost_is_uniform_cost(self) -> None:
        node = best_first_search(RoadMap(), lambda n: n.path_cost)
        assert node is not None
        self.assertEqual(node.path_cost, 16)

    def test_greedy_on_the_road_map(self) -> None:
        node = greedy_search(RoadMap(), straight_line)
        assert node is not None
        self.assertEqual([n.state.name for n in node.path()], ["S", "A", "D", "G"])
        self.assertEqual(node.path_cost, 17)

    def test_a_star_on_the_road_map(self) -> None:
        node = a_star_search(RoadMap(), straight_line)
        assert node is not None
        self.assertEqual([n.state.name for n in node.path()], ["S", "B", "D", "G"])
        self.assertEqual(node.path_cost, 16)

    def test_weighted_a_star_with_weight_1_is_a_star(self) -> None:
        node = weighted_a_star_search(RoadMap(), straight_line, 1)
        assert node is not None
        self.assertEqual(node.path_cost, 16)

    def test_a_star_is_optimal_on_pancakes(self) -> None:
        for stack in random_stacks(7, 5, seed=1):
            bfs = breadth_first_search(PancakeProblem(stack))
            a_star = a_star_search(PancakeProblem(stack), gap_heuristic)
            assert bfs is not None and a_star is not None
            self.assertEqual(a_star.path_cost, bfs.path_cost, f"stack {stack}")

    def test_weighted_a_star_within_its_bound(self) -> None:
        for stack in random_stacks(7, 5, seed=2):
            best = a_star_search(PancakeProblem(stack), gap_heuristic)
            weighted = weighted_a_star_search(PancakeProblem(stack), gap_heuristic, 2)
            assert best is not None and weighted is not None
            self.assertLessEqual(weighted.path_cost, 2 * best.path_cost)

    def test_ida_star_on_the_road_map(self) -> None:
        node = ida_star_search(RoadMap(), straight_line)
        assert node is not None
        self.assertEqual(node.path_cost, 16)

    def test_ida_star_is_optimal_on_pancakes(self) -> None:
        for flip_cost in (False, True):
            for stack in random_stacks(7, 4, seed=3):
                a_star = a_star_search(PancakeProblem(stack, flip_cost), gap_heuristic)
                ida = ida_star_search(PancakeProblem(stack, flip_cost), gap_heuristic)
                assert a_star is not None and ida is not None
                self.assertEqual(ida.path_cost, a_star.path_cost, f"stack {stack}, flip_cost {flip_cost}")
                self.assertTrue(PancakeProblem(stack).is_goal(ida.state))


if __name__ == "__main__":
    unittest.main()
