from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass
from typing import Generic, Optional

from core.search_problem import S, SearchProblem


@dataclass(eq=False)
class Node(Generic[S]):
    """A node of the search tree: a state plus how we got there."""

    state: S
    parent: Optional[Node[S]] = None
    action: Optional[str] = None
    path_cost: float = 0
    depth: int = 0

    def expand(self, problem: SearchProblem[S]) -> Iterator[Node[S]]:
        """The children of this node, one per successor of its state."""
        for next_state, action in problem.get_successors(self.state):
            cost = problem.get_action_cost(self.state, action, next_state)
            yield Node(next_state, self, action, self.path_cost + cost, self.depth + 1)

    def path(self) -> list[Node[S]]:
        """Nodes from the root to this node."""
        node: Optional[Node[S]] = self
        result: list[Node[S]] = []
        while node is not None:
            result.append(node)
            node = node.parent
        return result[::-1]

    def actions(self) -> list[str]:
        """The sequence of actions leading from the root to this node."""
        return [n.action for n in self.path()[1:] if n.action is not None]

    def on_path(self, state: S) -> bool:
        """True if state appears on the path from the root to this node."""
        node: Optional[Node[S]] = self
        while node is not None:
            if node.state == state:
                return True
            node = node.parent
        return False
