from collections import namedtuple
from enum import Enum
from itertools import permutations
import unittest

class HaltCondition(Enum):
    ON_HALT_INSTRUCTION = 1
    ON_OUTPUT = 2

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

    def run(self, inputs, verbose=False):
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
                        raise(ValueError, "Input instruction missing input")
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
                raise ValueError("{} has invalid opcode {} at position {}."
                                 .format(self.ints[0:self.ip],
                                 self.ints[self.ip], self.ip))
            self.ip += op.params + 1
        return output

    def is_done(self):
        return self.done

    def _parse_instruction(self, ins):
        opcode = ins % 100
        digits = ins // 100
        modes = []
        if opcode not in self._OPCODES:
            raise ValueError("Instruction {} has invalid opcode {}.".format(
                             ins, opcode))
        op  = self._OPCODES[opcode]
        while len(modes) < op.params:
            modes.append(digits % 10)
            digits //= 10
        if digits != 0 or any(mode > 1 for mode in modes):
            raise ValueError("Instruction {} has invalid parameter modes."
                             .format(ins))
        if op.outputs and any(mode > 0 for mode in modes[-op.outputs:]):
            raise ValueError("Instruction {} has invalid output param mode."
                             .format(ins))
        return opcode, modes

def max_thruster_series(ints, inputs=range(5)):
    max_output_phases = (0, None)
    for phases in permutations(inputs):
        phase_list = list(phases)
        prev_output = 0
        amps = [IntcodeComputer(ints.copy()) for _ in phases]
        for amp in amps:
            prev_output = amp.run([phase_list.pop(0), prev_output])
        if prev_output > max_output_phases[0]:
            max_output_phases = prev_output, phases
    return max_output_phases

def max_thruster_feedback(ints, inputs=range(5,10)):
    max_output_phases = (0, None)
    for phases in permutations(inputs):
        phase_list = list(phases)
        prev_output = 0
        amps = [IntcodeComputer(ints.copy(), wait_for_input=True)
                for _ in phases]
        while not amps[0].is_done():
            for amp in amps:
                inputs = [prev_output]
                if phase_list:
                    inputs.insert(0, phase_list.pop(0))
                prev_output = amp.run(inputs)
            if prev_output is not None and prev_output > max_output_phases[0]:
                max_output_phases = prev_output, phases
    return max_output_phases

def main():
    with open("day07.txt") as input_file:
        ints = [int(x) for x in input_file.read().split(",")]
    
    print("Part 1 output: {}".format(max_thruster_series(ints)[0]))
    print("Part 2 output: {}".format(max_thruster_feedback(ints)[0]))

if __name__ == '__main__':
    main()

class TestMaxThruster(unittest.TestCase):
    def test_max_thruster_series(self):
        ints1 = [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]
        self.assertEqual(max_thruster_series(ints1), (43210, (4,3,2,1,0)))

        ints2 = [3,23,3,24,1002,24,10,24,1002,23,-1,23,
                 101,5,23,23,1,24,23,23,4,23,99,0,0]
        self.assertEqual(max_thruster_series(ints2), (54321, (0,1,2,3,4)))

        ints3 = [3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,
                 1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0]
        self.assertEqual(max_thruster_series(ints3), (65210, (1,0,4,3,2)))
    def test_max_thruster_feedback(self):
        ints1 = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,
                 27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]
        self.assertEqual(max_thruster_feedback(ints1), (139629729, (9,8,7,6,5)))

        ints2 = [
            3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,
            -5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,
            53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10]
        self.assertEqual(max_thruster_feedback(ints2), (18216, (9,7,8,5,6)))
