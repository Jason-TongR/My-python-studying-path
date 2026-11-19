import sys
import math
import trees

def main():

    # if len(sys.argv) < 2:
    #         print("usage: debug.py <n>")
    # else:
        # n = int(sys.argv[1])

    tree = \
        [\
            0,\
            [3],\
            [2,\
                [5]\
            ],\
            [1,\
                [4,\
                    [7]\
                ],\
                [6]\
            ]
        ]

    pi = trees.parents(tree)

    done = 1

if __name__ == "__main__":
    main()