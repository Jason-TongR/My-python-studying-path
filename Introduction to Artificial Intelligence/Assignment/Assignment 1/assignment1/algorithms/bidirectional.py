from collections.abc import Callable, Iterable
from typing import Optional

from core.node import Node
from core.reversible import ReversibleSearchProblem
from core.search_problem import S


def bidirectional_search(problem: ReversibleSearchProblem[S]) -> Optional[Node[S]]:
    """Bidirectional breadth-first search: one search forward from the initial state, and
    one backward from the goal state, expanding one complete layer at a time (always the
    side with the smaller layer) until they meet. Returns a goal node whose path has the
    fewest possible steps, or None if there is no solution."""
    # TODO: write it. Suggestions: keep, for each direction, a
    #       dictionary from the states it has reached to their nodes, and its current layer.
    #       When expanding a layer, note every new state that the other direction has
    #       already reached; once the layer is finished, join the two paths through the
    #       meeting state with the fewest total steps. The backward nodes' paths lead to the
    #       goal: follow them to build the second half of the result, with real path costs.
    raise NotImplementedError("bidirectional_search")   # remove this line when you are done
