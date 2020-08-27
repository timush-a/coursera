import sys
import math


a, b, c = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])


def roots_of_square_equation(a, b, c):

    """Calculate the square equation roots if D is greater or equals to 0"""

    first_root = int((-b + math.sqrt(b ** 2 - (4 * a * c))) / (2 * a))
    second_root = int((-b - math.sqrt(b ** 2 - (4 * a * c))) / (2 * a))
    print(f"{first_root}\n{second_root}")


if __name__ == "__main__":
    roots_of_square_equation(a, b, c)
