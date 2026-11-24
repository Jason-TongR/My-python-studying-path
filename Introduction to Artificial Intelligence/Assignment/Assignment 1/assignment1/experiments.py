"""Run the experiments of the assignment on your team's instances, and print the tables for
your report:

    python experiments.py --team 7                  all the experiments
    python experiments.py --team 7 --part knapsack  only one part: pancakes, flip-cost, knapsack, coloring

The results depend on your team number, and on random choices: the generators are seeded with
your team number, so running the same code again gives the same results.
"""
import argparse
import random
import time
from collections.abc import Callable, Iterable
from typing import Any, Optional

from algorithms.bidirectional import bidirectional_search
from algorithms.genetic import evolve, rank_selection, tournament_selection
from algorithms.informed import a_star_search, greedy_search, ida_star_search, weighted_a_star_search
from algorithms.local_search import hill_climbing, local_beam_search, random_restart, stochastic_hill_climbing
from algorithms.uninformed import breadth_first_search, iterative_deepening_search, uniform_cost_search
from core.node import Node
from core.reversible import ReversibleSearchProblem
from core.search_problem import S
from problems.instances import coloring_instance, knapsack_instance, knapsack_optimum, pancake_instances
from problems.pancakes import PancakeProblem, PancakeState, flip_cost_heuristic, gap_heuristic, my_heuristic

BUDGET = 200_000   # at most this many expansions per search


class OutOfBudget(Exception):
    pass


class CountingProblem(ReversibleSearchProblem[S]):
    """Wraps a problem, and counts the states it expands: the calls to get_successors and
    get_predecessors. Stops the search after BUDGET expansions."""

    def __init__(self, problem: ReversibleSearchProblem[S]) -> None:
        self.problem = problem
        self.expanded = 0

    def get_initial_state(self) -> S:
        return self.problem.get_initial_state()

    def get_goal_state(self) -> S:
        return self.problem.get_goal_state()

    def is_goal(self, state: S) -> bool:
        return self.problem.is_goal(state)

    def count(self) -> None:
        self.expanded += 1
        if self.expanded > BUDGET:
            raise OutOfBudget()

    def get_successors(self, state: S) -> Iterable[tuple[S, str]]:
        self.count()
        return self.problem.get_successors(state)

    def get_predecessors(self, state: S) -> Iterable[tuple[S, str]]:
        self.count()
        return self.problem.get_predecessors(state)

    def get_action_cost(self, state: S, action: str, next_state: S) -> float:
        return self.problem.get_action_cost(state, action, next_state)


Search = Callable[[CountingProblem[PancakeState]], Optional[Node[PancakeState]]]


def run(name: str, search: Search, problem: PancakeProblem) -> None:
    counting = CountingProblem(problem)
    start = time.time()
    try:
        node = search(counting)
    except OutOfBudget:
        print(f"  {name:30} {'':>6} {'':>6} {'> ' + format(BUDGET, ','):>12} {time.time() - start:8.2f}")
        return
    except NotImplementedError as e:
        print(f"  {name:30} not implemented yet: {e}")
        return
    seconds = time.time() - start
    if node is None:
        print(f"  {name:30} no solution")
    else:
        print(f"  {name:30} {node.path_cost:6g} {node.depth:6} {counting.expanded:12,} {seconds:8.2f}")


def header() -> None:
    print(f"  {'algorithm':30} {'cost':>6} {'flips':>6} {'expanded':>12} {'seconds':>8}")


def pancakes(team: int) -> None:
    print("=== Pancakes, every flip costs 1")
    for size, stacks in pancake_instances(team).items():
        for stack in stacks:
            print(f"\n{size} stack: {' '.join(map(str, stack))}")
            header()
            problem = PancakeProblem(stack)
            searches: list[tuple[str, Search]] = []
            if size != "large":
                searches += [("breadth-first search", breadth_first_search)]
            if size == "small":
                searches += [("iterative deepening", iterative_deepening_search)]
            if size != "large":
                searches += [("uniform-cost search", uniform_cost_search)]
            searches += [("greedy, gap", lambda p: greedy_search(p, gap_heuristic)),
                         ("A*, gap", lambda p: a_star_search(p, gap_heuristic)),
                         ("A*, your heuristic", lambda p: a_star_search(p, my_heuristic)),
                         ("weighted A* (w = 2), gap", lambda p: weighted_a_star_search(p, gap_heuristic, 2)),
                         ("IDA*, gap", lambda p: ida_star_search(p, gap_heuristic))]
            if size != "large":
                searches += [("bidirectional search", bidirectional_search)]
            for name, search in searches:
                run(name, search, problem)


def flip_cost(team: int) -> None:
    print("=== Pancakes, flipping k pancakes costs k")
    instances = pancake_instances(team)
    for stack in instances["small"] + instances["medium"]:
        print(f"\nstack: {' '.join(map(str, stack))}")
        header()
        problem = PancakeProblem(stack, flip_cost=True)
        searches: list[tuple[str, Search]] = [
            ("uniform-cost search", uniform_cost_search),
            ("A*, gap", lambda p: a_star_search(p, gap_heuristic)),
            ("A*, flip-cost heuristic", lambda p: a_star_search(p, flip_cost_heuristic)),
            ("IDA*, flip-cost heuristic", lambda p: ida_star_search(p, flip_cost_heuristic)),
            ("bidirectional search", bidirectional_search)]
        for name, search in searches:
            run(name, search, problem)


def local_and_genetic(title: str, problem: Any, show: Callable[[Any], str], team: int) -> None:
    print(f"\n  {'algorithm':42} {'result':>24} {'seconds':>8}")
    trials: list[tuple[str, Callable[[], Any]]] = [
        ("hill climbing", lambda: hill_climbing(problem)[0]),
        ("stochastic hill climbing", lambda: stochastic_hill_climbing(problem)[0]),
        ("random restart, 30 hill climbings", lambda: random_restart(problem, hill_climbing, 30)[0]),
        ("random restart, 30 stochastic", lambda: random_restart(problem, stochastic_hill_climbing, 30)[0]),
        ("local beam search, k = 5", lambda: local_beam_search(problem, 5)[0]),
        ("local beam search, k = 20", lambda: local_beam_search(problem, 20)[0]),
        ("evolve, tournaments of 3", lambda: evolve(problem, 100, 200, tournament_selection(3), 0.2)[0]),
        ("evolve, rank selection", lambda: evolve(problem, 100, 200, rank_selection, 0.2)[0]),
    ]
    for name, trial in trials:
        random.seed(team)
        start = time.time()
        try:
            result = trial()
        except NotImplementedError as e:
            print(f"  {name:42} not implemented yet: {e}")
            continue
        print(f"  {name:42} {show(result):>24} {time.time() - start:8.2f}")


def knapsack(team: int) -> None:
    problem = knapsack_instance(team)
    optimum = knapsack_optimum(problem)
    print(f"=== Knapsack: 40 items, capacity {problem.capacity}; the optimum is {optimum}")

    def show(s: Any) -> str:
        if problem.total_weight(s) > problem.capacity:
            return "too heavy"
        return f"{problem.total_value(s)} ({100 * problem.total_value(s) / optimum:.1f}%)"
    local_and_genetic("knapsack", problem, show, team)


def coloring(team: int) -> None:
    problem = coloring_instance(team)
    print(f"=== Graph coloring: {problem.n} nodes, {len(problem.edges)} edges, {problem.k} colors")
    local_and_genetic("coloring", problem, lambda c: f"{problem.conflicts(c)} conflicts", team)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--team", type=int, required=True, help="your team number")
    parser.add_argument("--part", choices=["pancakes", "flip-cost", "knapsack", "coloring"])
    args = parser.parse_args()
    parts = {"pancakes": pancakes, "flip-cost": flip_cost, "knapsack": knapsack, "coloring": coloring}
    for name, part in parts.items():
        if args.part in (None, name):
            part(args.team)
            print()
