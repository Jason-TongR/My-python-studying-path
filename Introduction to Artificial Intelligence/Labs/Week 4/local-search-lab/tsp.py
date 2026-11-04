"""The traveling salesman problem: visit every city once and return to the start, as
cheaply as possible. A tour is a list of city numbers, a permutation of 0, ..., n - 1.
"""
import math
import random

City = tuple[float, float]
Tour = list[int]


def random_cities(n: int, seed: int = 2026) -> list[City]:
    """n cities at random points of the unit square (always the same ones for a seed)."""
    rng = random.Random(seed)
    return [(rng.random(), rng.random()) for _ in range(n)]


def tour_length(tour: Tour, cities: list[City]) -> float:
    """The length of the closed tour, back to its first city."""
    total = 0.0
    for i in range(len(tour)):
        total += math.dist(cities[tour[i - 1]], cities[tour[i]])
    return total


def random_tour(n: int) -> Tour:
    tour = list(range(n))
    random.shuffle(tour)
    return tour


def two_opt_neighbors(tour: Tour) -> list[Tour]:
    """All the tours obtained by reversing one segment tour[i..j] (a 2-opt move)."""
    # TODO: for each i from 1 to len(tour) - 2, and each j from i + 1 to len(tour) - 1,
    #       add the tour with the segment tour[i..j] reversed (tour[i:j + 1][::-1] reverses it).
    raise NotImplementedError("two_opt_neighbors")   # remove this line when you are done


def save_svg(tour: Tour, cities: list[City], path: str, title: str = "") -> None:
    """Draw the tour in an SVG file, to open in a web browser."""
    size, margin = 600, 30

    def point(city: City) -> tuple[float, float]:
        return margin + city[0] * (size - 2 * margin), margin + (1 - city[1]) * (size - 2 * margin)

    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size + 40}" '
             f'viewBox="0 0 {size} {size + 40}" style="background:white">']
    points = " ".join(f"{x:.1f},{y:.1f}" for x, y in (point(cities[c]) for c in tour))
    parts.append(f'<polygon points="{points}" fill="none" stroke="#e8590c" stroke-width="2.5"/>')
    for city in cities:
        x, y = point(city)
        parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="#1f2328"/>')
    label = f"{title}  length {tour_length(tour, cities):.3f}".strip()
    parts.append(f'<text x="{margin}" y="{size + 25}" font-family="sans-serif" font-size="18">{label}</text>')
    parts.append("</svg>")
    with open(path, "w") as f:
        f.write("\n".join(parts))
