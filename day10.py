import unittest
from math import atan2, pi
from collections import defaultdict

# Returns a list of (x, y) coords for each asteroid.
def get_asteroid_coords(asteroid_map):
    rows = range(len(asteroid_map))
    cols = range(len(asteroid_map[0]))
    return [(x, y) for y in rows for x in cols if asteroid_map[y][x] == "#"]

def get_most_detected(asteroid_map):
    asteroids = get_asteroid_coords(asteroid_map)
    # { asteroid: set of unique angles }
    detected_angles = {asteroid: set() for asteroid in asteroids}

    most_so_far = 0
    detections = {} # { coords: detections }
    for start in asteroids:
        for end in [x for x in asteroids if x != start]:
            angle = atan2(end[1] - start[1], end[0] - start[0])
            detected_angles[start].add(angle)
        detections[start] = len(detected_angles[start])
    max_coords = max(detections, key=detections.get)
    return max_coords, detections[max_coords]

def get_vaporized(asteroid_map, station):
    asteroids = get_asteroid_coords(asteroid_map)
    vaporized = []
    angle_map = defaultdict(list) # [ { angle: [distance, (row, col)] } ]
    for other in [x for x in asteroids if x != station]:
        dx = other[0] - station[0]
        dy = other[1] - station[1]
        # dy grows as we move in -y (since y=0 is at the top), so flip sign
        # angle is counterclockwise from +x axis, so:
        #  1) subtract pi/2 to get counterclockwise angle from +y axis
        #  1) subtract angle from 2*pi to get clockwise angle from +y axis
        #  3) take modulus to wrap angle to [0, 2*pi], so +y axis is 0
        angle = (2*pi - (atan2(-dy, dx) - pi/2)) % (2*pi)
        # Store Manhattan distance, a simple way to find closer asteroids along
        # the same angle from the station.
        distance = abs(dx) + abs(dy)
        angle_map[angle].append((distance, other))

    while angle_map:
        # Sort so we move through angles clockwise from +y axis.
        for angle, value in sorted(angle_map.items()):
            distance, coords = min(angle_map[angle]) # min distance coords
            angle_map[angle].remove((distance, coords))
            vaporized.append(coords)
        angle_map = {key: val for key, val in angle_map.items() if len(val)}

    return vaporized

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