from collections import defaultdict
import math
import operator
from typing import Dict, List, NamedTuple, Set, Tuple

from colorama import Fore, Back, Style
import pytest


class Asteroid(NamedTuple):
    x: int
    y: int

    def manhattan_distance(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)


class AsteroidMap:
    def __init__(self, asteroids: List[Asteroid]):
        self._asteroids: Set[Asteroid] = set(coordinates for coordinates in asteroids)
        self.x_min = 0
        self.x_max = 10  # max(x for x, y in asteroids)
        self.y_min = 0
        self.y_max = 9  # max(y for x, y in asteroids)

    def __repr__(self):
        return repr(self._asteroids)

    def __len__(self):
        return len(self._asteroids)

    def __contains__(self, key):
        return key in self._asteroids

    def __iter__(self):
        return iter(self._asteroids)

    def draw(
        self, current_asteroid: Asteroid, visible_asteroids: Set[Asteroid]
    ) -> None:
        """WORK IN PROGRESS"""
        grid = []

        # blank spaces
        for _ in range(self.y_max + 1):
            grid.append([Style.DIM + "."] * (self.x_max + 1))
        # asteroids
        for asteroid in self._asteroids:
            grid[asteroid.y][asteroid.x] = "#"
        for asteroid in visible_asteroids:
            grid[current_asteroid.y][current_asteroid.x] = Fore.MAGENTA + "#"
        grid[current_asteroid.y][current_asteroid.x] = Fore.GREEN + "#"

        grid_output = ""
        for line in grid:
            grid_output += "".join(line) + "\n"
        return print(grid_output)

    def find_closest_astroids(self, asteroid) -> Dict[int, List[Asteroid]]:
        asteroid_distances = defaultdict(list)

        all_other_asteroids = self._asteroids.copy()
        all_other_asteroids.remove(asteroid)
        for other_asteroid in all_other_asteroids:
            distance = asteroid.manhattan_distance(other_asteroid)
            asteroid_distances[distance].append(other_asteroid)

        return asteroid_distances

    def astroids_observed(self, asteroid: Asteroid):
        asteroids_observed = set()
        unobservable_points = set()

        asteroid_distances = self.find_closest_astroids(asteroid)
        sorted_distances = sorted(asteroid_distances.keys())
        for distance in sorted_distances:
            asteroids_at_x_distance = asteroid_distances[distance]
            for other_asteroid in asteroids_at_x_distance:
                if other_asteroid in unobservable_points:
                    continue
                asteroids_observed.add(other_asteroid)

                step_x = other_asteroid.x - asteroid.x
                step_y = other_asteroid.y - asteroid.y

                if step_x == 0:
                    step_y = int(step_y / abs(step_y))
                elif step_y == 0:
                    step_x = int(step_x / abs(step_x))
                else:
                    gcd = math.gcd(step_x, step_y)
                    if gcd != 1:
                        step_x = int(step_x / gcd)
                        step_y = int(step_y / gcd)

                num_steps = 0
                while True:
                    num_steps += 1

                    new_x = other_asteroid.x + (step_x * num_steps)
                    new_y = other_asteroid.y + (step_y * num_steps)

                    if not self._within_map_boundary(new_x, new_y):
                        break
                    unobservable_points.add(Asteroid(new_x, new_y))

        return asteroids_observed

    def degrees_map(self, asteroid: Asteroid):
        asteroids_degrees = defaultdict(list)

        all_other_asteroids = self._asteroids.copy()
        all_other_asteroids.remove(asteroid)
        for other_asteroid in all_other_asteroids:
            distance = asteroid.manhattan_distance(other_asteroid)
            rise = asteroid.y - other_asteroid.y
            run = other_asteroid.x - asteroid.x

            if run == 0:
                if rise > 0:
                    degrees = 0
                elif rise < 0:
                    degrees = 180
                else:
                    raise ValueError("should not get here")
            elif run > 0:
                slope = rise / run
                degrees = 90 - math.degrees(math.atan(slope))
            elif run < 0:
                slope = rise / run
                degrees = 270 - math.degrees(math.atan(slope))

            asteroids_degrees[degrees].append((distance, other_asteroid))

        # sort by degrees then sort by distance
        return {
            degrees: sorted(asteroids_degrees[degrees], reverse=True)
            for degrees in sorted(asteroids_degrees.keys())
        }

    def _within_map_boundary(self, x, y) -> bool:
        # TODO not sure why i need to offset my x_mas and y_max... but it works
        return (self.x_min <= x <= (self.x_max + 100)) and (
            self.y_min <= y <= (self.y_max + 100)
        )


def find_all_asteroids(grid: List[str]) -> List[Asteroid]:
    asteroids = []
    for y_index, line in enumerate(grid):
        for x_index, value in enumerate(line):
            if value == "#":
                asteroids.append(Asteroid(x_index, y_index))
    return asteroids


def clear_asteroids(degrees_map, num_destroy):
    destruction_path = []
    counter = 0
    for degrees, asteroids in degrees_map.items():
        if asteroids:
            counter += 1
            destruction_path.append((counter, asteroids.pop()))

            if counter == num_destroy:
                break
    return destruction_path


LINE_OF_SIGHT_INPUT = """#.........
...#......
...#..a...
.####....a
..#.c.b...
.....c....
..efd.c.gb
.......c..
....f...c.
...e..d..c""".split()


TEST_INPUT1 = """.#..#
.....
#####
....#
...##""".split()

TEST_INPUT2 = """......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####""".split()

TEST_INPUT3 = """#.#...#.#.
.###....#.
.#....#...
##.#.#.#.#
....#.#.#.
.##..###.#
..#...##..
..##....##
......#...
.####.###.""".split()

TEST_INPUT4 = """.#..#..###
####.###.#
....###.#.
..###.##.#
##.##.#.#.
....###..#
..#.#..#.#
#..#.#.###
.##...##.#
.....#.#..""".split()

TEST_INPUT5 = """.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##""".split()


@pytest.mark.parametrize(
    "astroids_grid, best, num_asteroids",
    [
        (TEST_INPUT1, Asteroid(3, 4), 8),
        (TEST_INPUT2, Asteroid(5, 8), 33),
        (TEST_INPUT3, Asteroid(1, 2), 35),
        (TEST_INPUT4, Asteroid(6, 3), 41),
        (TEST_INPUT5, Asteroid(11, 13), 210),
    ],
)
def test_find_asteroid_that_can_observe_the_most(astroids_grid, best, num_asteroids):
    asteroids = find_all_asteroids(astroids_grid)
    asteroids_map = AsteroidMap(asteroids)

    observed_mapping = {}
    for asteroid in asteroids_map:
        observed_mapping[asteroid] = len(asteroids_map.astroids_observed(asteroid))

    assert observed_mapping[best] == num_asteroids
    assert max(observed_mapping.items(), key=operator.itemgetter(1))[0] == best


@pytest.mark.parametrize(
    "astroids_grid, best, num_200", [(TEST_INPUT5, Asteroid(11, 13), Asteroid(8, 2))]
)
def test_find_200th_asteroid_to_blow_up(astroids_grid, best, num_200):
    asteroids = find_all_asteroids(astroids_grid)
    asteroids_map = AsteroidMap(asteroids)

    degrees_map = asteroids_map.degrees_map(best)
    result = clear_asteroids(degrees_map, 200)
    assert result[-1][1][1] == num_200


if __name__ == "__main__":
    with open("2019/data/day10_input.txt", "r") as f:
        grid = []
        for line in f.readlines():
            grid.append(line.strip())

    asteroids = find_all_asteroids(grid)
    asteroids_map = AsteroidMap(asteroids)
    observed_mapping = {}
    for asteroid in asteroids_map:
        observed_mapping[asteroid] = len(asteroids_map.astroids_observed(asteroid))
    asteroid, num_observed = max(observed_mapping.items(), key=operator.itemgetter(1))
    print(f"Asteroid with best view: {asteroid}")
    print(f"Max observable asteroids: {num_observed}")

    degrees_map = asteroids_map.degrees_map(asteroid)
    result = clear_asteroids(degrees_map, 200)[-1][1][1]
    print(f"Calculated field: {result.x * 100 + result.y}")
