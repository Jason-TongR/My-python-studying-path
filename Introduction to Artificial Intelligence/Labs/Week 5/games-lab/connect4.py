"""Connect Four: X (MAX) moves first; a move drops a piece into a column, where it falls to
the lowest empty square; four in a row (in any direction) wins. A state is a tuple of
42 squares, row by row from the top, each "X", "O" or " ". An action is a column, 0 to 6.
"""

Board = tuple[str, ...]
ROWS, COLUMNS = 6, 7
WIN = 10000   # a win for MAX is worth more than WIN; evaluations must stay between -WIN and WIN


def _lines() -> list[tuple[int, int, int, int]]:
    """All the groups of four squares in a row: horizontal, vertical and diagonal."""
    lines = []
    for r in range(ROWS):
        for c in range(COLUMNS):
            for dr, dc in ((0, 1), (1, 0), (1, 1), (1, -1)):
                cells = [(r + k * dr, c + k * dc) for k in range(4)]
                if all(0 <= rr < ROWS and 0 <= cc < COLUMNS for rr, cc in cells):
                    a, b, cc_, d = (rr * COLUMNS + cc for rr, cc in cells)
                    lines.append((a, b, cc_, d))
    return lines


LINES = _lines()   # 69 groups of four


def winner(board: Board) -> str | None:
    for a, b, c, d in LINES:
        if board[a] != " " and board[a] == board[b] == board[c] == board[d]:
            return board[a]
    return None


class ConnectFour:
    def __init__(self, order: list[int] | None = None) -> None:
        """order: the order in which columns are tried; by default the center first."""
        self.order = order if order is not None else [3, 2, 4, 1, 5, 0, 6]

    def initial_state(self) -> Board:
        return (" ",) * (ROWS * COLUMNS)

    def max_to_move(self, state: Board) -> bool:
        return state.count("X") == state.count("O")

    def actions(self, state: Board) -> list[int]:
        return [col for col in self.order if state[col] == " "]   # the top square is free

    def result(self, state: Board, action: int) -> Board:
        mark = "X" if self.max_to_move(state) else "O"
        row = max(r for r in range(ROWS) if state[r * COLUMNS + action] == " ")
        i = row * COLUMNS + action
        return state[:i] + (mark,) + state[i + 1:]

    def is_terminal(self, state: Board) -> bool:
        return winner(state) is not None or " " not in state

    def utility(self, state: Board) -> float:
        """A quicker win is better: a win is worth WIN plus the number of empty squares left."""
        bonus = WIN + state.count(" ")
        return {"X": bonus, "O": -bonus, None: 0}[winner(state)]

    def show(self, state: Board) -> str:
        rows = [" ".join(state[r * COLUMNS + c] if state[r * COLUMNS + c] != " " else "."
                         for c in range(COLUMNS)) for r in range(ROWS)]
        return "\n".join(rows + [" ".join(str(c) for c in range(COLUMNS))])


def center_evaluation(state: Board) -> float:
    """A simple evaluation: pieces in the three central columns, X's minus O's."""
    score = 0
    for r in range(ROWS):
        for c in (2, 3, 4):
            piece = state[r * COLUMNS + c]
            score += 1 if piece == "X" else -1 if piece == "O" else 0
    return score


def evaluation(state: Board) -> float:
    """Your evaluation of a position: how good it is for X (MAX)."""
    # TODO: return a number between -WIN and WIN, higher when X is doing better and lower when O is.
    #       center_evaluation above is an example. Ideas: LINES lists the 69 groups of four squares
    #       in a row; what does a group with three X and no O say about the position?
    raise NotImplementedError("evaluation")   # remove this line when you are done
