# Subset Generation Algorithms (Binary Reflected Gray Code Order)
#
# This file is part of the Winter 2025 edition of the Combinatorial Algorithms
# course taught at the Guangdong Technion Israel Institute of Technology, Shantou, China
#
# copyright (C) 2025 Valentin Cassano
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

def rank(A, n):
    """
    an implementation of the rank algorithm
    """
    # require: A in 2^[0:n)

    r, b = 0, 0        # b is the running suffix XOR

    for a in reversed(range(n)):

        if a in A:
            b = 1-b    # flip b: XOR with χ(A)[i] = 1

        r = 2*r + b    # Horner: shift r left, append b

    return r
    # ensure: G^n_r = X(A)

def unrank(r, n):
    """
    an implementation of the unrank algorithm
    """
    # require: r in [0:2^n-1)
    A, i, k = set(), r%2, r//2    # i = bit 0 of r; k = r shifted right by 1

    for a in range(n):
        j = k%2                   # j = bit (a+1) of r

        if i != j:                # χ(A)[a] = bin(r)[a] XOR bin(r)[a+1]
            A = A | {a}           # a belongs to A
        
        i, k = j, k//2            # slide window: next bit becomes current

    return A
    # ensure: G^n_r = X(A)

def successor(A, n):
    """
    an implementation of the successor algorithm
    """
    # require: A in 2^[0:n)

    B = A

    if not(len(B)%2):    # |A| even = rank is even = (j = 0)

        B = B ^ {0}      # flip element 0

    else:

        a = 0

        while not(a in B) and (a < n):
            a += 1            # find smallest element of A
        
        if a < n:
            B = B ^ {a+1}    # flip element j = i+1
        else:
            B = set()        # wrap-around

    return B
    # ensure: rank(B) = rank(A)+1 (mod 2^n)
