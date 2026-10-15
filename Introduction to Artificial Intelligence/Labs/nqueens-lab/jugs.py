"""The water jug problem: with jugs of 5 and 3 liters, measure exactly 4 liters.

A state is a pair (x, y): the liters in the 5-liter jug and in the 3-liter jug.
This is reference code: breadth-first search and depth-first search, written
directly for this problem. There are no costs, and no check for repeated states.

Run it with:  python jugs.py
"""
from collections import deque

JugState = tuple[int, int]   # (liters in the 5-liter jug, liters in the 3-liter jug)


def is_goal(state: JugState) -> bool:
    """True if one of the jugs holds exactly 4 liters."""
    x, y = state
    return x == 4 or y == 4


def successors(state: JugState) -> list[JugState]:
    """The states reachable from state with one move."""
    x, y = state
    pour12 = min(x, 3 - y)    # liters poured from the 5-liter jug into the 3-liter jug
    pour21 = min(y, 5 - x)    # liters poured from the 3-liter jug into the 5-liter jug
    candidates = [
        (5, y),                     # fill the 5-liter jug
        (x, 3),                     # fill the 3-liter jug
        (0, y),                     # empty the 5-liter jug
        (x, 0),                     # empty the 3-liter jug
        (x - pour12, y + pour12),   # pour the 5-liter jug into the 3-liter jug
        (x + pour21, y - pour21),   # pour the 3-liter jug into the 5-liter jug
    ]
    result: list[JugState] = []
    for candidate in candidates:
        if candidate != state:      # leave out moves that change nothing
            result.append(candidate)
    return result


def bfs(start: JugState) -> list[JugState] | None:
    """Breadth-first search. Returns the list of states from start to a goal, or None."""
    queue: deque[list[JugState]] = deque()   # a queue, like Java's ArrayDeque
    queue.append([start])       # each element of the queue is a path: a list of states
    while queue:                # while the queue is not empty
        path = queue.popleft()  # take the oldest path in the queue
        state = path[-1]        # the last state of the path
        if is_goal(state):
            return path
        for next_state in successors(state):
            queue.append(path + [next_state])
    return None


def dfs(state: JugState, depth_limit: int) -> list[JugState] | None:
    """Depth-first search, at most depth_limit moves deep.

    Returns the list of states from state to a goal, or None. Without the depth
    limit, this search could go around in circles forever: for example, filling
    the 5-liter jug, emptying it, filling it again, and so on.
    """
    if is_goal(state):
        return [state]
    if depth_limit == 0:
        return None
    for next_state in successors(state):
        path = dfs(next_state, depth_limit - 1)
        if path is not None:
            return [state] + path
    return None


def show(name: str, path: list[JugState] | None) -> None:
    if path is None:
        print(name + ": no solution")
    else:
        print(name + ":", len(path) - 1, "moves:", " -> ".join(str(s) for s in path))


if __name__ == "__main__":
    show("Breadth-first search", bfs((0, 0)))
    depth_limit = 10   # change this number to try other limits
    show(f"Depth-first search, depth limit {depth_limit}", dfs((0, 0), depth_limit))
