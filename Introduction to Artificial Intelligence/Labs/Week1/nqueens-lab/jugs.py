"""The water jug problem: with jugs of 5 and 3 liters, measure exactly 4 liters.

A state is a pair (x, y): the liters in the 5-liter jug and in the 3-liter jug.
This is reference code: breadth-first search and depth-first search, written
directly for this problem. There are no costs, and no check for repeated states.

Run it with:  python jugs.py
"""

# 中文概括：通过 5 升和 3 升水壶的装满、倒空和互倒操作，量出恰好 4 升水。
# 导入双端队列，广度优先搜索会把它当作先进先出的队列使用。
from collections import deque

# 定义状态类型：x 是 5 升壶中的水量，y 是 3 升壶中的水量。
JugState = tuple[int, int]   # (liters in the 5-liter jug, liters in the 3-liter jug)


# 判断某个状态是否已经达到目标：任意一个壶中恰有 4 升即可。
def is_goal(state: JugState) -> bool:
    """True if one of the jugs holds exactly 4 liters."""
    # 将二元组拆成两个水壶当前的水量。
    x, y = state
    # 返回两个壶中是否有一个正好装了 4 升。
    return x == 4 or y == 4


# 计算从当前状态执行一次操作后，所有不同的可达状态。
def successors(state: JugState) -> list[JugState]:
    """The states reachable from state with one move."""
    # 拆出两个壶当前的水量。
    x, y = state
    # 计算从 5 升壶倒入 3 升壶的最大水量：不能超过源壶现有水，也不能超过目标壶剩余空间。
    pour12 = min(x, 3 - y)    # liters poured from the 5-liter jug into the 3-liter jug
    # 计算从 3 升壶倒入 5 升壶的最大水量，依据同样的“源水量”和“目标空位”限制。
    pour21 = min(y, 5 - x)    # liters poured from the 3-liter jug into the 5-liter jug
    # 列出灌满、倒空，以及两个方向倒水这六种操作的结果。
    candidates = [
        (5, y),                     # 将 5 升壶装满，3 升壶水量保持不变
        (x, 3),                     # 将 3 升壶装满，5 升壶水量保持不变
        (0, y),                     # 倒空 5 升壶，3 升壶水量保持不变
        (x, 0),                     # 倒空 3 升壶，5 升壶水量保持不变
        (x - pour12, y + pour12),   # 从 5 升壶向 3 升壶倒入 pour12 升
        (x + pour21, y - pour21),   # 从 3 升壶向 5 升壶倒入 pour21 升
    ]
    # result 将过滤掉不会改变状态的操作。
    result: list[JugState] = []
    # 逐个检查每种操作的结果。
    for candidate in candidates:
        # 如果操作后的状态与原状态不同，说明它确实改变了水量。
        if candidate != state:      # leave out moves that change nothing
            # 将有效后继状态保留在结果列表中。
            result.append(candidate)
    # 返回所有有效后继状态。
    return result


# 使用广度优先搜索寻找最少操作数的解；若找不到则返回 None。
def bfs(start: JugState) -> list[JugState] | None:
    """Breadth-first search. Returns the list of states from start to a goal, or None."""
    # 队列中每个元素是一条从起点开始的完整路径。
    queue: deque[list[JugState]] = deque()   # a queue, like Java's ArrayDeque
    # 初始路径只包含起始状态。
    queue.append([start])       # each element of the queue is a path: a list of states
    # 队列非空时，仍有尚未扩展的路径。
    while queue:                # while the queue is not empty
        # 取出最早加入队列的路径，因此按路径长度逐层探索。
        path = queue.popleft()  # take the oldest path in the queue
        # 路径最后一个状态是当前正在检查的状态。
        state = path[-1]        # the last state of the path
        # 如果当前状态是目标，当前路径就是一条解；BFS 保证它是最短解。
        if is_goal(state):
            return path
        # 否则为当前状态的每个后继建立一条新路径并放入队尾。
        for next_state in successors(state):
            queue.append(path + [next_state])
    # 队列耗尽仍未找到目标，表示没有找到解。
    return None


# 使用深度优先搜索，但最多只允许递归探索 depth_limit 步。
def dfs(state: JugState, depth_limit: int) -> list[JugState] | None:
    """Depth-first search, at most depth_limit moves deep.

    Returns the list of states from state to a goal, or None. Without the depth
    limit, this search could go around in circles forever: for example, filling
    the 5-liter jug, emptying it, filling it again, and so on.
    """
    # 若当前状态已是目标，路径只需包含当前状态。
    if is_goal(state):
        return [state]
    # 深度预算用完且尚未到达目标，当前分支失败。
    if depth_limit == 0:
        return None
    # 按后继状态的顺序逐个深入搜索。
    for next_state in successors(state):
        # 递归时将剩余深度减一，因为已经执行了一步操作。
        path = dfs(next_state, depth_limit - 1)
        # 递归找到解时，在其路径前加上当前状态并向上返回。
        if path is not None:
            return [state] + path
    # 所有后继分支都失败，当前状态也无法在限制内到达目标。
    return None


# 按统一格式打印算法名称以及求出的路径或失败信息。
def show(name: str, path: list[JugState] | None) -> None:
    # None 表示没有找到路径。
    if path is None:
        print(name + ": no solution")
    # 否则路径长度减一就是执行的操作数，再把各个状态用箭头连接。
    else:
        print(name + ":", len(path) - 1, "moves:", " -> ".join(str(s) for s in path))


# 只有直接运行本文件时才执行下面的演示；被其他文件导入时不会自动运行。
if __name__ == "__main__":
    # 从两个水壶都为空的状态运行广度优先搜索并打印结果。
    show("Breadth-first search", bfs((0, 0)))
    # 设置深度优先搜索最多探索的操作数，可修改它观察深度限制的影响。
    depth_limit = 10   # change this number to try other limits
    # 运行带深度限制的深度优先搜索并打印结果。
    show(f"Depth-first search, depth limit {depth_limit}", dfs((0, 0), depth_limit))
