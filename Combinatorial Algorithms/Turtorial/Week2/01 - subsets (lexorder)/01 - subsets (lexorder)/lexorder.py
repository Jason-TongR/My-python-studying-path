# Subset Generation Algorithms (Lexicographic Order)
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

def rank(A: set, n: int) -> int:
    """
    an implementation of the rank algorithm
    """
    # require: A: 2^[0:n)
    r = 0

    for i in reversed(range(n)):

        r = 2*r + (i in A)

    return r
    # ensure :r = int(X(A))

def unrank(r: int, n: int) -> set:
    """
    an implementation of the unrank algorithm
    """
    # require: r: [0:2^n]

    A = set()

    for a in range(n):
        
        if r%2:
            A = A | {a}
        
        r //= 2

    return A
    # ensure: int(X(A)) = r

def successor(A: set, n: int) -> set:
    """
    an implementation of the successor algorithm
    """
    # require: A: 2^[0:n)
    
    B, a = A, 0

    while (a in B):

        B, a = B-{a}, a+1
    
    if a < n:

        B = B | {a}

    return B
    # ensure: X(B) = X(A)+1
