# Lab: heuristic search

In this lab you turn uniform-cost search into best-first search, use it to build greedy
search and A*, and compare them with heuristics of your own on two problems: a map
with a lake, and the 8-puzzle.

You need Python 3.10 or later, and nothing else. Run the commands in this folder (on
some systems, type `python3` instead of `python`).

| File | What it contains | What you do |
|---|---|---|
| `search.py` | uniform-cost search (complete); best-first search, greedy search and A* | complete `best_first_search`, `greedy_search` and `a_star_search` |
| `grid.py` | a map with land, water and walls | implement `manhattan` |
| `puzzle.py` | the 8-puzzle | implement `misplaced` and `manhattan` |
| `main.py` | runs a search on the map or on the 8-puzzle | run it |

States are plain tuples here: `(row, col)` on the map, and the 9 squares of a board in
the 8-puzzle. Tuples can be dictionary keys, which is what the searches need.

## Two new pieces of Python

- **`lambda`** writes a small function inline, like Java's `(g, state) -> h(state)`:
  `lambda g, state: h(state)` takes `g` and `state`, and returns `h(state)`.
- **`heapq`** is Python's priority queue: `heapq.heappush(heap, item)` adds an item to a
  list, and `heapq.heappop(heap)` removes the smallest. Items are tuples, compared
  element by element, so the first element is the priority.

## Exercises

1. **Uniform-cost search.** Read `uniform_cost_search` in `search.py`, then run
   `python main.py grid ucs`. In the drawing, `o` and `O` mark the squares the search
   expanded, on land and on water, and `*` the route it found. Why does it expand almost
   the whole map?
2. **Best-first search.** Complete `best_first_search`: it is `uniform_cost_search` with
   one change, a state's priority is `f(g, state)` instead of `g`. Then complete
   `greedy_search` (f = h) and `a_star_search` (f = g + h), one line each, calling
   `best_first_search` with a lambda.
3. **The map.** Moving onto land costs 1 and onto water 5. Implement `manhattan` in
   `grid.py`, then run `python main.py grid greedy` and `python main.py grid astar`, and
   compare them with uniform-cost search: the cost of the route, and the number of squares
   expanded.
   - Why does greedy search cross the lake?
   - Why is the Manhattan distance admissible here? Would it still be if water cost 0.5?
4. **The 8-puzzle.** Implement `misplaced` (h1) and `manhattan` (h2) in `puzzle.py`. For
   the `easy`, `medium`, `hard` and `hardest` boards, run `ucs`, `astar-misplaced` and
   `astar-manhattan`, for example `python main.py puzzle hard astar-manhattan`, and fill
   in a table with the number of boards each one expands.
   - Which heuristic is better, and why?
   - Prove that both heuristics are admissible.
5. **If you have time.**
   - Write `weighted_a_star_search(problem, h, w)` in `search.py`, with f = g + w · h, and
     try it on the map with w = 2 and w = 5. What happens to the cost of the route and to
     the number of squares expanded?
   - Try `greedy-manhattan` on the 8-puzzle boards. How long are its solutions?
   - Run the `unsolvable` board with each algorithm. What happens? Why doesn't the
     heuristic help?
