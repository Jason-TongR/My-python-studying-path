# Lab: local search and genetic algorithms

In this lab you write local search algorithms and a genetic algorithm from scratch, in
plain Python, and try them on 8-queens and on the traveling salesman problem.

You need Python 3.10 or later, and nothing else. Run the commands in this folder (on
some systems, type `python3` instead of `python`):

```
python main.py queens hill               one run of steepest hill climbing on 8 queens
python main.py queens stats              success rates of the hill-climbing variants
python main.py queens restart            random-restart hill climbing, until a solution
python main.py queens ga                 a genetic algorithm on 8 queens
python main.py queens minconflicts 1000  min-conflicts on 1,000 queens
python main.py tsp hill                  2-opt hill climbing on 30 cities: random.svg, hill.svg
python main.py tsp ga                    a genetic algorithm on 30 cities: ga.svg
```

Open the `.svg` files in a web browser. Every run is random, so run things several times.

| File | What it contains | What you do |
|---|---|---|
| `queens.py` | 8-queens as local search | write `neighbors` |
| `tsp.py` | the traveling salesman problem, and drawing tours | write `two_opt_neighbors` |
| `local_search.py` | hill climbing (complete), its variants, min-conflicts | write `first_choice_hill_climbing` and `random_restart` |
| `genetic.py` | a genetic algorithm (complete), selection, crossover, mutation | write `tournament_selection`, `one_point_crossover` and `mutate_queens` |
| `main.py` | runs the experiments; its settings are at the top | run it, and change the settings |

A board is a list of rows, one per column: `board[col]` is the row of the queen in column
`col`. A tour is a list of city numbers. Local search minimizes a cost (the attacking
pairs, the length of the tour); the genetic algorithm maximizes a fitness (28 minus the
attacking pairs; minus the length of the tour).

## Exercises

1. **Hill climbing on 8-queens.** Write `neighbors` in `queens.py`. Run
   `python main.py queens hill` a few times, then `python main.py queens stats`.
   - How often does steepest hill climbing solve the problem?
   - What do sideways moves change, and at what price?
2. **First choice and random restarts.** Write `first_choice_hill_climbing` and
   `random_restart` in `local_search.py`. Run `python main.py queens stats` again, and
   `python main.py queens restart`.
   - How many runs does random restart need, on average? Why is that close to 1/p, where p
     is the success rate of a single run?
3. **The traveling salesman.** Write `two_opt_neighbors` in `tsp.py`, run
   `python main.py tsp hill`, and open `random.svg` and `hill.svg`.
   - Run it several times: do you always get the same tour? Why not?
4. **A genetic algorithm for 8-queens.** Write `tournament_selection`,
   `one_point_crossover` and `mutate_queens` in `genetic.py`, then run
   `python main.py queens ga` several times.
   - How often does it find a solution within 500 generations?
   - Change the settings at the top of `main.py`. What happens with
     `QUEENS_MUTATION_RATE = 0`? With a population of 20, or of 300?
5. **If you have time.**
   - Write `order_crossover` in `genetic.py`, run `python main.py tsp ga`, and open
     `ga.svg`. Compare the genetic algorithm with 2-opt hill climbing: the length of the
     tours, and the time each takes.
   - On the TSP, try `TOURNAMENT_SIZE = 2` and `10`. What happens to the average of the
     population, and to the best tour?
   - Run min-conflicts on 1,000 and on 10,000 queens.
