from collections import defaultdict

from intcode import IntcodeComputer

def get_move_score(output):
    ball_x = None
    paddle_x = None
    score = None
    for i in range(0, len(output), 3):
        if output[i + 2] == 4:
            ball_x = output[i]
        elif output[i + 2] == 3:
            paddle_x = output[i]
        elif (output[i], output[i + 1]) == (-1, 0):
            score = output[i + 2]
    dx = paddle_x - ball_x if ball_x and paddle_x else None
    move = None if not dx else -1 if dx > 0 else +1 if dx < 0 else 0
    return move, score

def print_tiles(output):
    tiles = defaultdict(int) # {(x,y): tile}
    for i in range(0, len(output), 3):
        tiles[(output[i], output[i + 1])] = output[i + 2]
    xs, ys = zip(*tiles.keys())
    for y in reversed(range(min(ys), max(ys) + 1)):
        for x in range(min(xs), max(xs) + 1):
            print(tiles[(x,y)] if tiles[(x,y)] else " ", end="")
        print()

def main():
    with open("day13.txt") as input_file:
        ints = [int(x) for x in input_file.read().split(",")]
    output = IntcodeComputer(ints).run()
    print("Part one solution: {}".format(output[2::3].count(2)))

    ints[0] = 2
    computer = IntcodeComputer(ints, wait_for_input=True)
    move = 0 # Don't move paddle to start.
    while not computer.is_done():
        output = computer.run(inputs=[move])
        move, score = get_move_score(output)
    print("Part two solution: {}".format(score))

if __name__ == "__main__":
    main()