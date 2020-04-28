#!/usr/bin/python3

from collections import namedtuple
import unittest


OP_DIGITS = 2
Opcode = namedtuple("Opcode", ("name", "params"))
OPCODES = {
    1: Opcode("ADD", 3),
    2: Opcode("MULTIPLY", 3),
    3: Opcode("INPUT", 1),
    4: Opcode("OUTPUT", 1),
    5: Opcode("JUMP_IF_TRUE", 2),
    6: Opcode("JUMP_IF_FALSE", 2),
    7: Opcode("LESS_THAN", 3),
    8: Opcode("EQUALS", 3),
    99: Opcode("HALT", 0),
}

# Get opcode and parameter modes from instruction.
def get_opcode_modes_from_instruction(instruction):
    digits = []
    while instruction != 0:
        digits.append(instruction % 10)
        instruction //= 10
    while len(digits) < OP_DIGITS:
        digits.append(0)
    opcode = digits[0] + digits[1] * 10
    if len(digits[OP_DIGITS:]) < OPCODES[opcode].params:
        digits += [0] * (OPCODES[opcode].params - len(digits[OP_DIGITS:]))
    return opcode, digits[OP_DIGITS:]
    

def run_intcode_program(ints, input_id=None):
    outputs = []
    i = 0
    while True: 
        opcode, modes = get_opcode_modes_from_instruction(ints[i])
        if OPCODES[opcode].name == "HALT":
            break
        #print("Intcode: {}, i: {}, input_id: {}".format(ints, i, input_id))
        #print("Opcode: {}".format(opcode))
        #print("Modes: {}".format(modes))
        # Position mode == 0, immediate mode == 1.
        pos = [ints[i + 1 + j] if mode == 0 else i + 1 + j
               for j, mode in enumerate(modes)]
        #print("pos: {}".format(pos))
        if OPCODES[opcode].name == "ADD":
            ints[pos[2]] = ints[pos[0]] + ints[pos[1]]
        elif OPCODES[opcode].name == "MULTIPLY":
            ints[pos[2]] = ints[pos[0]] * ints[pos[1]]
        elif OPCODES[opcode].name == "INPUT":
            if i != 0:
                raise ValueError("Input instruction at index {}.".format(i))
            if input_id is None:
                raise ValueError("No input instruction given.")
            ints[pos[0]] = input_id
        elif OPCODES[opcode].name == "OUTPUT":
            outputs.append(ints[pos[0]])
            #print("Output: {}".format(ints[pos[0]]))
        elif OPCODES[opcode].name == "JUMP_IF_TRUE":
            if (ints[pos[0]] != 0):
                i = ints[pos[1]] 
                continue
        elif OPCODES[opcode].name == "JUMP_IF_FALSE":
            if (ints[pos[0]] == 0):
                i = ints[pos[1]] 
                continue
        elif OPCODES[opcode].name == "LESS_THAN":
            ints[pos[2]] = 1 if ints[pos[0]] < ints[pos[1]] else 0
        elif OPCODES[opcode].name == "EQUALS":
            ints[pos[2]] = 1 if ints[pos[0]] == ints[pos[1]] else 0
        else:
            raise ValueError("{} has invalid opcode {} at position {}.".format(
                             ints[0:i], ints[i], i))
        i += OPCODES[opcode].params + 1
    return outputs

def main():
    with open("day05.txt") as input_file:
        ints = [int(x) for x in input_file.read().split(",")]

    out1 = run_intcode_program(ints.copy(), input_id=1)
    print("Part 1 output: {}".format(out1))
    out2 = run_intcode_program(ints.copy(), input_id=5)
    print("Part 2 output: {}".format(out2))


if __name__ == '__main__':
    main()

class TestRunIntcodeProgram(unittest.TestCase):
    def test_run_intcode_program(self):
        self.assertEqual(run_intcode_program([99]), [])
        self.assertEqual(run_intcode_program([1002,4,3,4,33]), [])
        self.assertEqual(run_intcode_program([1101,2,3,0,4,0,99]), [5])
        self.assertEqual(run_intcode_program([102,10,0,0,4,0,99]), [1020])
        self.assertEqual(run_intcode_program([3,0,4,0,99], 123), [123])
        self.assertRaises(ValueError, run_intcode_program, [3,0,3,0,99])

    def test_run_intcode_program_compare(self):
        self.assertEqual(run_intcode_program([3,9,8,9,10,9,4,9,99,-1,8], 8), [1])
        self.assertEqual(run_intcode_program([3,9,8,9,10,9,4,9,99,-1,8], 7), [0])
        self.assertEqual(run_intcode_program([3,9,7,9,10,9,4,9,99,-1,8], 8), [0])
        self.assertEqual(run_intcode_program([3,9,7,9,10,9,4,9,99,-1,8], 7), [1])
        self.assertEqual(run_intcode_program([3,3,1108,-1,8,3,4,3,99], 8), [1])
        self.assertEqual(run_intcode_program([3,3,1108,-1,8,3,4,3,99], 7), [0])
        self.assertEqual(run_intcode_program([3,3,1107,-1,8,3,4,3,99], 8), [0])
        self.assertEqual(run_intcode_program([3,3,1107,-1,8,3,4,3,99], 7), [1])

    def test_run_intcode_program_jump(self):
        self.assertEqual(run_intcode_program(
            [3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9], 0), [0])
        self.assertEqual(run_intcode_program(
            [3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9], 1), [1])
        self.assertEqual(run_intcode_program(
            [3,3,1105,-1,9,1101,0,0,12,4,12,99,1], 0), [0])
        self.assertEqual(run_intcode_program(
            [3,3,1105,-1,9,1101,0,0,12,4,12,99,1], 1), [1])

    def test_run_intcode_program_large(self):
        self.assertEqual(run_intcode_program(
            [3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
             1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
             999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99], 7), [999])
        self.assertEqual(run_intcode_program(
            [3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
             1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
             999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99], 8), [1000])
        self.assertEqual(run_intcode_program(
            [3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
             1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
             999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99], 9), [1001])
