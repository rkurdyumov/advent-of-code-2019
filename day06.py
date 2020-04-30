import unittest

class OrbitMap:
    def __init__(self, orbits):
        self.children = set()
        self.parents = {} # {satellite: primary}
        for primary, satellite in orbits:
            self.children.add(satellite)
            if satellite in self.parents:
                raise ValueError("Object {} is orbiting {}. Cannot orbit {}."
                    .format(satellite, self.parents[satellite], primary))
            self.parents[satellite] = primary
        root = self._get_ancestors(next(iter(self.children)))[-1]
        for c in self.children:
            if root != self._get_ancestors(c)[-1]:
                raise ValueError("Invalid orbit map: multiple COM: {}, {}."
                                 .format(root, self._get_ancestors(c)[-1]))

    def _get_ancestors(self, obj):
        ancestors = [obj]
        visited = set()
        while ancestors[-1] in self.parents:
            if ancestors[-1] in visited:
                raise ValueError("Cycle in orbit map: {}.". format(ancestors))
            visited.add(ancestors[-1])
            ancestors.append(self.parents[ancestors[-1]])
        return ancestors[1:]

    def count_orbits(self):
        num_orbits = 0
        # This could be improved by caching num_orbits for each ancestor.
        for child in self.children:
            num_orbits += len(self._get_ancestors(child))
        return num_orbits
    
    def min_transfers(self, a, b):
        a_ancestors = self._get_ancestors(a)
        b_ancestors = self._get_ancestors(b)
        for i, ancestor in enumerate(a_ancestors):
            if ancestor in b_ancestors:
                return i + b_ancestors.index(ancestor)
        return -1

def main():
    with open("day06.txt") as input_file:
        orbits = [entry.split(")") for entry in input_file.read().split()]
    orbit_map = OrbitMap(orbits)
    print("Part 1 orbits: {}".format(orbit_map.count_orbits()))
    print("Part 2 transfers: {}".format(orbit_map.min_transfers("YOU", "SAN")))

if __name__ == '__main__':
    main()

class TestOrbitMap(unittest.TestCase):

    def test_invalid_maps(self):
        multiple_parent_map = [
            ["COM", "B"],
            ["A", "B"]]
        self.assertRaises(ValueError, OrbitMap, multiple_parent_map)

        multiple_root_map = [
            ["COM", "B"],
            ["A", "C"]]
        self.assertRaises(ValueError, OrbitMap, multiple_root_map)

        cycle_map = [
            ["COM", "B"],
            ["B", "C"],
            ["C", "COM"]]
        self.assertRaises(ValueError, OrbitMap, cycle_map)

        cycle_map_with_multiple_roots = [
            ["COM", "B"],
            ["C", "C"],
            ["C", "COM"],
            ["A", "D"]]
        self.assertRaises(ValueError, OrbitMap, cycle_map_with_multiple_roots)

    def test_count_orbits(self):
        self.assertEqual(OrbitMap([["COM", "B"]]).count_orbits(), 1)

        simple_map = [
            ["COM", "B"],
            ["B", "C"],
            ["COM", "D"]]
        self.assertEqual(OrbitMap(simple_map).count_orbits(), 4)

        example_map = [
            ["COM", "B"],
            ["B", "C"],
            ["C", "D"],
            ["D", "E"],
            ["E", "F"],
            ["B", "G"],
            ["G", "H"],
            ["D", "I"],
            ["E", "J"],
            ["J", "K"],
            ["K", "L"]]
        self.assertEqual(OrbitMap(example_map).count_orbits(), 42)

    def test_min_transfers(self):
        simple_map = [
            ["COM", "B"],
            ["B", "C"],
            ["C", "D"],
            ["COM", "E"]]
        simple_map = OrbitMap(simple_map)
        self.assertEqual(simple_map.min_transfers("COM","B"), -1)
        self.assertEqual(simple_map.min_transfers("COM","C"), -1)
        self.assertEqual(simple_map.min_transfers("COM","D"), -1)
        self.assertEqual(simple_map.min_transfers("COM","E"), -1)
        self.assertEqual(simple_map.min_transfers("B","B"), 0)
        self.assertEqual(simple_map.min_transfers("B","C"), 1)
        self.assertEqual(simple_map.min_transfers("B","D"), 2)
        self.assertEqual(simple_map.min_transfers("B","E"), 0)
        self.assertEqual(simple_map.min_transfers("C","E"), 1)
        self.assertEqual(simple_map.min_transfers("D","E"), 2)

        example_map = [
            ["COM", "B"],
            ["B", "C"],
            ["C", "D"],
            ["D", "E"],
            ["E", "F"],
            ["B", "G"],
            ["G", "H"],
            ["D", "I"],
            ["E", "J"],
            ["J", "K"],
            ["K", "L"],
            ["K", "YOU"],
            ["I", "SAN"]]
        example_map = OrbitMap(example_map)
        self.assertEqual(example_map.min_transfers("YOU","SAN"), 4)
        
