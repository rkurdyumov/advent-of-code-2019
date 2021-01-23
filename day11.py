from collections import defaultdict

from intcode import IntcodeComputer

dxy = [
    [0, 1], # up
    [1, 0], # right
    [0, -1], # down
    [-1, 0]] # left

def update(panels, coords, direction, color, turn_right):
    panels[tuple(coords)] = color # white = 1
    direction = (direction + (1 if turn_right else -1)) % 4
    coords = [coords[0] + dxy[direction][0], coords[1] + dxy[direction][1]]
    return coords, direction

def get_painted_panels(ints, initial_color):
    panels = defaultdict(int) # { (x, y): color }
    computer = IntcodeComputer(ints, wait_for_input=True)
    coords = [0, 0]
    direction = 0
    panels[tuple([0,0])] = initial_color
    while not computer.is_done():
        color, turn = computer.run(inputs=[panels[tuple(coords)]])
        coords, direction = update(panels, coords, direction, color, turn)
    return panels

def print_panels(panels):
    xs, ys = zip(*panels.keys())
    # Print from bottom to top (since up is positive)
    for y in reversed(range(min(ys), max(ys) + 1)):
        for x in range(min(xs), max(xs) + 1):
            print(u"\u2588" if panels[(x,y)] else " ", end="")
        print()

def main():
    with open("day11.txt") as input_file:
        ints = [int(x) for x in input_file.read().split(",")]
    panels = get_painted_panels(ints, 0)
    print("Part one solution: {}".format(len(panels)))
    print("Part two solution:")
    print_panels(get_painted_panels(ints, 1))

if __name__ == "__main__":
    main()