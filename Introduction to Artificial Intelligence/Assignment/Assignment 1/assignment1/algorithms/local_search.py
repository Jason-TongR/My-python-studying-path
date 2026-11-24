"""Local search for any OptimizationProblem: hill climbing and its variants. Each function
returns the best state found and the number of moves (or steps) it made."""
import random
from collections.abc import Callable
from typing import Optional

from core.optimization import OptimizationProblem, T


def hill_climbing(problem: OptimizationProblem[T], start: Optional[T] = None) -> tuple[T, int]:
    """Steepest descent: move to the best neighbor (ties broken at random) as long as it is
    better than the current state. Starts from start, or from a random state."""
    current = problem.random_state() if start is None else start
    moves = 0
    while True:
        candidates = problem.neighbors(current)
        costs = [problem.cost(c) for c in candidates]
        least = min(costs)
        if least >= problem.cost(current):
            return current, moves
        current = random.choice([c for c, k in zip(candidates, costs) if k == least])
        moves += 1


def stochastic_hill_climbing(problem: OptimizationProblem[T], start: Optional[T] = None) -> tuple[T, int]:
    """Move to a neighbor chosen at random among those better than the current state, until
    no neighbor is better."""
    # TODO:
    raise NotImplementedError("stochastic_hill_climbing")   # remove this line when you are done


def random_restart(problem: OptimizationProblem[T],
                   search: Callable[[OptimizationProblem[T]], tuple[T, int]],
                   restarts: int) -> tuple[T, int]:
    """Run search (which starts from a random state) up to `restarts` times and keep the best
    result; stop early if a state of cost 0 is found. Returns the best state and the total
    number of moves of all the runs."""
    # TODO:
    raise NotImplementedError("random_restart")   # remove this line when you are done


def local_beam_search(problem: OptimizationProblem[T], k: int, max_steps: int = 1000) -> tuple[T, int]:
    """Local beam search: start from k random states; at each step, keep the k best states
    among all the neighbors of the current k (without duplicates). Stop when the best of them
    is no better than the best state found so far, or after max_steps steps. Returns the best
    state found and the number of steps."""
    # TODO: states may be lists, which cannot be put in a set; to remove
    #       duplicates, you can compare their tuple(...) versions.
    raise NotImplementedError("local_beam_search")   # remove this line when you are done
