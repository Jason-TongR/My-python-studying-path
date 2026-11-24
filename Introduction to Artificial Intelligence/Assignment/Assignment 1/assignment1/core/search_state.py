from abc import ABC, abstractmethod
from collections.abc import Hashable


class SearchState(ABC):
    """A configuration of a search problem. Never modify a state after creating it."""

    @abstractmethod
    def key(self) -> Hashable:
        """The data that identifies this configuration, e.g. a tuple."""

    @abstractmethod
    def __str__(self) -> str: ...

    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and self.key() == other.key()

    def __hash__(self) -> int:
        return hash(self.key())
