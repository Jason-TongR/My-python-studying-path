"""N-queens as local search: one queen per column, and a move puts a queen in another row
of its column. A board is a list of rows: board[col] is the row of the queen in column col.
"""
import random

Board = list[int]


def random_board(n: int) -> Board:
    """A board with one queen in a random row of each of the n columns."""
    return [random.randrange(n) for _ in range(n)]


def attacking_pairs(board: Board) -> int:
    """The number of pairs of queens that attack each other: 0 for a solution."""
    n = len(board)
    count = 0
    for c1 in range(n):
        for c2 in range(c1 + 1, n):
            if board[c1] == board[c2] or abs(board[c1] - board[c2]) == c2 - c1:
                count += 1
    return count


def neighbors(board: Board) -> list[Board]:
    """All the boards that move one queen to another row of its column."""
    # TODO: for each column, and each row other than the queen's current row, add a copy of
    #       board with the queen of that column moved to that row (8 x 7 = 56 boards for 8 queens).
    raise NotImplementedError("neighbors")   # remove this line when you are done


def random_neighbor(board: Board) -> Board:
    """A random neighbor: one random queen moved to another random row."""
    neighbor = board.copy()
    col = random.randrange(len(board))
    neighbor[col] = random.choice([row for row in range(len(board)) if row != board[col]])
    return neighbor


def show(board: Board) -> str:
    """The board as text: Q for a queen, . for an empty square."""
    n = len(board)
    lines: list[str] = []
    for row in range(n):
        lines.append(" ".join("Q" if board[col] == row else "." for col in range(n)))
    return "\n".join(lines)
