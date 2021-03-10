import io
import re
import unittest

from collections import defaultdict
from math import ceil

def minimum_ore(reactions, target_fuel=1):
    required = defaultdict(int, {"FUEL": target_fuel})
    while any(required[(resultant := chem)] > 0 for chem in reactions.keys()):
        amount, components = reactions[resultant]
        num_reactions = ceil(required[resultant] / amount)
        required[resultant] -= num_reactions * amount
        for amount, chemical in components:
            required[chemical] += num_reactions * amount
    return required["ORE"]

def maximum_fuel(reactions, available_ore=1000000000000):
    low = 1
    high = available_ore
    while low < high:
        mid = (low + high) // 2
        if minimum_ore(reactions, mid) > available_ore:
            high = mid - 1
        else:
            low = mid + 1
    return high

def get_reactions(input_file):
    reactions = {} # { chemical: (amount, [(other_amount, other_chemical)]) }
    for line in input_file:
        entries = [(int(amount), name) for amount, name in re.findall(
            r'(\d+) (\w+)', line)]
        amount, chemical = entries[-1]
        reactions[chemical] = (amount, entries[:-1])
    return reactions

def main():
    with open("day14.txt") as input_file:
        reactions = get_reactions(input_file)
    print("Part one solution: {}".format(minimum_ore(reactions)))
    print("Part two solution: {}".format(maximum_fuel(reactions)))

if __name__ == "__main__":
    main()

class ReactionTest(unittest.TestCase):
    def test_get_reactions(self):
        string_file = io.StringIO("""
            10 ORE => 10 A
            1 ORE => 1 B
            7 A, 1 B => 1 C
            7 A, 1 C => 1 D
            7 A, 1 D => 1 E
            7 A, 1 E => 1 FUEL
        """.strip())
        self.assertEqual(get_reactions(string_file), {
            "A": (10, [(10, "ORE")]),
            "B": (1, [(1, "ORE")]),
            "C": (1, [(7, "A"), (1, "B")]),
            "D": (1, [(7, "A"), (1, "C")]),
            "E": (1, [(7, "A"), (1, "D")]),
            "FUEL": (1, [(7, "A"), (1, "E")])}
        )

    def test_simple(self):
        string_file = io.StringIO("""
            10 ORE => 10 A
            1 ORE => 1 B
            7 A, 1 B => 1 C
            7 A, 1 C => 1 D
            7 A, 1 D => 1 E
            7 A, 1 E => 1 FUEL
        """.strip())
        self.assertEqual(31, minimum_ore(get_reactions(string_file)))

    def test_simple2(self):
        string_file = io.StringIO("""
            9 ORE => 2 A
            8 ORE => 3 B
            7 ORE => 5 C
            3 A, 4 B => 1 AB
            5 B, 7 C => 1 BC
            4 C, 1 A => 1 CA
            2 AB, 3 BC, 4 CA => 1 FUEL
        """.strip())
        self.assertEqual(165, minimum_ore(get_reactions(string_file)))

    def test_large(self):
        string_file = io.StringIO("""
            157 ORE => 5 NZVS
            165 ORE => 6 DCFZ
            44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
            12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
            179 ORE => 7 PSHF
            177 ORE => 5 HKGWZ
            7 DCFZ, 7 PSHF => 2 XJWVT
            165 ORE => 2 GPVTF
            3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT
        """.strip())
        reactions = get_reactions(string_file)
        self.assertEqual(13312, minimum_ore(reactions))
        self.assertEqual(82892753, maximum_fuel(reactions))


    def test_large2(self):
        string_file = io.StringIO("""
            2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG
            17 NVRVD, 3 JNWZP => 8 VPVL
            53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL
            22 VJHF, 37 MNCFX => 5 FWMGM
            139 ORE => 4 NVRVD
            144 ORE => 7 JNWZP
            5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC
            5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV
            145 ORE => 6 MNCFX
            1 NVRVD => 8 CXFTF
            1 VJHF, 6 MNCFX => 4 RFSQX
            176 ORE => 6 VJHF
        """.strip())
        reactions = get_reactions(string_file)
        self.assertEqual(180697, minimum_ore(reactions))
        self.assertEqual(5586022, maximum_fuel(reactions))

    def test_large3(self):
        string_file = io.StringIO("""
            171 ORE => 8 CNZTR
            7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL
            114 ORE => 4 BHXH
            14 VRPVC => 6 BMBT
            6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL
            6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT
            15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW
            13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW
            5 BMBT => 4 WPTQ
            189 ORE => 9 KTJDG
            1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP
            12 VRPVC, 27 CNZTR => 2 XDBXC
            15 KTJDG, 12 BHXH => 5 XCVML
            3 BHXH, 2 VRPVC => 7 MZWV
            121 ORE => 7 VRPVC
            7 XCVML => 6 RJRHP
            5 BHXH, 4 VRPVC => 5 LTCX
        """.strip())
        reactions = get_reactions(string_file)
        self.assertEqual(2210736, minimum_ore(reactions))
        self.assertEqual(460664, maximum_fuel(reactions))