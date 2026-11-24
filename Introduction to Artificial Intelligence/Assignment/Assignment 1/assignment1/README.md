# Introduction to Artificial Intelligence · Assignment 1

**Search, logic programming and local search**

| | |
|---|---|
| **Teams** | 3 to 5 students |
| **Submission** | Monday, November 30, 2026, 23:59, on Moodle |
| **Weight** | graded, and defended in person by every member of the team |
| **Covers** | lectures 1 to 4: search, heuristic search, logic programming, local search and genetic algorithms |
| **Workload** | about 5 to 7 days of part-time work for a team |

In this assignment you implement search algorithms that we have seen in the lectures but
not yet implemented, and variants of the ones we have; you model new problems for them; and
you compare the algorithms with experiments on problems that only your team has. Everything
builds on the framework of the lectures and labs: `SearchState`, `SearchProblem`, `Node`,
`Frontier`, and the generic algorithms.

## Getting started

You need Python 3.10 or later, with no other libraries, and SWI-Prolog 9 for part D.

```
python -m unittest                      run the tests (in this folder)
python experiments.py --team 7          run the experiments for team 7, for your report
cd prolog; swipl check.pl               check part D
```

Your **team number** is given on Moodle. Team 1 is equivalent to Group A, Team 2 to Group B, and so on. Your 
experiments run on instances generated from it, so every team has its own puzzles, items and graph.

| Folder or file | What it contains | What you do |
|---|---|---|
| `core/` | the course framework, with two new abstract classes: `ReversibleSearchProblem` and `OptimizationProblem`/`GeneticProblem` | read it; do not change it |
| `algorithms/uninformed.py` | breadth-first, depth-first, uniform-cost, depth-limited and iterative deepening search | read it |
| `algorithms/informed.py` | the best-first family and IDA* | part A |
| `algorithms/bidirectional.py` | bidirectional search | part A |
| `problems/pancakes.py` | the pancake problem | part B |
| `problems/knapsack.py`, `problems/coloring.py` | two problems for local search and genetic algorithms | part C |
| `algorithms/local_search.py`, `algorithms/genetic.py` | local search and genetic algorithms | part C |
| `prolog/pancakes.pl` | the pancake problem in Prolog | part D |
| `problems/instances.py`, `experiments.py`, `tests/` | your team's instances, the experiments, the tests | run them; do not change them |
| `REPORT.md` | the report | fill it in |

Every place where you must write code says `TODO` and, in Python, raises
`NotImplementedError` until you remove that line. Keep the names and signatures of the
functions and methods: the tests and the experiments use them. You may add helper functions,
methods and tests. We recommend you to use type hints, as in the labs.

## Part A: search algorithms (25 points)

**A1. The best-first family** (`algorithms/informed.py`). Write `best_first_search`, which
expands the node with the lowest value of an evaluation function f, and from it
`greedy_search`, `a_star_search` and `weighted_a_star_search` (f = g + w·h), one line each.

**A2. IDA\*** (`algorithms/informed.py`). Write `ida_star_search`: iterative deepening A*, a
series of depth-first searches limited by a bound on f = g + h. The first bound is the
heuristic value of the initial state; each new bound is the smallest f that exceeded the
previous one. Like `depth_limited_search`, it skips the states already on the current path.

**A3. Bidirectional search** (`algorithms/bidirectional.py`). Write `bidirectional_search`:
two breadth-first searches, one forward from the initial state and one backward from the
goal state, which expand one complete layer at a time (always the smaller one) until they
meet. It works on a `ReversibleSearchProblem`, which provides the goal state and the
predecessors of a state. The result must be a goal node whose path has the fewest possible
steps, with the real path cost.

## Part B: modeling the pancake problem (25 points)

A stack of n pancakes of sizes 1 to n must be sorted, with the smallest on top, using a
spatula: a flip of k pancakes (2 ≤ k ≤ n) reverses the order of the top k. A state is the
stack from the top down; the sorted stack is (1, 2, …, n).

**B1. The problem** (`problems/pancakes.py`). Complete `PancakeProblem`: the goal state, the
goal test, the successors (actions named `"flip k"`), the predecessors, and the action costs,
in two variants: every flip costs 1, or flipping k pancakes costs k.

**B2. The gap heuristic.** Write `gap_heuristic`: the number of pairs of adjacent pancakes
whose sizes differ by more than 1, counting the plate as a pancake of size n + 1 under the
stack. In the report, prove that it is admissible and consistent when every flip costs 1.

**B3. A heuristic of your own.** Design and write `my_heuristic`. In the report, say whether
it is admissible and whether it is consistent, with a proof or a counterexample, and compare
it with the gap heuristic in your experiments.

**B4. Flips that cost k.** When flipping k pancakes costs k, is the gap heuristic still
admissible? Write `flip_cost_heuristic`, an admissible heuristic for this variant that is
never smaller than the gap heuristic, and prove its admissibility in the report.

## Part C: local search and genetic algorithms (25 points)

Two problems implement both `OptimizationProblem` (for local search) and `GeneticProblem`
(for genetic algorithms):

- **0/1 knapsack** (`problems/knapsack.py`): choose items of greatest total value whose total
  weight fits the capacity. A candidate is a list of 0s and 1s. Its fitness is its total value
  if it fits, and minus its excess weight if it does not; its cost is minus its fitness.
- **Graph coloring** (`problems/coloring.py`): give each node one of k colors so that no edge
  joins two nodes of the same color. A candidate is a list of colors. Its cost is the number of
  conflicts (edges whose ends have the same color); its fitness is the number of edges without
  a conflict.

**C1. The problems.** Complete both classes, following the descriptions in the code.

**C2. Local search** (`algorithms/local_search.py`). Hill climbing is given. Write
`stochastic_hill_climbing`, `random_restart` and `local_beam_search`.

**C3. A genetic algorithm** (`algorithms/genetic.py`). Tournament and roulette selection are
given. Write `rank_selection`, and `evolve`: a genetic algorithm with elitism that works for
*any* `GeneticProblem`, using only its four methods. The same `evolve`, unchanged, must solve
both problems.

## Part D: logic programming (10 points)

In `prolog/pancakes.pl`, write `flip/3` (with `append/3` and `reverse/2`), `move/3`,
`solve/2` (depth-first), `solve_id/2` (iterative deepening) and `gaps/2` (the gap heuristic).
`swipl check.pl` checks them.

## The report (15 points)

Fill in `REPORT.md`: your team, the tables printed by `python experiments.py --team N` for
your team number, your proofs, and your answers to these questions.

1. **Pancakes, unit cost.** Which algorithms found optimal solutions, and why? Compare the
   numbers of states expanded. Why does iterative deepening sometimes expand fewer states than
   breadth-first search, and sometimes more?
2. **Weighted A\*.** Are its solutions within the bound you expect? Which bound, and why?
3. **Your heuristic.** What did A* with your heuristic return, compared with the gap
   heuristic? Explain the results with your analysis of B3.
4. **Pancakes, flip costs.** Compare uniform-cost search, A* with the gap heuristic and A*
   with your flip-cost heuristic. Why does bidirectional search sometimes return a more
   expensive solution in this variant?
5. **Knapsack and coloring.** Which algorithms worked best on your instances, and why? What do
   random restarts change? A beam of 5 against a beam of 20? Tournament against rank selection?
6. **Fitness.** Overweight knapsack selections get a negative fitness. Why is that useful?
   Could roulette selection be used with this fitness?
7. **Prolog.** What happens with `solve([3,1,2,4], Moves)`, and why? Why does `solve_id/2`
   terminate, and return a solution with the fewest flips? What does `flip(2, X, [1,3,2])`
   compute, and what makes that possible?

The tests check part of your work; passing them is necessary, not sufficient. The grade also
considers the correctness of the code beyond the tests, its clarity, your proofs, and the
analysis in your report. We will run your code with your team number: the numbers in your
report must be the ones it produces.

## Submission

One member of the team uploads a single file, `team-N.zip` (N being your team number, 1 for A, 
2 for B, and so on), on Moodle before **Monday, November 30, 2026, 23:59**. It contains this 
whole folder, with your code and your completed `REPORT.md`. Late submissions are not accepted, 
unless agreed in advance.

## The defense

After the submission, every team meets the lecturer for an in-person defense of about 30
minutes. **Every member** must be able to explain any part of the submission, not only their
own, to answer questions on the algorithms behind it, and to make small changes to the code on
the spot, without AI tools. The grade of each member depends on the defense: a member who
cannot explain the team's work receives a lower grade than the team, possibly zero. The
schedule of the defenses will be announced on Moodle.

## Use of AI tools

The purpose of the assignment is that you learn the algorithms by implementing them. You may
use AI assistants the way you would use a textbook or a teaching assistant: to understand a
concept, an error message or a Python feature. You may not submit code, proofs or answers that
you could not have written and explained yourselves. In the report, declare which tools you
used and for what. Remember that the defense checks exactly this.

Teams may discuss ideas, but each team writes its own code and report.
