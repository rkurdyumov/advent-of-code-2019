import unittest

def most_detected(asteroid_map):
    occupied = list(asteroid_map)i


if __name__ == "__main__":
    main()

def main():
    pass

class AsteroidDetectorTest(unittest.TestCase):
    def test_small_map(self):
        asteroid_map = [
                ".#,,#",
                ".....",
                "#####",
                "....#",
                "...##"]
        self.assertEqual(most_detected(asteroid_map), 8)


