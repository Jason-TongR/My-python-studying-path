"""Breadth-first search and depth-first search.

Both work with any problem object that has three methods, described by the
Problem protocol below. Both return the path found, as a list of states from the
initial state to a goal, or None if there is no solution. Neither checks for
repeated states.
"""
from collections import deque
from typing import Protocol, TypeVar

S = TypeVar("S")   # the type of the states: like the type parameter S in Java's Problem<S>


class Problem(Protocol[S]):
    """What a search needs from a problem, like a Java interface Problem<S>.

    A class does not need to declare that it implements Problem: it is enough
    that it has these three methods, with these types.
    """

    def initial_state(self) -> S:
        """The state where the search starts."""
        ...

    def successors(self, state: S) -> list[S]:
        """The states reachable from state with one action."""
        ...

    def is_goal(self, state: S) -> bool:
        """True if state is a solution."""
        ...


def bfs(problem: Problem[S]) -> list[S] | None:
    """Breadth-first search, with a queue of paths."""
    queue: deque[list[S]] = deque()              # a queue, like Java's ArrayDeque
    queue.append([problem.initial_state()])      # each element of the queue is a path
    while queue:                                 # while the queue is not empty
        path = queue.popleft()                   # take the oldest path in the queue
        state = path[-1]                         # the last state of the path
        if problem.is_goal(state):
            return path
        for next_state in problem.successors(state):
            queue.append(path + [next_state])
    return None


def dfs(problem: Problem[S]) -> list[S] | None:
    """Depth-first search, written recursively."""
    return dfs_from(problem, problem.initial_state())


def dfs_from(problem: Problem[S], state: S) -> list[S] | None:
    """Search depth-first from state. Returns a path from state to a goal, or None.

    Look at dfs in jugs.py: it is the same idea, without the depth limit.
    """
    # TODO 1: if state is a goal, return the path [state].
    # TODO 2: for each successor next_state of state:
    #             search recursively from next_state;
    #             if that search found a path, return [state] + that path.
    # TODO 3: if no successor leads to a goal, return None.
    raise NotImplementedError("dfs_from")   # remove this line when you are done
