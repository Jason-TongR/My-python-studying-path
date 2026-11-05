import math

##################################
##################################

def fac2dec(f:list[int])->list[int]:
    """
    returns the decimal value of the factorial number
    """
    return []

def dec2fac(d:list[int])->list[int]:
    """
    returns the decimal value of the factorial number
    """
    return []

def perm2lehmer(pi:list[int])->list[int]:
    """
    returns the Lehmer code associated to the input permutation
    """
    n   = len(pi)
    rho = [0]*n

    for i in range(n):
        rho[i] = len([x for x in pi[(i+1):] if x < pi[i]])

    return rho

def lehmer2perm(rho:list[int])->list[int]:
    """
    returns the permutation associated to the Lehmer code
    """
    n   = len(rho)
    pi = [0]*n

    # do something!

    return pi

def rank(pi:list[int])->int:
    """
    an implementation of the rank algorithm
    """
    return fac2dec(perm2lehmer(pi))

def unrank(r:int)->list[int]:
    """
    an implementation of the unrank algorithm
    """
    return lehmer2perm(dec2fac(r))

def successor(pi:list[int])->list[int]:
    """
    an implementation of the successor algorithm
    """
    pass

##################################
##################################


def fac2dec(A,n):
    a = 0
    for i in range( 0,n):
        a = a + A[i]*math.factorial(n-i-1)
    return a


def dec2fac(a,n):
    A,q,r,i = [0]*n,a,0,1
    while q > 0 :
        q,r = q//i,q%i
        A[i-1] = r
        i += 1
    A.reverse()
    return A


def Rank(S,n):
    A = []
    for i in range(0,n):
        t = 0
        for j in range(i,n):
            if S[i] > S[j]:
                t += 1
        A.append(t)
    return fac2dec(A,len(A))


def Unrank(r,n):
    S,p,l = [],dec2fac(r,n), list(range(0,n))
    k = 0
    for i in range(0,n):
        k = p[i]
        S.append(l[k])
        l = l[:k] + l[k+1:]
    return S


def LexSuccesor(n, A):
    B = list(A)
    i = -1
    for k in range(0,n-1):
        if B[k] < B[k+1]:
            i = k

    if i != -1:
        j = n-1
        while B[j] < B[i]:
            j = j-1
        B[j], B[i] = B[i], B[j]
        temp = B[i +1:]
        temp.reverse()
        p = B[:i+1] + temp
    else:
        p = list(range(0,n))
    return p

