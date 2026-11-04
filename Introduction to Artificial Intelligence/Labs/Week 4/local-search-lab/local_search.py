"""Local search algorithms. They work on any problem given as functions: the neighbors of
a state, and the cost of a state, to be minimized.
"""
import random
from collections.abc import Callable
from typing import TypeVar

S = TypeVar("S")   # the type of the states


def best_neighbor(state: S, neighbors: Callable[[S], list[S]], cost: Callable[[S], float]) -> S:
    """A neighbor of least cost; if several are tied, one of them at random."""
    candidates = neighbors(state)
    costs = [cost(candidate) for candidate in candidates]
    least = min(costs)
    return random.choice([c for c, k in zip(candidates, costs) if k == least])


def hill_climbing(start: S, neighbors: Callable[[S], list[S]],
                  cost: Callable[[S], float]) -> tuple[S, int]:
    """Steepest descent: move to the best neighbor, as long as it is better than the current
    state. Returns the final state and the number of moves made."""
    current, moves = start, 0
    while True:
        best = best_neighbor(current, neighbors, cost)
        if cost(best) >= cost(current):
            return current, moves
        current, moves = best, moves + 1


def hill_climbing_sideways(start: S, neighbors: Callable[[S], list[S]],
                           cost: Callable[[S], float], max_sideways: int) -> tuple[S, int]:
    """Like hill_climbing, but also accepting up to max_sideways moves in a row to a
    neighbor of equal cost, to cross plateaus."""
    current, moves, sideways = start, 0, 0
    while True:
        best = best_neighbor(current, neighbors, cost)
        if cost(best) > cost(current):
            return current, moves
        if cost(best) == cost(current):
            if sideways == max_sideways:
                return current, moves
            sideways += 1
        else:
            sideways = 0
        current, moves = best, moves + 1


def first_choice_hill_climbing(start: S, random_neighbor: Callable[[S], S],
                               cost: Callable[[S], float], max_tries: int = 100) -> tuple[S, int]:
    """Try random neighbors, and move to the first one that is better. Stop after max_tries
    random neighbors in a row that are no better."""
    # TODO: like hill_climbing, but instead of looking at all the neighbors, try up to
    #       max_tries random neighbors, and move to the first one that is better.
    #       Hint: Python's for ... else runs the else part when the loop did not break.
    raise NotImplementedError("first_choice_hill_climbing")   # remove this line when you are done


def random_restart(make_start: Callable[[], S], search: Callable[[S], tuple[S, int]],
                   cost: Callable[[S], float], max_restarts: int) -> tuple[S, int, int]:
    """Run search from new random states, keeping the best result. Stop as soon as a state
    of cost 0 is found, or after max_restarts searches. Returns the best state, the number
    of searches run, and the total number of moves."""
    # TODO: call search(make_start()) up to max_restarts times, adding up the moves and
    #       keeping the best state found; return as soon as a state of cost 0 is found.
    raise NotImplementedError("random_restart")   # remove this line when you are done


def min_conflicts_queens(board: list[int], max_steps: int) -> tuple[list[int], int]:
    """Min-conflicts for N-queens: repeatedly pick a random queen under attack, and move it
    to a row of its column with the fewest attacks (ties broken at random).
    Returns the final board and the number of steps."""
    n = len(board)
    board = board.copy()
    rows = [0] * n                 # number of queens in each row
    up = [0] * (2 * n - 1)         # ... on each diagonal row + col
    down = [0] * (2 * n - 1)       # ... on each diagonal row - col + n - 1
    for col, row in enumerate(board):
        rows[row] += 1
        up[row + col] += 1
        down[row - col + n - 1] += 1

    def attacks(row: int, col: int) -> int:
        """Queens attacking square (row, col), not counting one standing on it."""
        here = 3 if board[col] == row else 0
        return rows[row] + up[row + col] + down[row - col + n - 1] - here

    for step in range(max_steps):
        attacked = [col for col in range(n) if attacks(board[col], col) > 0]
        if not attacked:
            return board, step
        col = random.choice(attacked)
        old = board[col]
        rows[old] -= 1
        up[old + col] -= 1
        down[old - col + n - 1] -= 1
        board[col] = -1                                    # lift the queen
        scores = [rows[r] + up[r + col] + down[r - col + n - 1] for r in range(n)]
        least = min(scores)
        row = random.choice([r for r in range(n) if scores[r] == least])
        board[col] = row
        rows[row] += 1
        up[row + col] += 1
        down[row - col + n - 1] += 1
    return board, max_steps
