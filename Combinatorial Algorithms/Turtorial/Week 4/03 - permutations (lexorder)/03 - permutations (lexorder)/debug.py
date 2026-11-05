import sys
import math
import lexorder

def main():

    if len(sys.argv) < 2:
        print("usage: debug.py <n>")
    else:
        n = int(sys.argv[1])

        for i in range(math.factorial(n)):
            
            A = lexorder.unrank(i, n)
            print(f'unrank({i}, n) = {A}')

            r = lexorder.rank(A, n)
            print(f'rank({A}, n) = {r}')

if __name__ == "__main__":
    main()