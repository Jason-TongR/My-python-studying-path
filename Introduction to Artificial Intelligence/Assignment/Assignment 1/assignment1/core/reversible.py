from abc import abstractmethod
from collections.abc import Iterable

from core.search_problem import S, SearchProblem


class ReversibleSearchProblem(SearchProblem[S]):
    """A search problem with a single goal state, whose steps can also be followed
    backwards: what bidirectional search needs.

    Subclasses MUST implement get_goal_state and get_predecessors, as well as the
    abstract methods of SearchProblem.
    """

    @abstractmethod
    def get_goal_state(self) -> S:
        """The goal state (is_goal must be true for it, and only for it)."""

    @abstractmethod
    def get_predecessors(self, state: S) -> Iterable[tuple[S, str]]:
        """Pairs (previous_state, action) such that action leads from previous_state to state."""
