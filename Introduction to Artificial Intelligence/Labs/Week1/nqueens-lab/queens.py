"""The N-queens problem: place N queens on an N x N board so that no two attack each other.

Two formulations of the same problem:

  Placing queens:  the board starts empty, and each action puts a queen on a
                   free square (one that is empty and not attacked).
  Moving queens:   all N queens start on the board, one per column, all in the
                   first row; each action moves one queen one row forward.

Rows and columns are numbered from 0 to N - 1.
"""

# 中文概括：在 N×N 棋盘上放置 N 个皇后，要求任意两个皇后都不能互相攻击。

# 用一个二元整数元组表示格子坐标，顺序是（行号，列号），编号从 0 开始。
Position = tuple[int, int]   # (row, col) of a square


# 判断两个格子上的皇后是否处于同一行、同一列或同一条对角线上。
def attacks(row1: int, col1: int, row2: int, col2: int) -> bool:
    """True if queens on these two squares attack each other (same row, column or diagonal)."""
    # 对角线条件是行差的绝对值等于列差的绝对值；任一条件成立即会攻击。
    return row1 == row2 or col1 == col2 or abs(row1 - row2) == abs(col1 - col2)


# 检查列表中每一对皇后；只有所有不同皇后都不互相攻击时才返回 True。
def no_attacks(positions: list[Position]) -> bool:
    """True if no two of the queens at these (row, col) positions attack each other."""
    # i 选取一只皇后作为当前比较对象。
    for i in range(len(positions)):
        # j 从 i+1 开始，避免重复比较同一对，也避免皇后与自身比较。
        for j in range(i + 1, len(positions)):
            # 分别拆出这两只皇后的行号和列号，便于传给攻击判断函数。
            row1, col1 = positions[i]
            row2, col2 = positions[j]
            # 一旦找到相互攻击的一对，整个布局就不合法，可以立即结束。
            if attacks(row1, col1, row2, col2):
                return False
    # 所有皇后对都检查完毕且没有冲突，布局合法。
    return True


# 把棋盘状态转换为可打印的多行文本，皇后用 Q 表示，空格用点表示。
def board(n: int, positions: list[Position]) -> str:
    """The board as text: Q for a queen, . for an empty square."""
    # lines 保存每一整行棋盘的文本。
    lines: list[str] = []
    # 逐行构造棋盘。
    for row in range(n):
        # squares 临时保存当前行每一列对应的字符。
        squares: list[str] = []
        # 逐列检查当前位置是否在皇后坐标集合中。
        for col in range(n):
            # 有皇后就添加 Q，否则添加表示空格的点号。
            squares.append("Q" if (row, col) in positions else ".")
        # 用空格分隔当前行的格子，并将整行添加到结果列表。
        lines.append(" ".join(squares))
    # 用换行符连接每一行，得到完整棋盘字符串。
    return "\n".join(lines)


# 下面是第一种建模：状态表示目前已经放置的皇后。
# ---------------------------------------------------------------------------
# Formulation 1: placing queens
# ---------------------------------------------------------------------------

class PlacementState:
    """Queens placed so far: a list of (row, col) positions."""

    # 初始化一个放置状态；queens 未提供时，棋盘上暂时没有皇后。
    def __init__(self, n: int, queens: list[Position] | None = None) -> None:
        # 保存棋盘边长，行列范围均为 0 到 n-1。
        self.n: int = n
        # None 表示调用者没有提供初始皇后列表，此时创建空列表。
        if queens is None:
            queens = []
        # 保存当前状态的皇后位置；列表中的每项是（行，列）。
        self.queens: list[Position] = queens

    # 复制当前状态，避免搜索扩展新状态时修改原状态。
    def copy(self) -> "PlacementState":
        """A new state with the same queens. Changing the copy leaves this state unchanged."""
        # list(...) 创建新列表，但元组坐标本身不可变，因此浅拷贝足够。
        return PlacementState(self.n, list(self.queens))

    # 在当前状态中追加一只皇后的位置。
    def place(self, row: int, col: int) -> None:
        """Put a queen on the square (row, col)."""
        # 将行列坐标组合成元组并添加到皇后列表。
        self.queens.append((row, col))

    # 判断指定格子是否空闲：既不能已有皇后，也不能被已有皇后攻击。
    def is_free(self, row: int, col: int) -> bool:
        """True if the square (row, col) is empty and no queen attacks it."""
        # 逐个检查已放置的皇后。
        for queen_row, queen_col in self.queens:
            if attacks(row, col, queen_row, queen_col):   # also true if the square is occupied
                # 只要会被任何一只已放置皇后攻击，该格子就不可用。
                return False
        # 没有发现冲突，因此该格子可放置新皇后。
        return True

    # 定义状态相等的规则，供搜索算法或测试比较两个状态。
    def __eq__(self, other: object) -> bool:
        """Like equals in Java: same queens, in any order."""
        # 类型必须相同；排序后比较使皇后列表的排列顺序不影响状态相等性。
        return isinstance(other, PlacementState) and sorted(self.queens) == sorted(other.queens)

    # 定义 print(state) 时显示的内容。
    def __str__(self) -> str:
        """Like toString in Java."""
        # 复用 board 函数生成棋盘文本。
        return board(self.n, self.queens)


class PlacementProblem:
    """N queens, placed one at a time on free squares."""

    # 保存问题规模 N。
    def __init__(self, n: int) -> None:
        self.n: int = n

    # 创建搜索的起点：棋盘上还没有放置皇后。
    def initial_state(self) -> PlacementState:
        # 初始时不放置任何皇后。
        return PlacementState(self.n)

    # 目标状态必须放满 N 只皇后，并且所有皇后互不攻击。
    def is_goal(self, state: PlacementState) -> bool:
        # 必须恰好放置 n 只皇后，并且它们之间没有攻击关系。
        return len(state.queens) == self.n and no_attacks(state.queens)

    # 生成所有通过再放置一只皇后可到达的后继状态。
    def successors(self, state: PlacementState) -> list[PlacementState]:
        """The states that result from putting one more queen on a free square.

        Go through every square (row, col) of the board. For each free square,
        make a copy of state, place a queen on the copy, and add the copy to
        the result. Never change state itself: work on copies.
        """
        # result 收集新状态；当前模板尚未实现如何遍历并放置皇后。
        result: list[PlacementState] = []
        # TODO: add to result one new state for each free square
        # 占位异常表示后继状态生成尚未实现；练习要求遍历空格并复制、放置皇后。
        raise NotImplementedError("PlacementProblem.successors")   # remove this line when you are done
        # 实现完成后返回所有新状态；当前这行因上面的异常不会执行。
        return result


# 下面是第二种建模：每列固定一只皇后，每步让其中一只向下一行移动。
# ---------------------------------------------------------------------------
# Formulation 2: moving queens
# ---------------------------------------------------------------------------

class MoveState:
    """All queens on the board, one per column: rows[col] is the row of the queen in column col."""

    # 初始化移动状态；rows[col] 保存第 col 列皇后的当前行号。
    def __init__(self, n: int, rows: list[int] | None = None) -> None:
        # 保存棋盘边长。
        self.n: int = n
        # 未给定行号时，所有皇后都从第 0 行开始，每一列一只。
        if rows is None:
            rows = [0] * n          # all queens start in the first row
        # 保存每列皇后的行号列表。
        self.rows: list[int] = rows

    # 复制状态，后继状态的修改不会影响当前状态。
    def copy(self) -> "MoveState":
        """A new state with the queens in the same places. Changing the copy leaves this state unchanged."""
        # 新建行号列表，并与相同的棋盘边长一起传给新状态。
        return MoveState(self.n, list(self.rows))

    # 将指定列的皇后向前移动一行（行号增加 1）。
    def move_forward(self, col: int) -> None:
        """Move the queen in column col one row forward."""
        # 只改变第 col 列皇后的行号。
        self.rows[col] += 1

    # 将紧凑的行号列表转换为通用的（行，列）坐标列表。
    def positions(self) -> list[Position]:
        """The (row, col) positions of all the queens."""
        # result 保存转换后的皇后坐标。
        result: list[Position] = []
        # 每列恰好一只皇后，列号就是当前循环的 col。
        for col in range(self.n):
            # rows[col] 是该列皇后的行号。
            result.append((self.rows[col], col))
        # 返回全部皇后的位置。
        return result

    # 两个移动状态相等，当且仅当每一列皇后所在的行都相同。
    def __eq__(self, other: object) -> bool:
        """Like equals in Java: every queen in the same row."""
        # 先检查类型，再比较行号列表。
        return isinstance(other, MoveState) and self.rows == other.rows

    # 将状态转换成便于阅读的棋盘字符串。
    def __str__(self) -> str:
        """Like toString in Java."""
        # positions 转换坐标后交给共享的棋盘打印函数。
        return board(self.n, self.positions())


class MoveProblem:
    """N queens, one per column, starting in the first row and moving forward."""

    # 初始化 N 皇后移动问题。
    def __init__(self, n: int) -> None:
        self.n: int = n

    # 所有皇后都在第一行的初始状态。
    def initial_state(self) -> MoveState:
        # 构造默认状态时，所有列的皇后都处在第 0 行。
        return MoveState(self.n)

    # 目标是所有皇后互不攻击；本模型中每列天然只有一只皇后。
    def is_goal(self, state: MoveState) -> bool:
        # 检查状态中全部皇后是否互不攻击。
        return no_attacks(state.positions())

    # 生成让任意一只尚未到达末行的皇后前进一格后得到的状态。
    def successors(self, state: MoveState) -> list[MoveState]:
        """The states that result from moving one queen one row forward.

        A queen can only move forward if it is not yet in the last row (row n - 1).
        Never change state itself: work on copies.
        """
        # result 用于收集合法移动产生的新状态；模板目前尚未实现循环逻辑。
        result: list[MoveState] = []
        # TODO: add to result one new state for each queen that can move forward
        # 占位异常提示后继生成未完成；需只移动尚未到达末行的皇后。
        raise NotImplementedError("MoveProblem.successors")   # remove this line when you are done
        # 实现完成后返回每次移动产生的新状态；当前不会执行到此处。
        return result
