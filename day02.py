#!/usr/bin/python3

from itertools import product
import unittest

OPCODE_ADD = 1
OPCODE_MULTIPLY = 2
OPCODE_HALT = 99

def run_intcode_program(ints, noun=None, verb=None):
    if noun is not None:
        ints[1] = noun
    if verb is not None:
        ints[2] = verb
    i = 0
    while ints[i] != OPCODE_HALT:
        if ints[i] == OPCODE_ADD:
            ints[ints[i+3]] = ints[ints[i+1]] + ints[ints[i+2]]
        elif ints[i] == OPCODE_MULTIPLY:
            ints[ints[i+3]] = ints[ints[i+1]] * ints[ints[i+2]]
        else:
            raise ValueError("{} has invalid opcode {} at position {}.".format(
                             ints[0:i], ints[i], i))
        i+=4
    return ints

def main():
    with open("day02.txt") as input_file:
        ints = [int(x) for x in input_file.read().split(",")]

    run_ints = run_intcode_program(ints.copy(), noun=12, verb=2)
    print("Part 1 output: {}".format(run_ints[0]))

    for noun, verb in product(range(100), repeat=2):
        run_ints = run_intcode_program(ints.copy(), noun, verb)
        if run_ints[0] == 19690720:
            print("Part 2 output: {} for verb={},noun={}".format(
                  100 * noun + verb, verb, noun))
            break

if __name__ == '__main__':
    main()

class TestRunIntcodeProgram(unittest.TestCase):
    def test_run_intcode_program(self):
        self.assertEqual(run_intcode_program([1,0,0,0,99]), [2,0,0,0,99])
        self.assertEqual(run_intcode_program([2,3,0,3,99]), [2,3,0,6,99])
        self.assertEqual(run_intcode_program([2,4,4,5,99,0]),
                                             [2,4,4,5,99,9801])
        self.assertEqual(run_intcode_program([1,1,1,4,99,5,6,0,99]),
                                             [30,1,1,4,2,5,6,0,99])
        self.assertEqual(run_intcode_program([1,9,10,3,2,3,11,0,99,30,40,50]),
                                             [3500,9,10,70,2,3,11,0,99,30,40,50])
        self.assertRaises(ValueError, run_intcode_program, [3,0,0,0,99])
