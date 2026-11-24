import heapq
from abc import ABC, abstractmethod
from collections import deque
from collections.abc import Callable
from itertools import count
from typing import Generic

from core.node import Node
from core.search_problem import S


class Frontier(ABC, Generic[S]):
    """The nodes generated but not yet expanded."""

    @abstractmethod
    def add(self, node: Node[S]) -> None: ...

    @abstractmethod
    def remove(self) -> Node[S]: ...

    @abstractmethod
    def __len__(self) -> int: ...

    def is_empty(self) -> bool:
        return len(self) == 0


class FIFOFrontier(Frontier[S]):
    """First in, first out: a queue."""

    def __init__(self) -> None:
        self._items: deque[Node[S]] = deque()

    def add(self, node: Node[S]) -> None:
        self._items.append(node)

    def remove(self) -> Node[S]:
        return self._items.popleft()

    def __len__(self) -> int:
        return len(self._items)


class LIFOFrontier(Frontier[S]):
    """Last in, first out: a stack."""

    def __init__(self) -> None:
        self._items: list[Node[S]] = []

    def add(self, node: Node[S]) -> None:
        self._items.append(node)

    def remove(self) -> Node[S]:
        return self._items.pop()

    def __len__(self) -> int:
        return len(self._items)


class PriorityFrontier(Frontier[S]):
    """Pops the node with the lowest key(node) first."""

    def __init__(self, key: Callable[[Node[S]], float]) -> None:
        self._key = key
        self._heap: list[tuple[float, int, Node[S]]] = []
        self._tie = count()  # breaks ties, so nodes are never compared

    def add(self, node: Node[S]) -> None:
        heapq.heappush(self._heap, (self._key(node), next(self._tie), node))

    def remove(self) -> Node[S]:
        return heapq.heappop(self._heap)[2]

    def __len__(self) -> int:
        return len(self._heap)
