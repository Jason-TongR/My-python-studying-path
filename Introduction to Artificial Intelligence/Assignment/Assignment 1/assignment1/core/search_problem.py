from abc import ABC, abstractmethod
from collections.abc import Iterable
from typing import Generic, TypeVar

from core.search_state import SearchState

S = TypeVar("S", bound=SearchState)


class SearchProblem(ABC, Generic[S]):
    """A search problem whose states have type S.

    Subclasses MUST implement the three abstract methods.
    They MAY override get_action_cost (a hook with a default).
    """

    @abstractmethod
    def get_initial_state(self) -> S:
        """The state the search starts from."""

    @abstractmethod
    def is_goal(self, state: S) -> bool:
        """True if state is a goal state."""

    @abstractmethod
    def get_successors(self, state: S) -> Iterable[tuple[S, str]]:
        """Pairs (next_state, action) for every action applicable in state."""

    def get_action_cost(self, state: S, action: str, next_state: S) -> float:
        """Cost of a single step. Unit cost unless overridden."""
        return 1
