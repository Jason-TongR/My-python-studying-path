"""The pancake problem: sort a stack of pancakes by repeatedly flipping the top k of them.

The pancakes have sizes 1, ..., n; a stack lists them from the top down, and it is sorted
when the smallest is on top: (1, 2, ..., n). Flipping k pancakes (2 <= k <= n) reverses
the order of the top k. Flips are their own inverse: flipping the same k twice undoes it.
"""
from collections.abc import Iterable

from core.reversible import ReversibleSearchProblem
from core.search_state import SearchState


class PancakeState(SearchState):
    """A stack of pancakes, from the top down."""

    def __init__(self, stack: tuple[int, ...]) -> None:
        self.stack = stack

    def key(self) -> tuple[int, ...]:
        return self.stack

    def __str__(self) -> str:
        return " ".join(str(p) for p in self.stack)


class PancakeProblem(ReversibleSearchProblem[PancakeState]):
    """Sort a stack with flips. Action names are "flip k".

    flip_cost=False: every flip costs 1. flip_cost=True: flipping k pancakes costs k.
    """

    def __init__(self, stack: tuple[int, ...], flip_cost: bool = False) -> None:
        self.stack = stack
        self.flip_cost = flip_cost

    def get_initial_state(self) -> PancakeState:
        return PancakeState(self.stack)

    def get_goal_state(self) -> PancakeState:
        # TODO: the sorted stack.
        raise NotImplementedError("get_goal_state")   # remove this line when you are done

    def is_goal(self, state: PancakeState) -> bool:
        # TODO:
        raise NotImplementedError("is_goal")   # remove this line when you are done

    def get_successors(self, state: PancakeState) -> Iterable[tuple[PancakeState, str]]:
        # TODO: one successor per flip of k = 2, ..., n pancakes, with the
        #       action "flip k".
        raise NotImplementedError("get_successors")   # remove this line when you are done

    def get_predecessors(self, state: PancakeState) -> Iterable[tuple[PancakeState, str]]:
        # TODO: which states lead to state in one flip, and with which action?
        raise NotImplementedError("get_predecessors")   # remove this line when you are done

    def get_action_cost(self, state: PancakeState, action: str, next_state: PancakeState) -> float:
        # TODO: 1, or k for "flip k" when flip_cost is True.
        raise NotImplementedError("get_action_cost")   # remove this line when you are done


def gap_heuristic(state: PancakeState) -> float:
    """The number of gaps: pairs of adjacent pancakes whose sizes differ by more than 1.
    The plate counts as a pancake of size n + 1 under the stack."""
    # TODO:
    raise NotImplementedError("gap_heuristic")   # remove this line when you are done


def my_heuristic(state: PancakeState) -> float:
    """A heuristic of your own design, for unit-cost flips. In the report, say whether it is
    admissible and consistent, with a proof or a counterexample."""
    # TODO: your own heuristic.
    raise NotImplementedError("my_heuristic")   # remove this line when you are done


def flip_cost_heuristic(state: PancakeState) -> float:
    """An admissible heuristic for the variant where flipping k pancakes costs k, better
    informed than gap_heuristic. Prove its admissibility in the report."""
    # TODO: what is the cheapest flip that can remove a gap? Which
    #       flips can remove the gap between the bottom pancake and the plate?
    raise NotImplementedError("flip_cost_heuristic")   # remove this line when you are done
