"""Breadth-first search and depth-first search.

Both work with any problem object that has three methods, described by the
Problem protocol below. Both return the path found, as a list of states from the
initial state to a goal, or None if there is no solution. Neither checks for
repeated states.
"""
# deque 提供 BFS 所需的高效队列；Protocol 和 TypeVar 用于描述通用问题接口与状态类型。
from collections import deque
from typing import Protocol, TypeVar

# S 是泛型状态类型占位符，使搜索算法能用于不同问题的状态对象。
S = TypeVar("S")   # the type of the states: like the type parameter S in Java's Problem<S>


# Protocol 描述搜索算法需要问题对象提供哪些方法，不要求具体继承此类。
class Problem(Protocol[S]):
    """What a search needs from a problem, like a Java interface Problem<S>.

    A class does not need to declare that it implements Problem: it is enough
    that it has these three methods, with these types.
    """

    # 返回搜索起点，类型 S 由具体问题决定。
    def initial_state(self) -> S:
        """The state where the search starts."""
        ...

    # 返回从给定状态执行一次操作后可到达的状态列表。
    def successors(self, state: S) -> list[S]:
        """The states reachable from state with one action."""
        ...

    # 判断给定状态是否满足问题的目标条件。
    def is_goal(self, state: S) -> bool:
        """True if state is a solution."""
        ...


# BFS 使用队列逐层扩展路径，适用于每步代价相同且希望找最少步数解的情形。
def bfs(problem: Problem[S]) -> list[S] | None:
    """Breadth-first search, with a queue of paths."""
    # 队列元素是一条完整路径，路径末尾是待扩展的状态。
    queue: deque[list[S]] = deque()              # a queue, like Java's ArrayDeque
    # 将只含初始状态的路径放入队列。
    queue.append([problem.initial_state()])      # each element of the queue is a path
    # 只要还有路径等待处理，就继续搜索。
    while queue:                                 # while the queue is not empty
        # FIFO 出队保证先处理较浅的路径。
        path = queue.popleft()                   # take the oldest path in the queue
        # 当前状态是路径最后一个元素。
        state = path[-1]                         # the last state of the path
        # 找到目标后立即返回从起点到目标的整条路径。
        if problem.is_goal(state):
            return path
        # 对每个后继状态都复制出一条扩展后的路径，并加入队尾等待检查。
        for next_state in problem.successors(state):
            queue.append(path + [next_state])
    # 所有可搜索路径都处理完仍无目标，返回 None。
    return None


# DFS 从初始状态开始调用递归辅助函数。
def dfs(problem: Problem[S]) -> list[S] | None:
    """Depth-first search, written recursively."""
    # 将问题对象和初始状态交给 dfs_from 完成递归搜索。
    return dfs_from(problem, problem.initial_state())


# 从指定状态递归执行深度优先搜索，并返回从该状态到目标的路径。
def dfs_from(problem: Problem[S], state: S) -> list[S] | None:
    """Search depth-first from state. Returns a path from state to a goal, or None.

    Look at dfs in jugs.py: it is the same idea, without the depth limit.
    """
    # 以下仍是练习模板：先检查目标，再递归探索后继，最后报告失败。
    # TODO 1: if state is a goal, return the path [state].
    # TODO 2: for each successor next_state of state:
    #             search recursively from next_state;
    #             if that search found a path, return [state] + that path.
    # TODO 3: if no successor leads to a goal, return None.
    # 尚未实现的占位异常会在真正调用本函数时提醒开发者完成 TODO。
    raise NotImplementedError("dfs_from")   # remove this line when you are done
