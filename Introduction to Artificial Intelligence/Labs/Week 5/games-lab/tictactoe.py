"""Tic-tac-toe: X (MAX) moves first. A state is a tuple of 9 squares, row by row, each
"X", "O" or " ". An action is the number (0 to 8) of an empty square.
"""

Board = tuple[str, ...]

LINES = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]


def winner(board: Board) -> str | None:
    """"X" or "O" if that player has three in a line, else None."""
    for a, b, c in LINES:
        if board[a] != " " and board[a] == board[b] == board[c]:
            return board[a]
    return None


class TicTacToe:
    def __init__(self, order: list[int] | None = None) -> None:
        """order: the order in which the squares are tried (by default 0, 1, ..., 8)."""
        self.order = order if order is not None else list(range(9))

    def initial_state(self) -> Board:
        return (" ",) * 9

    def max_to_move(self, state: Board) -> bool:
        return state.count("X") == state.count("O")

    def actions(self, state: Board) -> list[int]:
        return [square for square in self.order if state[square] == " "]

    def result(self, state: Board, action: int) -> Board:
        mark = "X" if self.max_to_move(state) else "O"
        return state[:action] + (mark,) + state[action + 1:]

    def is_terminal(self, state: Board) -> bool:
        return winner(state) is not None or " " not in state

    def utility(self, state: Board) -> float:
        return {"X": 1, "O": -1, None: 0}[winner(state)]

    def show(self, state: Board) -> str:
        """The board, with the number of each empty square."""
        cells = [state[i] if state[i] != " " else str(i) for i in range(9)]
        return "\n".join(" " + " | ".join(cells[r * 3:r * 3 + 3]) for r in range(3))
