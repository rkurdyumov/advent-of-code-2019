#!/usr/bin/python3

from collections import namedtuple
import unittest

Opcode = namedtuple("Opcode", ("name", "params", "outputs"))
OPCODES = {
    1: Opcode("ADD", 3, 1),
    2: Opcode("MULTIPLY", 3, 1),
    3: Opcode("INPUT", 1, 1),
    4: Opcode("OUTPUT", 1, 0),
    5: Opcode("JUMP_IF_TRUE", 2, 0),
    6: Opcode("JUMP_IF_FALSE", 2, 0),
    7: Opcode("LESS_THAN", 3, 1),
    8: Opcode("EQUALS", 3, 1),
    99: Opcode("HALT", 0, 0),
}

# Get opcode and parameter modes from instruction.
def get_opcode_modes_from_instruction(instruction):
    opcode = instruction % 100
    digits = instruction // 100
    modes = []
    if opcode not in OPCODES:
        raise ValueError("{} has bad opcode: {}.".format(instruction, opcode))
    while len(modes) < OPCODES[opcode].params:
        modes.append(digits % 10)
        digits //= 10
    if digits != 0 or any(mode > 1 for mode in modes):
        raise ValueError("{} has bad parameter modes.".format(instruction))
    if OPCODES[opcode].outputs and modes[-OPCODES[opcode].outputs] > 0:
        raise ValueError("{} has bad output param mode.".format(instruction))
    return opcode, modes

def run_intcode(ints, input_id=None, verbose=False):
    outputs = []
    ip = 0
    while True: 
        opcode, modes = get_opcode_modes_from_instruction(ints[ip])
        pos = [ints[ip + 1 + j] if mode == 0 else ip + 1 + j
               for j, mode in enumerate(modes)]
        if verbose:
            print("Intcode: {}, op: {}, modes: {}, pos: {}".format(
                  ints[ip:ip + 7], OPCODES[opcode].name, modes, pos))
        if OPCODES[opcode].name == "HALT":
            break
        if OPCODES[opcode].name == "ADD":
            ints[pos[2]] = ints[pos[0]] + ints[pos[1]]
        elif OPCODES[opcode].name == "MULTIPLY":
            ints[pos[2]] = ints[pos[0]] * ints[pos[1]]
        elif OPCODES[opcode].name == "INPUT":
            if input_id is None:
                raise ValueError("Input instruction requires input_id.")
            ints[pos[0]] = input_id
        elif OPCODES[opcode].name == "OUTPUT":
            outputs.append(ints[pos[0]])
        elif OPCODES[opcode].name == "JUMP_IF_TRUE":
            if (ints[pos[0]] != 0):
                ip = ints[pos[1]] 
                continue
        elif OPCODES[opcode].name == "JUMP_IF_FALSE":
            if (ints[pos[0]] == 0):
                ip = ints[pos[1]] 
                continue
        elif OPCODES[opcode].name == "LESS_THAN":
            ints[pos[2]] = 1 if ints[pos[0]] < ints[pos[1]] else 0
        elif OPCODES[opcode].name == "EQUALS":
            ints[pos[2]] = 1 if ints[pos[0]] == ints[pos[1]] else 0
        else:
            raise ValueError("{} has invalid opcode {} at position {}.".format(
                             ints[0:ip], ints[ip], ip))
        ip += OPCODES[opcode].params + 1
    return outputs

def main():
    with open("day05.txt") as input_file:
        ints = [int(x) for x in input_file.read().split(",")]

    print("Part 1 output: {}".format(run_intcode(ints.copy(), 1)))
    print("Part 2 output: {}".format(run_intcode(ints.copy(), 5)))

if __name__ == '__main__':
    main()

class TestRunIntcode(unittest.TestCase):
    def test_run_intcode(self):
        self.assertEqual(run_intcode([99]), [])
        self.assertEqual(run_intcode([1002,4,3,4,33]), [])
        self.assertEqual(run_intcode([1101,2,3,0,4,0,99]), [5])
        self.assertEqual(run_intcode([104,5,99]), [5])
        self.assertEqual(run_intcode([102,10,0,0,4,0,99]), [1020])
        self.assertEqual(run_intcode([3,0,4,0,99], 123), [123])
        self.assertRaises(ValueError, run_intcode, [0,0,99]) # Bad opcode.
        self.assertRaises(ValueError, run_intcode, [3,0,99]) # Missing input.
        self.assertRaises(ValueError, run_intcode, [103,0,99]) # Bad modes.
        self.assertRaises(ValueError, run_intcode, [10001,0,2,8,99])
        self.assertRaises(ValueError, run_intcode, [201,0,2,0,99])

    def test_run_intcode_compare(self):
        self.assertEqual(run_intcode([3,9,8,9,10,9,4,9,99,-1,8], 8), [1])
        self.assertEqual(run_intcode([3,9,8,9,10,9,4,9,99,-1,8], 7), [0])
        self.assertEqual(run_intcode([3,9,7,9,10,9,4,9,99,-1,8], 8), [0])
        self.assertEqual(run_intcode([3,9,7,9,10,9,4,9,99,-1,8], 7), [1])
        self.assertEqual(run_intcode([3,3,1108,-1,8,3,4,3,99], 8), [1])
        self.assertEqual(run_intcode([3,3,1108,-1,8,3,4,3,99], 7), [0])
        self.assertEqual(run_intcode([3,3,1107,-1,8,3,4,3,99], 8), [0])
        self.assertEqual(run_intcode([3,3,1107,-1,8,3,4,3,99], 7), [1])

    def test_run_intcode_jump(self):
        self.assertEqual(run_intcode(
            [3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9], 0), [0])
        self.assertEqual(run_intcode(
            [3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9], 1), [1])
        self.assertEqual(run_intcode(
            [3,3,1105,-1,9,1101,0,0,12,4,12,99,1], 0), [0])
        self.assertEqual(run_intcode(
            [3,3,1105,-1,9,1101,0,0,12,4,12,99,1], 1), [1])

    def test_run_intcode_large(self):
        self.assertEqual(run_intcode(
            [3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
             1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
             999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99], 7), [999])
        self.assertEqual(run_intcode(
            [3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
             1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
             999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99], 8), [1000])
        self.assertEqual(run_intcode(
            [3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
             1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
             999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99], 9), [1001])
