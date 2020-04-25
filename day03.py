#!/usr/bin/python3

import unittest

def get_point_steps(segments):
    DX = dict(zip("LRUD", [-1, +1, 0, 0]))
    DY = dict(zip("LRUD", [0, 0, +1, -1]))
    x = 0
    y = 0
    steps = 0
    point_steps = {}
    for segment in segments:
        if not segment:
            continue
        direction = segment[0]
        distance = int(segment[1:])
        if direction not in "LRUD":
            raise ValueError("Invalid segment direction {}.".format(direction))
        if distance < 1:
            raise ValueError("Invalid segment distance {}.".format(distance))
        for _ in range(distance):
            x += DX[direction]
            y += DY[direction]
            steps += 1
            if (x, y) not in point_steps:
                point_steps[(x, y)] = steps
    return point_steps

def get_intersection_point_steps(wire1, wire2): 
    segments1, segments2 = [x.split(",") for x in [wire1, wire2]]
    point_steps1 = get_point_steps(segments1)
    point_steps2 = get_point_steps(segments2)
    cross_points = point_steps1.keys() & point_steps2.keys()
    return {pt:[point_steps1[pt], point_steps2[pt]] for pt in cross_points}

def get_manhattan_distance(wire1, wire2):
    point_steps = get_intersection_point_steps(wire1, wire2)
    if not point_steps:
        return -1
    return min([abs(x) + abs(y) for x, y in point_steps.keys()])

def get_fewest_steps(wire1, wire2):
    point_steps = get_intersection_point_steps(wire1, wire2)
    if not point_steps:
        return -1
    return min([steps[0] + steps[1] for steps in point_steps.values()])

def main():
    with open("day03.txt") as input_file:
        wire1, wire2 = input_file.read().splitlines()
        print(get_manhattan_distance(wire1, wire2))
        print(get_fewest_steps(wire1, wire2))

if __name__ == '__main__':
    main()

class TestWireIntersections(unittest.TestCase):
    def test_get_manhattan_distance(self):
        self.assertEqual(get_manhattan_distance("", ""), -1)
        self.assertEqual(get_manhattan_distance("R1", "L1"), -1)
        self.assertRaises(ValueError, get_manhattan_distance, "X1", "R1")
        self.assertRaises(ValueError, get_manhattan_distance, "U1", "R-1")
        self.assertEqual(get_manhattan_distance(
                         "R8,U5,L5,D3", "U7,R6,D4,L4"), 6)
        self.assertEqual(get_manhattan_distance(
                         "R75,D30,R83,U83,L12,D49,R71,U7,L72",
                         "U62,R66,U55,R34,D71,R55,D58,R83"),
                         159)
        self.assertEqual(get_manhattan_distance(
                         "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51",
                         "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7"),
                         135)

    def test_get_fewest_steps(self):
        self.assertEqual(get_fewest_steps("", ""), -1)
        self.assertEqual(get_fewest_steps("R1", "L1"), -1)
        self.assertRaises(ValueError, get_fewest_steps, "X1", "R1")
        self.assertRaises(ValueError, get_fewest_steps, "U1", "R-1")
        self.assertEqual(get_fewest_steps(
                         "R8,U5,L5,D3", "U7,R6,D4,L4"), 30)
        self.assertEqual(get_fewest_steps(
                         "R75,D30,R83,U83,L12,D49,R71,U7,L72",
                         "U62,R66,U55,R34,D71,R55,D58,R83"),
                         610)
        self.assertEqual(get_fewest_steps(
                         "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51",
                         "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7"),
                         410)
