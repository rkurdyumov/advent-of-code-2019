import unittest

def nested_len(input_list):
    length = 0
    for elem in input_list:
        length += nested_len(elem) if type(elem) == list else 1
    return length

def get_image_layers(digit_string, width, height):
    digits = [int(x) for x in digit_string]
    layers = []
    while digits:
        layer = []
        while digits and nested_len(layer) < width * height:
            row = []
            while digits and len(row) < width:
                row.append(digits.pop(0))
            layer.append(row)
        layers.append(layer)
    return layers

def decode_image(layers):
    rows = len(layers[0])
    cols = len(layers[0][0])
    final_image = []
    for _ in range(rows):
        final_image.append([0 for _ in range(cols)])
    for i in range(rows):
        for j in range(cols):
            for layer in reversed(layers):
                if layer[i][j] != 2:
                    final_image[i][j] = layer[i][j]
    return final_image

def print_image(image):
    for row in image:
        print("".join("X" if elem == 1 else " " for elem in row))

def main():
    with open("day08.txt") as input_file:
        layers = get_image_layers(input_file.read().strip(), 25, 6)

    num_zeros = [sum([x == 0 for row in layer for x in row]) for layer in layers]
    i_min = num_zeros.index(min(num_zeros))
    num_ones = sum([x == 1 for row in layers[i_min] for x in row])
    num_twos = sum([x == 2 for row in layers[i_min] for x in row])
    print("Part one solution: {}".format(num_ones * num_twos))
    print("Part two solution:")
    print_image(decode_image(layers))

if __name__ == "__main__":
    main()

class TestImageDecoder(unittest.TestCase):
    def test_get_image_layers(self):
        self.assertEqual(get_image_layers("123456789012", width=3, height=2),
                         [[[1,2,3], [4,5,6]], [[7,8,9], [0,1,2]]])
    def test_decode_image(self):
        self.assertEqual(decode_image(
            [[[0,2],[2,2]], [[1,1],[2,2]], [[2,2],[1,2]], [[0,0],[0,0]]]),
            [[0,1],[1,0]])
