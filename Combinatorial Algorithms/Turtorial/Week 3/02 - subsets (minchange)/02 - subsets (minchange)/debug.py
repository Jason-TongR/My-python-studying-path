import sys
import graycode

def main():

    if len(sys.argv) < 2:
        print("usage: debug.py <n>")
    else:
        n = int(sys.argv[1])

        for i in range(0, 2**n):
            A = graycode.unrank(i, n)
            B = graycode.successor(A, n)
            r = graycode.rank(A, n)
            print(f'{i} successor({A}) = {B}')

if __name__ == "__main__":
    main()