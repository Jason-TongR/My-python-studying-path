# Permutations Generation Algorithms (Lexicographic Order)
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

import math

def trotterjohnson(n:int) -> list[list[int]]:
    """
    list of all pi in Pi^n in minchange order
    """
    # require: n >= 1
    Tn = []

    if n == 1:
        # base case
        Tn = [[0]]
    else:
        # inductive case
        Tm = trotterjohnson(n-1)
        b = 0

        for Tb in Tm:
            
            T = [ Tb[:] for _ in range(n) ]

            for t in range(n):

                p = n-(t+1) if not b else t

                T[t].insert(p, n-1)

            Tn.extend(T)

            b = 1 - b

    return Tn
    # ensure: Tn = T^n

def rank(pi:list[int], n:int) -> int:
    """
    the position of pi in T^n
    """
    # require: pi in Pi^n
    r = 0

    if n > 1:

        k = pi.index(n-1)
        rho = pi[:]
        rho.pop(k)
        b = rank(rho, n-1)
        t = k if b % 2 else n-(k+1)

        r = n*b + t

    return r
    # ensure: T^n[r] = pi

def unrank(r:int, n:int) -> list[int]:
    """
    the rth permutation in T^n
    """
    # require: r in [0:n!)

    pi = [0]

    if r >= 1:

        b = r // n
        t = r % n

        pi = unrank(b, n-1)

        k = t if b % 2 else n-(t+1)

        pi.insert(k, n-1)

    return pi
    # ensure: T^n[r] = pi