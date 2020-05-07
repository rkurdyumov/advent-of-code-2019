from collections import namedtuple
import unittest

class IntcodeComputer:
    Opcode = namedtuple("Opcode", ("name", "params", "outputs"))
    _OPCODES = {
        1: Opcode("ADD", 3, 1),
        2: Opcode("MULTIPLY", 3, 1),
        3: Opcode("INPUT", 1, 1),
        4: Opcode("OUTPUT", 1, 0),
        5: Opcode("JUMP_IF_TRUE", 2, 0),
        6: Opcode("JUMP_IF_FALSE", 2, 0),
        7: Opcode("LESS_THAN", 3, 1),
        8: Opcode("EQUALS", 3, 1),
        99: Opcode("HALT", 0, 0)
    }

    def __init__(self, ints, wait_for_input=False):
       self.ints = ints
       self.ip = 0
       self.wait_for_input = wait_for_input
       self.done = False

    def is_done(self):
        return self.done

    def run(self, inputs=[], verbose=False):
        output = None
        while True: 
            opcode, modes = self._parse_instruction(self.ints[self.ip])
            op = self._OPCODES[opcode]
            pos = [self.ints[self.ip+1+j] if mode == 0 else self.ip+1+j 
                   for j, mode in enumerate(modes)]
            if verbose:
                i_max = max(pos)+1 if pos else self.ip+1
                print("Intcode: {}\n"
                      "ip: {}, inputs: {}, op: {}, modes: {}, pos: {} val: {}"
                      .format(self.ints[0:i_max], self.ip, inputs, op.name,
                      modes, pos, [self.ints[i] for i in pos]))
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
                output = self.ints[pos[0]]
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
            else:
                raise ValueError("{} has invalid opcode {} at ip = {}.".format(
                                 self.ints[0:self.ip], self.ints[ip], self.ip))
            self.ip += op.params + 1
        return output

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
        if digits != 0 or any(mode > 1 for mode in modes):
            raise ValueError("Instruction {} has invalid parameter modes."
                             .format(instruction))
        if op.outputs and any(mode > 0 for mode in modes[-op.outputs:]):
            raise ValueError("Instruction {} has invalid output param mode."
                             .format(instruction))
        return opcode, modes

class TestIntcodeComputer(unittest.TestCase):
    def test_intcode_basic(self):
        self.assertEqual(IntcodeComputer([99]).run(), None)
        self.assertEqual(IntcodeComputer([1002,4,3,4,33]).run(), None)
        self.assertEqual(IntcodeComputer([1101,2,3,0,4,0,99]).run(), 5)
        self.assertEqual(IntcodeComputer([104,5,99]).run(), 5)
        self.assertEqual(IntcodeComputer([102,10,0,0,4,0,99]).run(), 1020)
        self.assertEqual(IntcodeComputer([3,0,4,0,99]).run([123]), 123)

    def test_intcode_invalid(self):
        # Invalid opcode.
        self.assertRaises(ValueError, IntcodeComputer([0,0,99]).run)
        # Missing input for input instruction.
        self.assertRaises(ValueError, IntcodeComputer([3,0,99]).run)
        # Input instruction cannot write in immediate mode.
        self.assertRaises(ValueError, IntcodeComputer([103,0,99]).run)
        # Add instruction cannot write in immediate mode.
        self.assertRaises(ValueError, IntcodeComputer([10001,0,2,8,99]).run)
        # Invalid mode.
        self.assertRaises(ValueError, IntcodeComputer([201,0,2,0,99]).run)
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

    def test_intcode_is_done(self):
        c = IntcodeComputer([3,0,99], wait_for_input=True)
        self.assertFalse(c.is_done())
        self.assertEqual(c.run(), None) # Wait for input.
        self.assertFalse(c.is_done())
        self.assertEqual(c.run([5]), None) # Received input.
        self.assertTrue(c.is_done())

    def test_intcode_large(self):
        ints = [3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
                1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
                999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99]
        self.assertEqual(IntcodeComputer(ints.copy()).run([7]), 999)
        self.assertEqual(IntcodeComputer(ints.copy()).run([8]), 1000)
        self.assertEqual(IntcodeComputer(ints.copy()).run([9]), 1001)

