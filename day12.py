from math import lcm
import re
import unittest

def move(positions, velocities):
    new_velocities = [0] * len(velocities)
    for i in range(len(new_velocities)):
        others = list(positions)
        value = others.pop(i)
        delta = sum([1 if x > value else -1 if x < value else 0 for x in others])
        new_velocities[i] = velocities[i] + delta
    new_positions = [x + y for x, y in zip(positions, new_velocities)]
    return new_positions, new_velocities

def move_3d(positions, velocities):
    px, vx = move(positions[0], velocities[0])
    py, vy = move(positions[1], velocities[1])
    pz, vz = move(positions[2], velocities[2])
    return [px, py, pz], [vx, vy, vz]

def total_energy(positions, steps):
    p = positions
    v = [[0]*len(positions[0])]*len(positions)
    for _ in range(steps):
        p, v = move_3d(p, v)
    p_abs = [list(map(abs, row)) for row in p]
    v_abs = [list(map(abs, row)) for row in v]
    potential_energies = [sum(x) for x in zip(*p_abs)]
    kinetic_energies = [sum(x) for x in zip(*v_abs)]
    total_energies = [x*y for x, y in zip(potential_energies, kinetic_energies)]
    return sum(total_energies)

def steps_to_repeat(positions, velocities):
    steps = 0
    p = positions
    v = velocities
    while True:
        p, v = move(p, v)
        steps += 1
        if p == positions and v == velocities:
            break
    return steps

def steps_to_repeat_3d(positions):
    velocities = [[0]*len(positions[0])]*len(positions)
    steps_x = steps_to_repeat(positions[0], velocities[0])
    steps_y = steps_to_repeat(positions[1], velocities[1])
    steps_z = steps_to_repeat(positions[2], velocities[2])
    return lcm(steps_x, steps_y, steps_z)


def main():
    with open("day12.txt") as input_file:
        positions = [[int(x) for x in re.findall(r'-?\d+', row)] for row in input_file.readlines()]
    p = list(map(list, zip(*positions)))
    print(p)
    energy = total_energy(p, steps=1000)
    print(f"Part one solution: {energy}")
    steps = steps_to_repeat_3d(p)
    print(f"Part two solution: {steps}")

if __name__== "__main__":
    main()

class MoonMotionTest(unittest.TestCase):
    def test_move_3d(self):
        positions = [
            [-1, 2, 4, 3],
            [0, -10, -8, 5],
            [2, -7, 8, -1]]
        velocities = [[0]*len(positions[0])]*len(positions)
        p, v = move_3d(positions, velocities)
        self.assertEqual(v,[
            [3, 1, -3, -1],
            [-1, 3, 1, -3],
            [-1, 3, -3, 1]])
        self.assertEqual(p, [
            [2, 3, 1, 2],
            [-1, -7, -7, 2],
            [1, -4, 5, 0]])

    def test_move_3d_multiple(self):
        p = [
            [-1, 2, 4, 3],
            [0, -10, -8, 5],
            [2, -7, 8, -1]]
        v = [[0]*len(p[0])]*len(p)
        for _ in range(10):
            p, v = move_3d(p, v)
        self.assertEqual(p, [
            [2, 1, 3, 2],
            [1, -8, -6, 0],
            [-3, 0, 1, 4]])
        self.assertEqual(v, [
            [-3, -1, 3, 1],
            [-2, 1, 2, -1],
            [1, 3, -3, -1]])

    def test_total_energy(self):
        p = [
            [-1, 2, 4, 3],
            [0, -10, -8, 5],
            [2, -7, 8, -1]]
        self.assertEqual(total_energy(p, 10), 179)

        p2 = [
            [-8, 5, 2, 9],
            [-10, 5, -7, -8],
            [0, 10, 3, -3]]
        self.assertEqual(total_energy(p2, 100), 1940)

    def test_steps_to_repeat_3d(self):
        p = [
            [-1, 2, 4, 3],
            [0, -10, -8, 5],
            [2, -7, 8, -1]]
        self.assertEqual(steps_to_repeat_3d(p), 2772)

        p2 = [
            [-8, 5, 2, 9],
            [-10, 5, -7, -8],
            [0, 10, 3, -3]]
        self.assertEqual(steps_to_repeat_3d(p2), 4686774924)
