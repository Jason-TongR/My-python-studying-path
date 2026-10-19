# Lab: N-queens with breadth-first and depth-first search

Place N queens on an N × N board so that no two attack each other. In this lab you
solve this problem with breadth-first search (BFS) and depth-first search (DFS), using
two different formulations of the problem, and compare how they behave.

You need Python 3.10 or later, and nothing else. Run the commands in this folder (on some systems,
type `python3` instead of `python`).

| File | What it contains | What you do |
|---|---|---|
| `jugs.py` | BFS and DFS for the water jug problem | read it: it is your reference |
| `queens.py` | the N-queens states and problems, in two formulations | implement two `successors` methods |
| `search.py` | BFS (complete) and DFS (to complete), for any problem | complete `dfs_from` |
| `main.py` | runs one formulation with one algorithm, for a given N | run it |

## Python for Java programmers

- Blocks are defined by indentation, not by braces.
- `self` is Java's `this`, written explicitly as the first parameter of every method.
- `__init__` is the constructor, `__eq__` is `equals`, and `__str__` is `toString`.
- `[]` is an empty list. `items.append(x)` adds `x` at the end, `items[-1]` is the last
  element, and `a + b` is a new list with the elements of `a` followed by those of `b`.
- `(row, col)` is a tuple: a pair that cannot be modified.
- `for x in items:` loops over a list, and `range(n)` is 0, 1, …, n − 1.
- `None` is Java's `null`.
- Type hints such as `def place(self, row: int, col: int) -> None` declare types,
  as in Java. `list[int]` is a list of integers, and `X | None` means "an `X`, or
  `None`". Python does not check them when it runs your program, but the type
  checker mypy does: `pip install mypy`, then `mypy --strict .` in this folder.
  Give your own code type hints too.

## Two formulations

- **Placing queens.** The board starts empty. An action puts a queen on a free square:
  a square that is empty and not attacked by any queen already on the board. The goal is
  to have N queens on the board.
- **Moving queens.** All N queens start on the board, one per column, all in the first
  row. An action moves one queen one row forward. The goal is a board where no two
  queens attack each other.

In both, a search returns a path: the list of states from the initial state to a goal.

## Exercises

1. **Warm-up.** Run `python jugs.py` and read `jugs.py`.
   - Why does `dfs` need a depth limit there?
   - Change `depth_limit` at the end of the file to 6, then to 8. Which solutions do you
     get, and why are they different from the one found by BFS?
2. **Placing queens.** Implement `successors` in `PlacementProblem` (in `queens.py`).
   Test it with `python main.py 4 place bfs`.
3. **Depth-first search.** Complete `dfs_from` in `search.py`, following its TODO
   comments. Test it with `python main.py 4 place dfs`.
4. **Moving queens.** Implement `successors` in `MoveProblem`. Test it with
   `python main.py 4 move`, which runs both algorithms.
5. **Experiments.** Run each formulation with each algorithm for N = 4, 5, 6 and 8, one
   at a time, for example `python main.py 6 place dfs`. Stop any run that takes more
   than a minute with Ctrl+C.
   - Fill in a table: which combinations find a solution, and how long do they take?
   - How many actions does a solution take in each formulation? Why?
   - Can the same board be reached by different sequences of actions? In which
     formulation does this happen more? What does it cost a search that never checks
     for repeated states?
   - Which algorithm suits each formulation better, and why?
