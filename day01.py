import unittest

def get_fuel(mass):
    return mass//3 - 2

def get_fuel2(mass):
    fuel = 0
    while mass > 0:
        fuel_needed = max(0, get_fuel(mass))
        fuel += fuel_needed
        mass = fuel_needed
    return fuel

def main():
    total_fuel = 0
    total_fuel2 = 0
    with open("day01.txt") as input_file:
        for line in input_file:
            total_fuel += get_fuel(int(line))
            total_fuel2 += get_fuel2(int(line))
    print("Part 1 fuel required: {}".format(total_fuel))
    print("Part 2 fuel required: {}".format(total_fuel2))

if __name__ == '__main__':
    main()

class TestGetFuel(unittest.TestCase):
    def test_get_fuel(self):
        self.assertEqual(get_fuel(12), 2)
        self.assertEqual(get_fuel(14), 2)
        self.assertEqual(get_fuel(1969), 654)
        self.assertEqual(get_fuel(100756), 33583)

    def test_get_fuel2(self):
        self.assertEqual(get_fuel2(14), 2)
        self.assertEqual(get_fuel2(1969), 966)
        self.assertEqual(get_fuel2(100756), 50346)

