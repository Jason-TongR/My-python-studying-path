"""Small problems with known answers, used by the tests."""
import heapq
import itertools
import math
from collections.abc import Iterable

from core.search_problem import SearchProblem
from core.search_state import SearchState
from problems.pancakes import PancakeProblem, PancakeState


class City(SearchState):
    def __init__(self, name: str) -> None:
        self.name = name

    def key(self) -> str:
        return self.name

    def __str__(self) -> str:
        return self.name


ROADS = {("S", "A"): 5, ("S", "B"): 5, ("A", "C"): 5, ("A", "D"): 7, ("B", "D"): 6, ("C", "G"): 8, ("D", "G"): 5}
H = {"S": 12.0, "A": 8.5, "B": 9.4, "C": 5.6, "D": 4.4, "G": 0.0}   # straight-line distances to G


class RoadMap(SearchProblem[City]):
    """The road map of lecture 2: the cheapest route from S to G costs 16 (S B D G)."""

    def get_initial_state(self) -> City:
        return City("S")

    def is_goal(self, state: City) -> bool:
        return state.name == "G"

    def get_successors(self, state: City) -> Iterable[tuple[City, str]]:
        for a, b in ROADS:
            if state.name in (a, b):
                other = b if state.name == a else a
                yield City(other), f"{state.name}-{other}"

    def get_action_cost(self, state: City, action: str, next_state: City) -> float:
        return ROADS.get((state.name, next_state.name), ROADS.get((next_state.name, state.name), math.inf))


def straight_line(state: City) -> float:
    return H[state.name]


def exact_costs(n: int, flip_cost: bool) -> dict[tuple[int, ...], float]:
    """The true cost from every stack of n pancakes to the sorted one (Dijkstra from the goal;
    flips are their own inverse, so distances are symmetric)."""
    problem = PancakeProblem(tuple(range(1, n + 1)), flip_cost)
    goal = problem.get_goal_state()
    dist: dict[tuple[int, ...], float] = {goal.stack: 0}
    heap: list[tuple[float, int, tuple[int, ...]]] = [(0, 0, goal.stack)]
    tie = itertools.count(1)
    while heap:
        d, _, stack = heapq.heappop(heap)
        if d > dist[stack]:
            continue
        state = PancakeState(stack)
        for nxt, action in problem.get_successors(state):
            nd = d + problem.get_action_cost(state, action, nxt)
            if nd < dist.get(nxt.stack, math.inf):
                dist[nxt.stack] = nd
                heapq.heappush(heap, (nd, next(tie), nxt.stack))
    return dist
