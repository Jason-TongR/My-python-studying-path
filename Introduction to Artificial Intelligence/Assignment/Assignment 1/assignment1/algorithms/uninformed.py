from enum import Enum
from itertools import count
from typing import Final, Optional, Union

from core.frontier import FIFOFrontier, Frontier, LIFOFrontier, PriorityFrontier
from core.node import Node
from core.search_problem import S, SearchProblem


def graph_search(problem: SearchProblem[S],
                 frontier: Frontier[S]) -> Optional[Node[S]]:
    """Generic graph search. The frontier decides the order of expansion."""
    root = Node(problem.get_initial_state())
    frontier.add(root)
    reached: dict[S, Node[S]] = {root.state: root}
    while not frontier.is_empty():
        node = frontier.remove()
        if problem.is_goal(node.state):
            return node
        for child in node.expand(problem):
            s = child.state
            if s not in reached or child.path_cost < reached[s].path_cost:
                reached[s] = child
                frontier.add(child)
    return None


def breadth_first_search(problem: SearchProblem[S]) -> Optional[Node[S]]:
    return graph_search(problem, FIFOFrontier())


def depth_first_search(problem: SearchProblem[S]) -> Optional[Node[S]]:
    return graph_search(problem, LIFOFrontier())


def uniform_cost_search(problem: SearchProblem[S]) -> Optional[Node[S]]:
    return graph_search(problem, PriorityFrontier(lambda n: n.path_cost))


class Cutoff(Enum):
    """Result of a depth-limited search that reached its limit."""

    CUTOFF = "cutoff"


CUTOFF: Final = Cutoff.CUTOFF


def depth_limited_search(problem: SearchProblem[S], limit: int) -> Union[Node[S], Cutoff, None]:
    """Depth-first tree search up to depth `limit`, skipping cycles on the current path.

    Returns a goal node, CUTOFF if the limit was reached, or None if there is no solution.
    """

    def recurse(node: Node[S]) -> Union[Node[S], Cutoff, None]:
        if problem.is_goal(node.state):
            return node
        if node.depth == limit:
            return CUTOFF
        cutoff_occurred = False
        for child in node.expand(problem):
            if node.on_path(child.state):
                continue
            result = recurse(child)
            if result is CUTOFF:
                cutoff_occurred = True
            elif result is not None:
                return result
        return CUTOFF if cutoff_occurred else None

    return recurse(Node(problem.get_initial_state()))


def iterative_deepening_search(problem: SearchProblem[S]) -> Optional[Node[S]]:
    """Depth-limited search with limits 0, 1, 2, ... until the result is not a cutoff."""
    for limit in count():
        result = depth_limited_search(problem, limit)
        if result is not CUTOFF:
            return result
    raise AssertionError("unreachable")
