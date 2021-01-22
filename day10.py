import unittest
from math import atan2, dist, pi
from collections import defaultdict

# Returns a list of (x, y) coords for each asteroid.
def get_asteroid_coords(asteroid_map):
    rows = range(len(asteroid_map))
    cols = range(len(asteroid_map[0]))
    return [(x, y) for y in rows for x in cols if asteroid_map[y][x] == "#"]

def get_angle(start, end):
    # We have +x right, +y down and need +x up, +y right (90 deg CCW rotation):
    # => [0, -1; 1, 0] * [dx; dy] = [-dy; dx]
    # See https://en.wikipedia.org/wiki/Rotation_matrix#Direction
    return atan2(end[0] - start[0], -(end[1] - start[1])) % (2*pi)

def get_num_detections(asteroids, start):
    return(len(set(get_angle(start, b) for b in asteroids if b != start)))

def get_most_detected(asteroid_map):
    asteroids = get_asteroid_coords(asteroid_map)
    all_detections = [get_num_detections(asteroids, a) for a in asteroids]
    i, max_detections = max(enumerate(all_detections), key=lambda d: d[1])
    return asteroids[i], max_detections

def get_vaporized(asteroid_map, station):
    rest = [a for a in get_asteroid_coords(asteroid_map) if a != station]
    rest.sort(key=lambda asteroid: dist(station, asteroid))
    # For each asteroid, find how many block its view of the station.
    num_blocking = {a: sum(get_angle(station, a) == get_angle(station, b)
                    for b in rest[:i]) for i, a in enumerate(rest)}
    # Return all unblocked asteroids sorted by angle, then more blocked.
    return sorted(rest, key=lambda a: (num_blocking[a], get_angle(station, a)))

def main():
    with open("day10.txt") as input_file:
        asteroid_map = input_file.read().split()
    station, detections = get_most_detected(asteroid_map)
    print("Part one solution: {}".format(detections))
    x, y = get_vaporized(asteroid_map, station)[199]
    print("Part two solution: {}".format(x*100 + y))

if __name__ == "__main__":
    main()

class AsteroidDetectorTest(unittest.TestCase):
    def test_small_detected(self):
        asteroid_map = [
                ".#..#",
                ".....",
                "#####",
                "....#",
                "...##"]
        station, detections = get_most_detected(asteroid_map)
        self.assertEqual(station, (3, 4))
        self.assertEqual(detections, 8)

    def test_medium_detected(self):
        asteroid_map = [
            "......#.#.",
            "#..#.#....",
            "..#######.",
            ".#.#.###..",
            ".#..#.....",
            "..#....#.#",
            "#..#....#.",
            ".##.#..###",
            "##...#..#.",
            ".#....####"]
        station, detections = get_most_detected(asteroid_map)
        self.assertEqual(station, (5, 8))
        self.assertEqual(detections, 33)

    def test_medium_detected2(self):
        asteroid_map = [
            "#.#...#.#.",
            ".###....#.",
            ".#....#...",
            "##.#.#.#.#",
            "....#.#.#.",
            ".##..###.#",
            "..#...##..",
            "..##....##",
            "......#...",
            ".####.###."]
        station, detections = get_most_detected(asteroid_map)
        self.assertEqual(station, (1, 2))
        self.assertEqual(detections, 35)

    def test_small_vaporized(self):
        asteroid_map = [
            ".#....#####...#..",
            "##...##.#####..##",
            "##...#...#.#####.",
            "..#.....#...###..",
            "..#.#.....#....##"]
        station = (8, 3)
        vaporized = get_vaporized(asteroid_map, station)
        self.assertEqual(vaporized[0], (8, 1))
        self.assertEqual(vaporized[1], (9, 0))
        self.assertEqual(vaporized[2], (9, 1))
        self.assertEqual(vaporized[3], (10, 0))
        self.assertEqual(vaporized[4], (9, 2))
        self.assertEqual(vaporized[8], (15, 1))

    def test_large_vaporized(self):
        asteroid_map = [
            ".#..##.###...#######",
            "##.############..##.",
            ".#.######.########.#",
            ".###.#######.####.#.",
            "#####.##.#.##.###.##",
            "..#####..#.#########",
            "####################",
            "#.####....###.#.#.##",
            "##.#################",
            "#####.##.###..####..",
            "..######..##.#######",
            "####.##.####...##..#",
            ".#####..#.######.###",
            "##...#.##########...",
            "#.##########.#######",
            ".####.#.###.###.#.##",
            "....##.##.###..#####",
            ".#.#.###########.###",
            "#.#.#.#####.####.###",
            "###.##.####.##.#..##"]
        station, detections = get_most_detected(asteroid_map)
        self.assertEqual(detections, 210)
        self.assertEqual(station, (11, 13))
        vaporized = get_vaporized(asteroid_map, station)
        self.assertEqual(vaporized[199], (8, 2))
