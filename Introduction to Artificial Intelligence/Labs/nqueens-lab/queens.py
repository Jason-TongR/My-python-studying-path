"""The N-queens problem: place N queens on an N x N board so that no two attack each other.

Two formulations of the same problem:

  Placing queens:  the board starts empty, and each action puts a queen on a
                   free square (one that is empty and not attacked).
  Moving queens:   all N queens start on the board, one per column, all in the
                   first row; each action moves one queen one row forward.

Rows and columns are numbered from 0 to N - 1.
"""

Position = tuple[int, int]   # (row, col) of a square


def attacks(row1: int, col1: int, row2: int, col2: int) -> bool:
    """True if queens on these two squares attack each other (same row, column or diagonal)."""
    return row1 == row2 or col1 == col2 or abs(row1 - row2) == abs(col1 - col2)


def no_attacks(positions: list[Position]) -> bool:
    """True if no two of the queens at these (row, col) positions attack each other."""
    for i in range(len(positions)):
        for j in range(i + 1, len(positions)):
            row1, col1 = positions[i]
            row2, col2 = positions[j]
            if attacks(row1, col1, row2, col2):
                return False
    return True


def board(n: int, positions: list[Position]) -> str:
    """The board as text: Q for a queen, . for an empty square."""
    lines: list[str] = []
    for row in range(n):
        squares: list[str] = []
        for col in range(n):
            squares.append("Q" if (row, col) in positions else ".")
        lines.append(" ".join(squares))
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Formulation 1: placing queens
# ---------------------------------------------------------------------------

class PlacementState:
    """Queens placed so far: a list of (row, col) positions."""

    def __init__(self, n: int, queens: list[Position] | None = None) -> None:
        self.n: int = n
        if queens is None:
            queens = []
        self.queens: list[Position] = queens

    def copy(self) -> "PlacementState":
        """A new state with the same queens. Changing the copy leaves this state unchanged."""
        return PlacementState(self.n, list(self.queens))

    def place(self, row: int, col: int) -> None:
        """Put a queen on the square (row, col)."""
        self.queens.append((row, col))

    def is_free(self, row: int, col: int) -> bool:
        """True if the square (row, col) is empty and no queen attacks it."""
        for queen_row, queen_col in self.queens:
            if attacks(row, col, queen_row, queen_col):   # also true if the square is occupied
                return False
        return True

    def __eq__(self, other: object) -> bool:
        """Like equals in Java: same queens, in any order."""
        return isinstance(other, PlacementState) and sorted(self.queens) == sorted(other.queens)

    def __str__(self) -> str:
        """Like toString in Java."""
        return board(self.n, self.queens)


class PlacementProblem:
    """N queens, placed one at a time on free squares."""

    def __init__(self, n: int) -> None:
        self.n: int = n

    def initial_state(self) -> PlacementState:
        return PlacementState(self.n)

    def is_goal(self, state: PlacementState) -> bool:
        return len(state.queens) == self.n and no_attacks(state.queens)

    def successors(self, state: PlacementState) -> list[PlacementState]:
        """The states that result from putting one more queen on a free square.

        Go through every square (row, col) of the board. For each free square,
        make a copy of state, place a queen on the copy, and add the copy to
        the result. Never change state itself: work on copies.
        """
        result: list[PlacementState] = []
        # TODO: add to result one new state for each free square
        raise NotImplementedError("PlacementProblem.successors")   # remove this line when you are done
        return result


# ---------------------------------------------------------------------------
# Formulation 2: moving queens
# ---------------------------------------------------------------------------

class MoveState:
    """All queens on the board, one per column: rows[col] is the row of the queen in column col."""

    def __init__(self, n: int, rows: list[int] | None = None) -> None:
        self.n: int = n
        if rows is None:
            rows = [0] * n          # all queens start in the first row
        self.rows: list[int] = rows

    def copy(self) -> "MoveState":
        """A new state with the queens in the same places. Changing the copy leaves this state unchanged."""
        return MoveState(self.n, list(self.rows))

    def move_forward(self, col: int) -> None:
        """Move the queen in column col one row forward."""
        self.rows[col] += 1

    def positions(self) -> list[Position]:
        """The (row, col) positions of all the queens."""
        result: list[Position] = []
        for col in range(self.n):
            result.append((self.rows[col], col))
        return result

    def __eq__(self, other: object) -> bool:
        """Like equals in Java: every queen in the same row."""
        return isinstance(other, MoveState) and self.rows == other.rows

    def __str__(self) -> str:
        """Like toString in Java."""
        return board(self.n, self.positions())


class MoveProblem:
    """N queens, one per column, starting in the first row and moving forward."""

    def __init__(self, n: int) -> None:
        self.n: int = n

    def initial_state(self) -> MoveState:
        return MoveState(self.n)

    def is_goal(self, state: MoveState) -> bool:
        return no_attacks(state.positions())

    def successors(self, state: MoveState) -> list[MoveState]:
        """The states that result from moving one queen one row forward.

        A queen can only move forward if it is not yet in the last row (row n - 1).
        Never change state itself: work on copies.
        """
        result: list[MoveState] = []
        # TODO: add to result one new state for each queen that can move forward
        raise NotImplementedError("MoveProblem.successors")   # remove this line when you are done
        return result
