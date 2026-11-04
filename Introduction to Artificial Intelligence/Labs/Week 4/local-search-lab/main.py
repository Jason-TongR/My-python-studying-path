"""Run the lab's experiments.

    python main.py queens hill               one run of steepest hill climbing on 8 queens
    python main.py queens stats              success rates of the hill-climbing variants
    python main.py queens restart            random-restart hill climbing, until a solution
    python main.py queens ga                 a genetic algorithm on 8 queens
    python main.py queens minconflicts 1000  min-conflicts on 1,000 queens
    python main.py tsp hill                  2-opt hill climbing on 30 cities: random.svg, hill.svg
    python main.py tsp ga                    a genetic algorithm on 30 cities: ga.svg

Open the .svg files in a web browser. Every run is random: run them several times.
"""
import sys
import time
from collections.abc import Callable

from genetic import (genetic_algorithm, mutate_queens, one_point_crossover, order_crossover,
                     reverse_mutation, tournament_selection)
from local_search import (first_choice_hill_climbing, hill_climbing, hill_climbing_sideways,
                          min_conflicts_queens, random_restart)
from queens import Board, attacking_pairs, neighbors, random_board, random_neighbor, show
from tsp import random_cities, random_tour, save_svg, tour_length, two_opt_neighbors

# Settings of the genetic algorithms: change them and see what happens.
POPULATION = 100
TOURNAMENT_SIZE = 3
GENERATIONS = 500
QUEENS_MUTATION_RATE = 0.2
TSP_MUTATION_RATE = 0.3
CITIES = 30


def queens_hill() -> None:
    start = random_board(8)
    print(show(start), f"\nstart: {attacking_pairs(start)} attacking pairs\n")
    end, moves = hill_climbing(start, neighbors, attacking_pairs)
    print(show(end), f"\nafter {moves} moves: {attacking_pairs(end)} attacking pairs")


def queens_stats(runs: int = 1000) -> None:
    variants: list[tuple[str, Callable[[Board], tuple[Board, int]]]] = [
        ("steepest", lambda b: hill_climbing(b, neighbors, attacking_pairs)),
        ("sideways (100)", lambda b: hill_climbing_sideways(b, neighbors, attacking_pairs, 100)),
        ("first choice", lambda b: first_choice_hill_climbing(b, random_neighbor, attacking_pairs, 100)),
    ]
    for name, search in variants:
        try:
            solved, moves = 0, 0
            for _ in range(runs):
                board, m = search(random_board(8))
                if attacking_pairs(board) == 0:
                    solved += 1
                    moves += m
            average = moves / solved if solved else 0
            print(f"{name:15} solves {100 * solved / runs:5.1f}% of the boards, in {average:.1f} moves on average")
        except NotImplementedError as e:
            print(f"{name:15} not implemented yet: {e}")
    try:
        trials, total_runs, total_moves = 200, 0, 0
        for _ in range(trials):
            board, r, m = random_restart(lambda: random_board(8),
                                         lambda b: hill_climbing(b, neighbors, attacking_pairs),
                                         attacking_pairs, 10000)
            total_runs += r
            total_moves += m
        print(f"{'random restart':15} needs {total_runs / trials:.1f} runs and {total_moves / trials:.1f} moves on average")
    except NotImplementedError as e:
        print(f"{'random restart':15} not implemented yet: {e}")


def queens_restart() -> None:
    board, runs, moves = random_restart(lambda: random_board(8),
                                        lambda b: hill_climbing(b, neighbors, attacking_pairs),
                                        attacking_pairs, 10000)
    print(show(board), f"\n{attacking_pairs(board)} attacking pairs, after {runs} runs and {moves} moves in total")


def queens_ga() -> None:
    population = [random_board(8) for _ in range(POPULATION)]
    best, generations, history = genetic_algorithm(
        population, lambda b: 28 - attacking_pairs(b), tournament_selection(TOURNAMENT_SIZE),
        one_point_crossover, mutate_queens, QUEENS_MUTATION_RATE, GENERATIONS, elite=1, target=28)
    for g in range(0, len(history), 10):
        print(f"generation {g:3}: best fitness {history[g][0]:.0f}, average {history[g][1]:.1f}")
    print(show(best), f"\nfitness {28 - attacking_pairs(best)} of 28, after {generations} generations")


def queens_minconflicts(n: int) -> None:
    start = time.time()
    board, steps = min_conflicts_queens(random_board(n), 100000)
    seconds = time.time() - start
    if n <= 20:
        print(show(board))
    solved = (len(set(board)) == n and len({r + c for c, r in enumerate(board)}) == n
              and len({r - c for c, r in enumerate(board)}) == n)
    print(f"{n} queens: {'solved' if solved else 'not solved'} in {steps} steps ({seconds:.2f} seconds)")


def tsp_hill() -> None:
    cities = random_cities(CITIES)
    start = random_tour(CITIES)
    save_svg(start, cities, "random.svg", "a random tour")
    began = time.time()
    tour, moves = hill_climbing(start, two_opt_neighbors, lambda t: tour_length(t, cities))
    seconds = time.time() - began
    save_svg(tour, cities, "hill.svg", "2-opt hill climbing")
    print(f"random tour: length {tour_length(start, cities):.3f}  (random.svg)")
    print(f"after {moves} moves of 2-opt hill climbing: length {tour_length(tour, cities):.3f}  "
          f"(hill.svg, {seconds:.2f} seconds)")


def tsp_ga() -> None:
    cities = random_cities(CITIES)
    population = [random_tour(CITIES) for _ in range(POPULATION)]
    best, generations, history = genetic_algorithm(
        population, lambda t: -tour_length(t, cities), tournament_selection(TOURNAMENT_SIZE),
        order_crossover, reverse_mutation, TSP_MUTATION_RATE, GENERATIONS, elite=2)
    for g in range(0, len(history), 50):
        print(f"generation {g:3}: best length {-history[g][0]:.3f}, average {-history[g][1]:.3f}")
    save_svg(best, cities, "ga.svg", "genetic algorithm")
    print(f"best tour after {generations} generations: length {tour_length(best, cities):.3f}  (ga.svg)")


def main(args: list[str]) -> None:
    commands = {("queens", "hill"): queens_hill, ("queens", "stats"): queens_stats,
                ("queens", "restart"): queens_restart, ("queens", "ga"): queens_ga,
                ("tsp", "hill"): tsp_hill, ("tsp", "ga"): tsp_ga}
    if len(args) == 3 and args[:2] == ["queens", "minconflicts"]:
        queens_minconflicts(int(args[2]))
    elif len(args) == 2 and (args[0], args[1]) in commands:
        commands[(args[0], args[1])]()
    else:
        print(__doc__)


if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except NotImplementedError as e:
        print("not implemented yet:", e)
