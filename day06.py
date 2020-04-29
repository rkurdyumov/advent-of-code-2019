from collections import defaultdict
import unittest

class Tree:
    def __init__(self, map_data):
        self.nodes = set()
        self.children = defaultdict(list)
        self.parents = {}
        entries = [entry.split(")") for entry in map_data.split()]
        for parent, child in entries:
            self.nodes.add(parent)
            self.nodes.add(child)
            self.children[parent].append(child)
            if child in self.parents:
                raise ValueError("Node {} has parent {}. Cannot add {}".format(
                                 child, self.parents[child], parent))
            self.parents[child] = parent

    def get_root(self):
        if not self.is_valid():
            return None
        all_children = sum(self.children.values(), [])
        root = set(self.nodes) - set(all_children)
        assert(len(root) == 1)
        return root.pop()

    def is_valid(self):
        all_children = sum(self.children.values(), [])
        # This only works if there are no loops in the tree.
        return len(self.nodes) == len(all_children) + 1

    def count_orbits(self):
        all_children = sum(self.children.values(), [])
        num_orbits = 0
        for child in all_children:
            while child in self.parents:
                num_orbits += 1
                child = self.parents[child]
        return num_orbits
    
    def min_transfers(self, a, b):
        if a == b:
            return 0
        if self.get_root() in {a, b}:
            return -1  # Root doesn't orbit anything.
        
        a_parents = []
        a_parent = a
        while a_parent in self.parents:
             a_parents.append(self.parents[a_parent])
             a_parent = self.parents[a_parent]

        b_parents = []
        b_parent = b
        while b_parent in self.parents:
             b_parents.append(self.parents[b_parent])
             b_parent = self.parents[b_parent]
        
        if a in b_parents:
            return b_parents.index(a) + 1
        if b in a_parents:
            return a_parents.index(b) + 1
 
        common_ancestors = [p for p in b_parents if p in a_parents]
        closest_ancestor = common_ancestors[0]
        return a_parents.index(closest_ancestor) + b_parents.index(
            closest_ancestor)

def main():
    with open("day06.txt") as input_file:
        map_data = input_file.read()
    orbits = Tree(map_data)

    print("Part 1 num_orbits: {}".format(orbits.count_orbits()))
    print("Part 2 min_transfers: {}".format(orbits.min_transfers("YOU", "SAN")))

if __name__ == '__main__':
    main()

        
class TestOrbits(unittest.TestCase):
    def test_valid_map(self):
        valid_map = """
        COM)B
        B)C
        COM)D
        """
        self.assertTrue(Tree(valid_map).is_valid())

        multiple_root_map = """
        COM)B
        A)C
        """
        self.assertFalse(Tree(multiple_root_map).is_valid())

        multiple_parent_map = """
        COM)B
        A)B
        """
        self.assertRaises(ValueError, Tree, multiple_parent_map)

        cycle_map = """
        COM)B
        B)C
        C)COM
        """
        self.assertFalse(Tree(cycle_map).is_valid())

        cycle_map_with_multiple_roots = """
        COM)B
        C)C
        C)COM
        A)D
        """
        # TODO: This should fail!
        # self.assertFalse(Tree(cycle_map).is_valid())

    def test_count_orbits(self):
        simple_map = """
        COM)B
        B)C
        COM)D
        """
        self.assertEqual(Tree(simple_map).count_orbits(), 4)

        example_map = """
        COM)B
        B)C
        C)D
        D)E
        E)F
        B)G
        G)H
        D)I
        E)J
        J)K
        K)L
        """
        self.assertEqual(Tree(example_map).count_orbits(), 42)

    def test_min_transfers(self):
        simple_map = """
        COM)B
        B)C
        C)D
        COM)E
        """
        simple_tree = Tree(simple_map)
        self.assertEqual(simple_tree.min_transfers("COM","B"), -1)
        self.assertEqual(simple_tree.min_transfers("COM","C"), -1)
        self.assertEqual(simple_tree.min_transfers("COM","D"), -1)
        self.assertEqual(simple_tree.min_transfers("COM","E"), -1)
        self.assertEqual(simple_tree.min_transfers("B","C"), 1)
        self.assertEqual(simple_tree.min_transfers("B","D"), 2)
        self.assertEqual(simple_tree.min_transfers("B","E"), 0)
        self.assertEqual(simple_tree.min_transfers("C","E"), 1)
        self.assertEqual(simple_tree.min_transfers("D","E"), 2)
        
