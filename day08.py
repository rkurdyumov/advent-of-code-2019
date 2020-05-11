import unittest

WIDTH = 25
HEIGHT = 6

def get_image_layers(digits, width, height):
    if (len(digits) % (width * height)) != 0:
        raise ValueError("Number of digits {} not divisible by layer size {}."
                         .format(len(digits), width * height))
    layers = []
    while digits:
        layer = []
        for _ in range(height):
            row = ""
            for _ in range(width):
                row += digits[0]
                digits = digits[1:]
            layer.append(row)
        layers.append(layer)
    return layers

def decode_image(layers):
    height = len(layers[0])
    width = len(layers[0][0])
    final_image = []
    for i in range(height):
        row = ""
        for j in range(width):
            colors = [c[i][j] for c in reversed(layers) if c[i][j] != "2"]
            row += colors[-1] if colors else "2"
        final_image.append(row)
    return final_image

def print_image(image):
    for row in image:
        print("".join(u"\u2588" if elem == "1" else " " for elem in row))

def main():
    with open("day08.txt") as input_file:
        layers = get_image_layers(input_file.read().strip(), WIDTH, HEIGHT)
    min_0_layer = min(layers, key=lambda layer: "".join(layer).count("0"))
    num_ones = "".join(min_0_layer).count("1")
    num_twos = "".join(min_0_layer).count("2")
    print("Part one solution: {}".format(num_ones * num_twos))
    print("Part two solution:")
    print_image(decode_image(layers))

if __name__ == "__main__":
    main()

class TestImageDecoder(unittest.TestCase):
    def test_get_image_layers(self):
        self.assertEqual(get_image_layers("123456789012", width=3, height=2),
                         [["123", "456"], ["789", "012"]])
        self.assertRaises(ValueError,get_image_layers,
                          "123456789012", width=3, height=3)
    def test_decode_image(self):
        self.assertEqual(decode_image(get_image_layers(
            "0222112222120000", width=2, height=2)), ["01", "10"])
