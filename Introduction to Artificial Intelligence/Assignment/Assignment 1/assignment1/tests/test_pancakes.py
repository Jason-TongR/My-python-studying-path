import unittest

from problems.pancakes import PancakeProblem, PancakeState, flip_cost_heuristic, gap_heuristic
from tests.helpers import exact_costs


class TestPancakeProblem(unittest.TestCase):
    def test_goal(self) -> None:
        problem = PancakeProblem((3, 1, 2))
        self.assertEqual(problem.get_goal_state(), PancakeState((1, 2, 3)))
        self.assertTrue(problem.is_goal(PancakeState((1, 2, 3))))
        self.assertFalse(problem.is_goal(PancakeState((2, 1, 3))))

    def test_successors(self) -> None:
        successors = dict((action, s.stack) for s, action in PancakeProblem((3, 1, 4, 2)).get_successors(PancakeState((3, 1, 4, 2))))
        self.assertEqual(successors, {"flip 2": (1, 3, 4, 2), "flip 3": (4, 1, 3, 2), "flip 4": (2, 4, 1, 3)})

    def test_predecessors(self) -> None:
        problem = PancakeProblem((3, 1, 4, 2))
        state = PancakeState((2, 4, 1, 3))
        for previous, action in problem.get_predecessors(state):
            self.assertIn((state, action), list(problem.get_successors(previous)))
        self.assertEqual(len(list(problem.get_predecessors(state))), 3)

    def test_action_costs(self) -> None:
        a, b = PancakeState((3, 2, 1)), PancakeState((1, 2, 3))
        self.assertEqual(PancakeProblem((3, 2, 1)).get_action_cost(a, "flip 3", b), 1)
        self.assertEqual(PancakeProblem((3, 2, 1), flip_cost=True).get_action_cost(a, "flip 3", b), 3)

    def test_gap_heuristic_examples(self) -> None:
        self.assertEqual(gap_heuristic(PancakeState((1, 2, 3, 4))), 0)
        self.assertEqual(gap_heuristic(PancakeState((4, 3, 2, 1))), 1)      # 1 above the plate (5)
        self.assertEqual(gap_heuristic(PancakeState((2, 4, 1, 3))), 4)

    def test_gap_heuristic_is_admissible_and_consistent(self) -> None:
        exact = exact_costs(6, flip_cost=False)
        problem = PancakeProblem((1, 2, 3, 4, 5, 6))
        for stack, cost in exact.items():
            state = PancakeState(stack)
            self.assertLessEqual(gap_heuristic(state), cost, f"overestimates on {stack}")
            for nxt, action in problem.get_successors(state):
                self.assertLessEqual(gap_heuristic(state), 1 + gap_heuristic(nxt), f"inconsistent on {stack}")

    def test_flip_cost_heuristic_is_admissible(self) -> None:
        exact = exact_costs(6, flip_cost=True)
        for stack, cost in exact.items():
            state = PancakeState(stack)
            self.assertLessEqual(flip_cost_heuristic(state), cost, f"overestimates on {stack}")
            self.assertGreaterEqual(flip_cost_heuristic(state), gap_heuristic(state))


if __name__ == "__main__":
    unittest.main()
