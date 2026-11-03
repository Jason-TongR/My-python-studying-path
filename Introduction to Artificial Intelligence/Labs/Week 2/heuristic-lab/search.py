"""Uniform-cost search, and best-first search with any priority: greedy search and A*.

The searches work with any problem object that has the three methods of the Problem
protocol below. States must be hashable, like tuples, because the searches use them
as dictionary keys.
"""
import heapq
from collections.abc import Callable, Hashable
from itertools import count
from typing import Generic, Protocol, TypeVar

S = TypeVar("S", bound=Hashable)   # the type of the states, like the S in Java's Problem<S>


class Problem(Protocol[S]):
    """What a search needs from a problem."""

    def initial_state(self) -> S:
        """The state where the search starts."""
        ...

    def successors(self, state: S) -> list[tuple[S, float]]:
        """The states reachable from state with one action, each with the cost of that action."""
        ...

    def is_goal(self, state: S) -> bool:
        """True if state is a goal."""
        ...


class SearchResult(Generic[S]):
    """What a search found."""

    def __init__(self, path: list[S] | None, cost: float, expanded: list[S]) -> None:
        self.path = path            # the states from the initial state to a goal, or None
        self.cost = cost            # the cost of that path
        self.expanded = expanded    # the states expanded, in the order they were expanded


def path_to(state: S, parent: dict[S, S | None]) -> list[S]:
    """The states from the initial state to state, following the parent links back."""
    path: list[S] = []
    current: S | None = state
    while current is not None:
        path.append(current)
        current = parent[current]
    path.reverse()
    return path


def uniform_cost_search(problem: Problem[S]) -> SearchResult[S]:
    """Always expand the state whose path is the cheapest so far."""
    start = problem.initial_state()
    tie = count()                                   # 0, 1, 2, ...: breaks ties, so states are never compared
    frontier: list[tuple[float, int, S]] = [(0.0, next(tie), start)]   # a heap of (g, tie, state)
    best_g: dict[S, float] = {start: 0.0}           # the cheapest known cost of every reached state
    parent: dict[S, S | None] = {start: None}       # how each state was reached
    expanded: list[S] = []
    while frontier:
        g, _, state = heapq.heappop(frontier)       # the entry with the lowest g
        if g > best_g[state]:
            continue                                # outdated: a cheaper path to state was found later
        if problem.is_goal(state):
            return SearchResult(path_to(state, parent), g, expanded)
        expanded.append(state)
        for next_state, step_cost in problem.successors(state):
            new_g = g + step_cost
            if next_state not in best_g or new_g < best_g[next_state]:
                best_g[next_state] = new_g
                parent[next_state] = state
                heapq.heappush(frontier, (new_g, next(tie), next_state))
    return SearchResult(None, float("inf"), expanded)


def best_first_search(problem: Problem[S], f: Callable[[float, S], float]) -> SearchResult[S]:
    """Always expand the state with the lowest f(g, state), where g is the cost of its path.

    This is uniform_cost_search with one change: the priority of a state in the
    frontier is f(g, state) instead of g. Copy uniform_cost_search and adapt it.
    The frontier needs to hold (f, tie, g, state): g is still needed, to compute
    the cost of the next states and to recognize outdated entries.
    """
    # TODO
    raise NotImplementedError("best_first_search")   # remove this line when you are done


def greedy_search(problem: Problem[S], h: Callable[[S], float]) -> SearchResult[S]:
    """Greedy best-first search: f = h."""
    # TODO: one line, calling best_first_search
    raise NotImplementedError("greedy_search")   # remove this line when you are done


def a_star_search(problem: Problem[S], h: Callable[[S], float]) -> SearchResult[S]:
    """A*: f = g + h."""
    # TODO: one line, calling best_first_search
    raise NotImplementedError("a_star_search")   # remove this line when you are done
