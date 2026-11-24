import random
from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")   # the type of the candidate solutions


class OptimizationProblem(ABC, Generic[T]):
    """A problem for local search: complete candidate solutions, each with a cost to minimize.

    Subclasses MUST implement the three abstract methods. They MAY override random_neighbor.
    """

    @abstractmethod
    def random_state(self) -> T:
        """A random candidate solution."""

    @abstractmethod
    def neighbors(self, state: T) -> list[T]:
        """The candidates that differ from state by one small change."""

    @abstractmethod
    def cost(self, state: T) -> float:
        """The cost of a candidate: lower is better."""

    def random_neighbor(self, state: T) -> T:
        """A neighbor chosen at random."""
        return random.choice(self.neighbors(state))


class GeneticProblem(ABC, Generic[T]):
    """A problem for a genetic algorithm: individuals, their fitness (to maximize), and the
    genetic operators.

    Subclasses MUST implement the four abstract methods. Operators never modify their
    arguments: they return new individuals.
    """

    @abstractmethod
    def random_individual(self) -> T:
        """A random individual, for the initial population."""

    @abstractmethod
    def fitness(self, individual: T) -> float:
        """How good an individual is: higher is better."""

    @abstractmethod
    def crossover(self, parent1: T, parent2: T) -> T:
        """A child combining two parents."""

    @abstractmethod
    def mutate(self, individual: T) -> T:
        """A copy of individual with a small random change."""
