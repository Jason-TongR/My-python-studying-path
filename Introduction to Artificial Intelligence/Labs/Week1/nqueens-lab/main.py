"""Solve the N-queens problem with a formulation and an algorithm of your choice.

    python main.py 4                  all formulations and algorithms, with N = 4
    python main.py 6 place dfs        N = 6, placing queens, depth-first search
    python main.py 5 move bfs         N = 5, moving queens, breadth-first search

Formulations: place, move.  Algorithms: bfs, dfs.
Some runs take a very long time: stop them with Ctrl+C.
"""
# sys 用于读取命令行参数，time 用于统计搜索耗时，Any/Callable 用于标注算法注册表类型。
import sys
import time
from typing import Any, Callable

# 导入两种 N 皇后状态空间建模方式，以及通用搜索接口和两种搜索算法。
from queens import MoveProblem, PlacementProblem
from search import Problem, bfs, dfs

# 两种问题状态类型不同，因此此注册表用 Any 统一容纳它们。
# The two formulations have different state types, so the tables use Any for them.
# 名称到问题构造函数的映射；调用对应构造函数时传入棋盘边长 n。
FORMULATIONS: dict[str, Callable[[int], Problem[Any]]] = {"place": PlacementProblem, "move": MoveProblem}
# 名称到搜索函数的映射；每个函数接收问题对象并返回状态路径或 None。
ALGORITHMS: dict[str, Callable[[Problem[Any]], list[Any] | None]] = {"bfs": bfs, "dfs": dfs}


# 使用指定棋盘规模、建模方式和搜索算法运行一次求解并打印结果。
def solve(n: int, formulation: str, algorithm: str) -> None:
    # 打印本轮求解配置，便于区分连续运行的多组实验。
    print(f"--- N = {n}, {formulation}, {algorithm}")
    # 从名称表中取出问题构造函数并创建对应的问题实例。
    problem = FORMULATIONS[formulation](n)
    # 记录搜索开始时间。
    start = time.time()
    # 搜索函数可能因练习尚未实现而抛出 NotImplementedError。
    try:
        # 按名称选择算法并执行搜索。
        path = ALGORITHMS[algorithm](problem)
    # 捕获未实现异常，使其他实验配置仍可继续运行。
    except NotImplementedError as e:
        # 打印缺少实现的具体提示。
        print("not implemented yet:", e)
        # 输出空行作为不同实验结果之间的分隔。
        print()
        # 当前实验无法继续，提前返回。
        return
    # 搜索结束后用当前时间减去起始时间，得到耗时秒数。
    seconds = time.time() - start
    # path 为 None 时表示算法没有找到解。
    if path is None:
        print(f"no solution ({seconds:.2f} seconds)")
    # 找到路径时报告动作数和耗时，并打印路径最后一个状态（最终棋盘）。
    else:
        print(f"solution with {len(path) - 1} actions ({seconds:.2f} seconds):")
        print(path[-1])
    # 每轮结果后加空行，提升终端输出可读性。
    print()


# 仅在直接运行 main.py 时解析参数并启动实验；导入本模块时不自动求解。
if __name__ == "__main__":
    # 第一个参数是棋盘大小；未提供时默认使用 4 皇后。
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    # 第二个参数指定一种建模；未提供时测试 place 和 move 两种方式。
    formulations = [sys.argv[2]] if len(sys.argv) > 2 else ["place", "move"]
    # 第三个参数指定一种算法；未提供时测试 BFS 与 DFS。
    algorithms = [sys.argv[3]] if len(sys.argv) > 3 else ["bfs", "dfs"]
    # 对所有选定的建模方式和算法组合逐一运行求解。
    for formulation in formulations:
        # 对当前建模方式，依次运行每一种指定算法。
        for algorithm in algorithms:
            solve(n, formulation, algorithm)
