"""Solve the N-queens problem with a formulation and an algorithm of your choice.

    python main.py 4                  all formulations and algorithms, with N = 4
    python main.py 6 place dfs        N = 6, placing queens, depth-first search
    python main.py 5 move bfs         N = 5, moving queens, breadth-first search

Formulations: place, move.  Algorithms: bfs, dfs.
Some runs take a very long time: stop them with Ctrl+C.
"""
import sys
import time
from typing import Any, Callable

from queens import MoveProblem, PlacementProblem
from search import Problem, bfs, dfs

# The two formulations have different state types, so the tables use Any for them.
FORMULATIONS: dict[str, Callable[[int], Problem[Any]]] = {"place": PlacementProblem, "move": MoveProblem}
ALGORITHMS: dict[str, Callable[[Problem[Any]], list[Any] | None]] = {"bfs": bfs, "dfs": dfs}


def solve(n: int, formulation: str, algorithm: str) -> None:
    print(f"--- N = {n}, {formulation}, {algorithm}")
    problem = FORMULATIONS[formulation](n)
    start = time.time()
    try:
        path = ALGORITHMS[algorithm](problem)
    except NotImplementedError as e:
        print("not implemented yet:", e)
        print()
        return
    seconds = time.time() - start
    if path is None:
        print(f"no solution ({seconds:.2f} seconds)")
    else:
        print(f"solution with {len(path) - 1} actions ({seconds:.2f} seconds):")
        print(path[-1])
    print()


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    formulations = [sys.argv[2]] if len(sys.argv) > 2 else ["place", "move"]
    algorithms = [sys.argv[3]] if len(sys.argv) > 3 else ["bfs", "dfs"]
    for formulation in formulations:
        for algorithm in algorithms:
            solve(n, formulation, algorithm)
