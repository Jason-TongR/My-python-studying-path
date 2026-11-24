"""Game-tree search: minimax, and alpha-beta pruning with an optional depth limit."""
import math
import time
from collections.abc import Callable
from typing import TypeVar

from game import Game, Player

S = TypeVar("S")
A = TypeVar("A")


class Counter:
    """Counts the states a search visits."""

    def __init__(self) -> None:
        self.nodes = 0


def minimax(game: Game[S, A], state: S, counter: Counter) -> float:
    """The minimax value of state: the utility MAX gets if both players play perfectly."""
    counter.nodes += 1
    if game.is_terminal(state):
        return game.utility(state)
    values = [minimax(game, game.result(state, a), counter) for a in game.actions(state)]
    return max(values) if game.max_to_move(state) else min(values)


def alphabeta(game: Game[S, A], state: S, alpha: float, beta: float, counter: Counter,
              depth: int | None = None, evaluate: Callable[[S], float] | None = None) -> float:
    """The minimax value of state, computed with alpha-beta pruning.

    alpha: the best value MAX can already guarantee on the path to state;
    beta: the best value MIN can already guarantee. With a depth, the search stops after
    that many moves, and returns evaluate(state) instead of the true value."""
    counter.nodes += 1
    # TODO: like minimax, but with alpha and beta:
    #   - a terminal state: return its utility;
    #   - depth == 0 (and an evaluate function given): return evaluate(state);
    #   - MAX to move: start from -math.inf and, for each action, take the max with the value of
    #     the next state (depth - 1, or None if depth is None). As soon as the value is >= beta,
    #     return it (MIN would never let the game come here); otherwise raise alpha to the value.
    #   - MIN to move: the same, with min, math.inf, <= alpha, and lowering beta.
    raise NotImplementedError("alphabeta")   # remove this line when you are done


def best_action(game: Game[S, A], state: S, value: Callable[[S], float]) -> A:
    """The action leading to the state with the best value for the player to move."""
    choose = max if game.max_to_move(state) else min
    return choose(game.actions(state), key=lambda a: value(game.result(state, a)))


def minimax_player(game: Game[S, A]) -> Player[S, A]:
    return lambda state: best_action(game, state, lambda s: minimax(game, s, Counter()))


def alphabeta_player(game: Game[S, A], depth: int | None = None,
                     evaluate: Callable[[S], float] | None = None) -> Player[S, A]:
    """A player using alpha-beta search, to the end of the game or to a depth limit."""
    def choose(state: S) -> A:
        d = None if depth is None else depth - 1
        return best_action(game, state,
                           lambda s: alphabeta(game, s, -math.inf, math.inf, Counter(), d, evaluate))
    return choose


def iterative_deepening_player(game: Game[S, A], seconds: float,
                               evaluate: Callable[[S], float]) -> Player[S, A]:
    """A player that searches to depth 1, 2, 3, ... and plays the best move of the deepest
    search it completed. It checks the clock between searches, so it can run a little over."""
    # TODO (extra): return a function choose(state) that runs alphabeta_player(game, depth, evaluate)
    #       with depth = 1, 2, 3, ... until the time is up, and returns the move of the deepest
    #       search it completed.
    raise NotImplementedError("iterative_deepening_player")   # remove this line when you are done
