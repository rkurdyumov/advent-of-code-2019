from collections import defaultdict
from collections import namedtuple
from enum import IntEnum
import unittest

class IntcodeComputer:
    Opcode = namedtuple("Opcode", ("name", "params", "writes"))
    _OPCODES = {
        1: Opcode("ADD", 3, 1),
        2: Opcode("MULTIPLY", 3, 1),
        3: Opcode("INPUT", 1, 1),
        4: Opcode("OUTPUT", 1, 0),
        5: Opcode("JUMP_IF_TRUE", 2, 0),
        6: Opcode("JUMP_IF_FALSE", 2, 0),
        7: Opcode("LESS_THAN", 3, 1),
        8: Opcode("EQUALS", 3, 1),
        9: Opcode("ADJUST_BASE", 1, 0),
        99: Opcode("HALT", 0, 0)
    }

    class Mode(IntEnum):
        POSITION = 0
        IMMEDIATE = 1
        RELATIVE = 2

    def __init__(self, ints, wait_for_input=False):
        self.ints = defaultdict(int, enumerate(ints))
        self.ip = 0 # Instruction pointer.
        self.base = 0 # Used in RELATIVE mode.
        self.wait_for_input = wait_for_input
        self.done = False

    def is_done(self):
        return self.done

    def run(self, inputs=[], verbose=False):
        outputs = []
        while True:
            opcode, modes = self._parse_instruction(self.ints[self.ip])
            op = self._OPCODES[opcode]
            pos = []
            for j, mode in enumerate(modes):
                if mode == self.Mode.POSITION:
                    pos.append(self.ints[self.ip + 1 + j])
                elif mode == self.Mode.IMMEDIATE:
                    pos.append(self.ip + 1 + j)
                elif mode == self.Mode.RELATIVE:
                    pos.append(self.base + self.ints[self.ip + 1 + j])
            if verbose:
                i_max = self.ip + len(modes)
                print("Intcode: {}\n"
                      "ip: {}, ins: {}, base: {}, inputs: {}, op: {}, "
                       "modes: {}, pos: {} val: {}\n"
                       "output: {}\n-----"
                      .format(list(self.ints.values())[0:i_max+1], self.ip,
                              self.ints[self.ip], self.base, inputs, op.name,
                              modes, pos, [self.ints[i] for i in pos], outputs))
            if op.name == "HALT":
                self.done = True
                break
            elif op.name == "ADD":
                self.ints[pos[2]] = self.ints[pos[0]] + self.ints[pos[1]]
            elif op.name == "MULTIPLY":
                self.ints[pos[2]] = self.ints[pos[0]] * self.ints[pos[1]]
            elif op.name == "INPUT":
                if not inputs:
                    if self.wait_for_input:
                        break # Wait for input, so don't increment ip.
                    else:
                        raise ValueError("Input instruction missing input.")
                self.ints[pos[0]] = inputs.pop(0)
            elif op.name == "OUTPUT":
                outputs.append(self.ints[pos[0]])
            elif op.name == "JUMP_IF_TRUE":
                if (self.ints[pos[0]] != 0):
                    self.ip = self.ints[pos[1]]
                    continue
            elif op.name == "JUMP_IF_FALSE":
                if (self.ints[pos[0]] == 0):
                    self.ip = self.ints[pos[1]]
                    continue
            elif op.name == "LESS_THAN":
                if self.ints[pos[0]] < self.ints[pos[1]]:
                    self.ints[pos[2]] = 1
                else:
                    self.ints[pos[2]] = 0
            elif op.name == "EQUALS":
                if self.ints[pos[0]] == self.ints[pos[1]]:
                    self.ints[pos[2]] = 1
                else:
                    self.ints[pos[2]] = 0
            elif op.name == "ADJUST_BASE":
                self.base += self.ints[pos[0]]
            self.ip += op.params + 1
        return outputs[0] if len(outputs) == 1 else outputs

    def _parse_instruction(self, instruction):
        opcode = instruction % 100
        digits = instruction // 100
        modes = []
        if opcode not in self._OPCODES:
            raise ValueError("Instruction {} has invalid opcode: {}.".format(
                             instruction, opcode))
        op  = self._OPCODES[opcode]
        while len(modes) < op.params:
            modes.append(digits % 10)
            digits //= 10
        if digits != 0 or any(mode > self.Mode.RELATIVE for mode in modes):
            raise ValueError("Instruction {} has invalid parameter modes."
                             .format(instruction))
        if op.writes and any(mode == self.Mode.IMMEDIATE
                             for mode in modes[-op.writes:]):
            raise ValueError("Instruction {} has write param immediate mode."
                             .format(instruction))
        return opcode, modes

class TestIntcodeComputer(unittest.TestCase):
    def test_intcode_basic(self):
        self.assertEqual(IntcodeComputer([99]).run(), [])
        self.assertEqual(IntcodeComputer([1002,4,3,4,33]).run(), [])
        self.assertEqual(IntcodeComputer([1101,2,3,0,4,0,99]).run(), 5)
        self.assertEqual(IntcodeComputer([104,5,99]).run(), 5)
        self.assertEqual(IntcodeComputer([102,10,0,0,4,0,99]).run(), 1020)
        self.assertEqual(IntcodeComputer([3,0,4,0,99]).run([123]), 123)

    def test_intcode_invalid(self):
        # Invalid opcode.
        self.assertRaises(ValueError, IntcodeComputer([1055,0,99]).run)
        # Missing input for input instruction.
        self.assertRaises(ValueError, IntcodeComputer([3,0,99]).run)
        # Input instruction cannot write in immediate mode.
        self.assertRaises(ValueError, IntcodeComputer([103,0,99]).run, [5])
        # Add instruction cannot write in immediate mode.
        self.assertRaises(ValueError, IntcodeComputer([10001,0,2,8,99]).run)
        # Invalid mode.
        self.assertRaises(ValueError, IntcodeComputer([301,0,2,0,99]).run)
        # Halt instruction cannot have params.
        self.assertRaises(ValueError, IntcodeComputer([199,99]).run)

    def test_intcode_compare(self):
        self.assertTrue(IntcodeComputer([3,9,8,9,10,9,4,9,99,-1,8]).run([8]))
        self.assertFalse(IntcodeComputer([3,9,8,9,10,9,4,9,99,-1,8]).run([7])),
        self.assertFalse(IntcodeComputer([3,9,7,9,10,9,4,9,99,-1,8]).run([8]))
        self.assertTrue(IntcodeComputer([3,9,7,9,10,9,4,9,99,-1,8]).run([7]))
        self.assertTrue(IntcodeComputer([3,3,1108,-1,8,3,4,3,99]).run([8]))
        self.assertFalse(IntcodeComputer([3,3,1108,-1,8,3,4,3,99]).run([7]))
        self.assertFalse(IntcodeComputer([3,3,1107,-1,8,3,4,3,99]).run([8]))
        self.assertTrue(IntcodeComputer([3,3,1107,-1,8,3,4,3,99]).run([7]))

    def test_intcode_jump_if_nonzero(self):
        self.assertFalse(IntcodeComputer(
            [3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9]).run([0]))
        self.assertTrue(IntcodeComputer(
            [3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9]).run([1]))
        self.assertFalse(IntcodeComputer(
            [3,3,1105,-1,9,1101,0,0,12,4,12,99,1]).run([0]))
        self.assertTrue(IntcodeComputer(
            [3,3,1105,-1,9,1101,0,0,12,4,12,99,1]).run([1]))

    def test_intcode_wait_for_input(self):
        c = IntcodeComputer([3,0,99], wait_for_input=True)
        self.assertFalse(c.is_done())
        c.run()
        self.assertFalse(c.is_done()) # Wait for input.
        c.run([5])
        self.assertTrue(c.is_done()) # Received input.

    def test_intcode_large(self):
        ints = [3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
                1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
                999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99]
        self.assertEqual(IntcodeComputer(ints.copy()).run([7]), 999)
        self.assertEqual(IntcodeComputer(ints.copy()).run([8]), 1000)
        self.assertEqual(IntcodeComputer(ints.copy()).run([9]), 1001)

    def test_intcode_relative_base(self):
        quine = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]
        self.assertEqual(IntcodeComputer(quine).run(), quine)

    def test_intcode_memory(self):
        digits16 = [1102,34915192,34915192,7,4,7,99,0]
        self.assertEqual(len(str(IntcodeComputer(digits16).run())), 16)

    def test_intcode_large_number(self):
        large_num = [104,1125899906842624,99]
        self.assertEqual(IntcodeComputer(large_num).run(), large_num[1])

