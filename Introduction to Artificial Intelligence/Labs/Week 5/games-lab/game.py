"""Two-player, zero-sum games with perfect information, and players for them.

MAX is the player who moves first, and MIN the other one. Utilities are always given
from MAX's point of view: MAX wants them high, and MIN wants them low.
"""
import random
from collections.abc import Callable
from typing import Protocol, TypeVar

S = TypeVar("S")   # the type of the states
A = TypeVar("A")   # the type of the actions


class Game(Protocol[S, A]):
    """What a game-playing search needs from a game."""

    def initial_state(self) -> S: ...

    def max_to_move(self, state: S) -> bool:
        """True if it is MAX's turn in state."""
        ...

    def actions(self, state: S) -> list[A]: ...

    def result(self, state: S, action: A) -> S: ...

    def is_terminal(self, state: S) -> bool: ...

    def utility(self, state: S) -> float:
        """The value of a terminal state, for MAX."""
        ...

    def show(self, state: S) -> str: ...


Player = Callable[[S], A]   # a player chooses an action in a state


def random_player(game: Game[S, A]) -> Player[S, A]:
    """A player that chooses its moves at random."""
    return lambda state: random.choice(game.actions(state))


def human_player(game: Game[S, int]) -> Player[S, int]:
    """A player that asks for its moves on the keyboard."""
    def choose(state: S) -> int:
        legal = game.actions(state)
        while True:
            answer = input(f"your move {sorted(legal)}: ")
            if answer.strip().isdigit() and int(answer) in legal:
                return int(answer)
            print("not a legal move")
    return choose


def play(game: Game[S, A], max_player: Player[S, A], min_player: Player[S, A],
         start: S | None = None, verbose: bool = True) -> float:
    """Play a game from start (or the initial state) and return its utility for MAX."""
    state = game.initial_state() if start is None else start
    while not game.is_terminal(state):
        if verbose:
            print(game.show(state), "\n")
        player = max_player if game.max_to_move(state) else min_player
        state = game.result(state, player(state))
    if verbose:
        print(game.show(state), "\n")
    return game.utility(state)
