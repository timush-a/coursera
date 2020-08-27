import sys

"""
calculate sum of digits that 
passed as parameters on the command line
"""

digit_string = sys.argv[1]


if __name__ == "__main__":
    print(sum([int(x) for x in sys.argv[1]]))
