"""A map with land, water and walls: find the cheapest route from S to G.

Moving to a neighboring square (up, down, left or right) costs 1 onto land and
5 onto water. Walls (#) cannot be crossed.
"""

GridState = tuple[int, int]   # (row, col)

MAP = """
#########################################
#.......................................#
#..........~~~~~~~~~~~~~~~~~~...........#
#.........~~~~~~~~~~~~~~~~~~~~..........#
#........~~~~~~~~~~~~~~~~~~~~~~.........#
#........~~~~~~~~~~~~~~~~~~~~~~.........#
#S.......~~~~~~~~~~~~~~~~~~~~~~.......G.#
#........~~~~~~~~~~~~~~~~~~~~~~.........#
#........~~~~~~~~~~~~~~~~~~~~~~.........#
#.........~~~~~~~~~~~~~~~~~~~~..........#
#..........~~~~~~~~~~~~~~~~~~...........#
#.......................................#
#########################################
"""

STEP_COST = {".": 1.0, "S": 1.0, "G": 1.0, "~": 5.0}   # the cost of moving onto a square


class GridProblem:
    """The cheapest route from S to G on a map."""

    def __init__(self, text: str = MAP) -> None:
        self.rows: list[str] = text.strip("\n").split("\n")
        self.start: GridState = self.find("S")
        self.goal: GridState = self.find("G")

    def find(self, symbol: str) -> GridState:
        """The position of the first square holding symbol."""
        for row, line in enumerate(self.rows):
            col = line.find(symbol)
            if col >= 0:
                return (row, col)
        raise ValueError(f"no {symbol} on the map")

    def initial_state(self) -> GridState:
        return self.start

    def is_goal(self, state: GridState) -> bool:
        return state == self.goal

    def successors(self, state: GridState) -> list[tuple[GridState, float]]:
        """The neighboring squares that are not walls, each with the cost of moving onto it."""
        row, col = state
        result: list[tuple[GridState, float]] = []
        for d_row, d_col in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            symbol = self.rows[row + d_row][col + d_col]   # the map is surrounded by walls
            if symbol != "#":
                result.append(((row + d_row, col + d_col), STEP_COST[symbol]))
        return result

    def manhattan(self, state: GridState) -> float:
        """The Manhattan distance from state to the goal: |row difference| + |column difference|."""
        # TODO
        raise NotImplementedError("GridProblem.manhattan")   # remove this line when you are done

    def draw(self, path: list[GridState] | None, expanded: list[GridState]) -> str:
        """The map, with the expanded squares (o on land, O on water) and the path (*)."""
        on_path = set(path or [])
        was_expanded = set(expanded)
        lines: list[str] = []
        for row, line in enumerate(self.rows):
            squares: list[str] = []
            for col, symbol in enumerate(line):
                if symbol in ".~" and (row, col) in on_path:
                    squares.append("*")
                elif symbol in ".~" and (row, col) in was_expanded:
                    squares.append("o" if symbol == "." else "O")
                else:
                    squares.append(symbol)
            lines.append("".join(squares))
        return "\n".join(lines)
