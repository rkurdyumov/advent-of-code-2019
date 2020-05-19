from intcode import IntcodeComputer

def main():
    with open("day09.txt") as input_file:
        ints = [int(x) for x in input_file.read().split(",")]
    print("Part one solution: {}".format(IntcodeComputer(ints).run([1])))
    print("Part two solution: {}".format(IntcodeComputer(ints).run([2])))

if __name__ == "__main__":
    main()

