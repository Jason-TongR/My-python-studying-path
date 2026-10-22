def unrank(r,n) :
    """
    an implementation of the unrank algorithm
    """
    # require : r in [0:2^n-1]
    A,i,k = set(),r%2,r//2  # i = bit 0 of r; k = r shifted right by i

    for a in range(n):
        j = k%2             # j = bit (a+1) of r 

        if i != j:          # X(A)[a] = bin(r)[a] XOR bin(r)[a+1]
            A = A | {a}

        i,k = j,k//2

    return A

