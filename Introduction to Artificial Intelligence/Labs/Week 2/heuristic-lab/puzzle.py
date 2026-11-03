"""The 8-puzzle: slide the tiles until they are in order, with the blank last.

A board is a tuple of 9 numbers, row by row; 0 is the blank. Every move costs 1.
"""

Board = tuple[int, ...]

GOAL: Board = (1, 2, 3,
               4, 5, 6,
               7, 8, 0)


class PuzzleProblem:
    """Reach the goal board from a start board."""

    def __init__(self, start: Board) -> None:
        self.start = start

    def initial_state(self) -> Board:
        return self.start

    def is_goal(self, state: Board) -> bool:
        return state == GOAL

    def successors(self, state: Board) -> list[tuple[Board, float]]:
        """The boards reachable by moving the blank up, down, left or right."""
        blank = state.index(0)
        row, col = blank // 3, blank % 3
        result: list[tuple[Board, float]] = []
        for d_row, d_col in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            new_row, new_col = row + d_row, col + d_col
            if 0 <= new_row < 3 and 0 <= new_col < 3:
                squares = list(state)
                other = new_row * 3 + new_col
                squares[blank], squares[other] = squares[other], squares[blank]
                result.append((tuple(squares), 1.0))
        return result

    def misplaced(self, state: Board) -> float:
        """h1: the number of tiles that are not on their goal square (the blank does not count)."""
        # TODO
        raise NotImplementedError("PuzzleProblem.misplaced")   # remove this line when you are done

    def manhattan(self, state: Board) -> float:
        """h2: the sum of the Manhattan distances of the tiles to their goal squares.

        Square i of a board is in row i // 3 and column i % 3, and GOAL.index(tile)
        is the goal square of a tile.
        """
        # TODO
        raise NotImplementedError("PuzzleProblem.manhattan")   # remove this line when you are done


def show(board: Board) -> str:
    """The board as three lines of text, with . for the blank."""
    lines: list[str] = []
    for row in range(3):
        lines.append(" ".join(str(t) if t != 0 else "." for t in board[row * 3:row * 3 + 3]))
    return "\n".join(lines)
