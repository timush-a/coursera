import sys

steps = sys.argv[1]


def stairs_generator(steps):
    steps = int(steps)
    empty_string = " " * steps
    for a in range(1, steps + 1):
        print((empty_string[0:steps - a] + ("*" * a)))

if __name__ == "__main__":
    stairs_generator(steps)
