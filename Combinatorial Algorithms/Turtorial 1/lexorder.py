def rank(A:set,n:int) -> int:
    """
    the tank of A in lexicographic order(this is a comment)
    """

    """
    require:
        A in 2^[0,n)
    """

    r:int =0

    for i in range(n):
    
        r = r + (2**i) * (i in A)

    return r

    """
    ensure: r = int(X(A))
    """