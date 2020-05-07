from intcode import IntcodeComputer
from itertools import permutations
import unittest

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
