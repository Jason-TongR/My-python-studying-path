"""Nim with one pile: each player in turn takes 1, 2 or 3 sticks, and whoever takes the
last stick wins. A state is (sticks left, True if it is MAX's turn).
"""

NimState = tuple[int, bool]


class Nim:
    def __init__(self, sticks: int) -> None:
        self.sticks = sticks

    def initial_state(self) -> NimState:
        return (self.sticks, True)

    def max_to_move(self, state: NimState) -> bool:
        return state[1]

    def actions(self, state: NimState) -> list[int]:
        """How many sticks can be taken: 1, 2 or 3, but not more than are left."""
        return [take for take in (1, 2, 3) if take <= state[0]]

    def result(self, state: NimState, action: int) -> NimState:
        return (state[0] - action, not state[1])

    def is_terminal(self, state: NimState) -> bool:
        return state[0] == 0

    def utility(self, state: NimState) -> float:
        """The player who took the last stick won: that is the player NOT to move now."""
        return -1 if state[1] else 1

    def show(self, state: NimState) -> str:
        return f"{'|' * state[0]}  ({state[0]} sticks, {'MAX' if state[1] else 'MIN'} to move)"
