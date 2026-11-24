import unittest

from algorithms.bidirectional import bidirectional_search
from algorithms.uninformed import breadth_first_search
from problems.pancakes import PancakeProblem
from tests.test_informed import random_stacks


class TestBidirectionalSearch(unittest.TestCase):
    def check_path(self, problem: PancakeProblem) -> int:
        node = bidirectional_search(problem)
        assert node is not None
        path = node.path()
        self.assertEqual(path[0].state, problem.get_initial_state())
        self.assertTrue(problem.is_goal(path[-1].state))
        cost = 0.0
        for a, b in zip(path, path[1:]):
            successors = list(problem.get_successors(a.state))
            self.assertIn((b.state, b.action), successors, "each step must follow a legal action")
            assert b.action is not None
            cost += problem.get_action_cost(a.state, b.action, b.state)
        self.assertAlmostEqual(node.path_cost, cost, msg="path_cost must be the real cost of the path")
        return len(path) - 1

    def test_fewest_steps_like_breadth_first_search(self) -> None:
        for n in (5, 6, 7):
            for stack in random_stacks(n, 6, seed=n):
                bfs = breadth_first_search(PancakeProblem(stack))
                assert bfs is not None
                self.assertEqual(self.check_path(PancakeProblem(stack)), bfs.depth, f"stack {stack}")

    def test_real_path_costs_with_flip_costs(self) -> None:
        for stack in random_stacks(6, 4, seed=11):
            self.check_path(PancakeProblem(stack, flip_cost=True))

    def test_start_is_goal(self) -> None:
        node = bidirectional_search(PancakeProblem((1, 2, 3, 4)))
        assert node is not None
        self.assertEqual(node.depth, 0)


if __name__ == "__main__":
    unittest.main()
