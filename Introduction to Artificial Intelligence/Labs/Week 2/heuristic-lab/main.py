"""Run the lab's searches on the map or on the 8-puzzle.

    python main.py grid ucs                    the map, with uniform-cost search
    python main.py grid greedy                 the map, with greedy search (Manhattan distance)
    python main.py grid astar                  the map, with A* (Manhattan distance)
    python main.py puzzle hard ucs             the hard 8-puzzle board, with uniform-cost search
    python main.py puzzle hard astar-misplaced
    python main.py puzzle hard astar-manhattan
    python main.py puzzle hard greedy-manhattan

Boards: easy, medium, hard, hardest, unsolvable.
"""
import sys
import time

from grid import GridProblem
from puzzle import Board, PuzzleProblem, show
from search import a_star_search, greedy_search, uniform_cost_search

BOARDS: dict[str, Board] = {
    "easy": (2, 3, 6, 1, 0, 4, 7, 5, 8),         # 8 moves from the goal
    "medium": (3, 7, 5, 4, 0, 1, 8, 2, 6),       # 16 moves
    "hard": (3, 6, 1, 5, 0, 2, 8, 4, 7),         # 22 moves
    "hardest": (4, 6, 7, 3, 5, 8, 0, 2, 1),      # 26 moves
    "unsolvable": (1, 2, 3, 4, 5, 6, 8, 7, 0),
}


def run_grid(algorithm: str) -> None:
    problem = GridProblem()
    start = time.time()
    if algorithm == "ucs":
        result = uniform_cost_search(problem)
    elif algorithm == "greedy":
        result = greedy_search(problem, problem.manhattan)
    elif algorithm == "astar":
        result = a_star_search(problem, problem.manhattan)
    else:
        print("unknown algorithm:", algorithm)
        return
    seconds = time.time() - start
    print(problem.draw(result.path, result.expanded))
    print("* route    o expanded land    O expanded water    ~ water    # wall")
    print(f"route cost {result.cost:g}, {len(result.expanded)} squares expanded ({seconds:.2f} seconds)")


def run_puzzle(board_name: str, algorithm: str) -> None:
    problem = PuzzleProblem(BOARDS[board_name])
    print(show(problem.start))
    start = time.time()
    if algorithm == "ucs":
        result = uniform_cost_search(problem)
    elif algorithm == "astar-misplaced":
        result = a_star_search(problem, problem.misplaced)
    elif algorithm == "astar-manhattan":
        result = a_star_search(problem, problem.manhattan)
    elif algorithm == "greedy-manhattan":
        result = greedy_search(problem, problem.manhattan)
    else:
        print("unknown algorithm:", algorithm)
        return
    seconds = time.time() - start
    if result.path is None:
        print("no solution", end="")
    else:
        print(f"solution with {len(result.path) - 1} moves", end="")
    print(f", {len(result.expanded):,} boards expanded ({seconds:.2f} seconds)")


if __name__ == "__main__":
    args = sys.argv[1:]
    try:
        if len(args) == 2 and args[0] == "grid":
            run_grid(args[1])
        elif len(args) == 3 and args[0] == "puzzle" and args[1] in BOARDS:
            run_puzzle(args[1], args[2])
        else:
            print(__doc__)
    except NotImplementedError as e:
        print("not implemented yet:", e)
