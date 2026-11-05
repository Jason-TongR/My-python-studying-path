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

def fac2dec(f: int, n:int) -> int:
    """
    the decimal value of a factorial number
    """
    # require: f is a factorial number
    
    d = 0
    q = f    # quotient
    m = 1    # multiplier

    for i in range(n):

        q = q // 10
        r = q % 10       # digit at position i
         
        d = d + r*m      # d = sum up to ith term 
        d = d + r*math.factorial(i)      # d = sum up to ith term 

        m = m * (i+1)    # next multiplier = (i+1)!

    return d
    # ensure: f is the factorial representation of d

def dec2fac(d: int, n:int) -> int:
    """
    the factorial representation of a decimal number
    """
    # require: d is a decimal number
    
    f = 0    # list of digits

    q = d     # quotient
    m = 1     # multiplier

    for i in range(n):

        r = q % (i+1)    # digit at position i

        f = r * m + f

        q = q // (i+1)    # next quotient
        m = m * 10        # next multiplier

    return f
    # ensure: f is the factorial representation of d

def encode(pi:list[int], n: int) -> list[int]:
    """
    the Lehmer code of pi
    """
    # require: pi in Pi^n

    rho = [0]*n

    for i in range(n):

        rho[i] = len([x for x in pi[(i+1):] if x < pi[i]])

    return rho
    # ensure: rho is the Lehmer code of pi

def decode(rho: list[int], n: int) -> list[int]:
    """
    the permutation in position r in lexorder
    """
    # require: rho a Lehmer code
    pi    = [0]*n
    alpha = list(range(n))

    for i in range(n):

        pi[i] = alpha.pop(rho[i])

    return pi
    # ensure: rho is the Lehmer code of pi

def numfy(pi:list[int], n: int) -> int:
    """
    numberfy the list pi
    """
    # require: for all i in [0:len(pi)), pi[i] in [0:9)
    r = 0

    cursor = len(pi)-n
    finish = len(pi)

    while cursor < finish:

        r = r * 10 + pi[cursor]

        cursor += 1

    return r
    # ensure: r is the numeric representation of pi[len(pi)-n:)

def rank(pi:list[int], n: int) -> int:
    """
    the position of a permutation in lexorder
    """
    # require: pi in Pi^n

    return fac2dec(numfy(encode(pi, n), n), n)
    # ensure: Pi^n_r = pi

def digify(r:int, n: int) -> list[int]:
    """
    split the number r into a list of its digits
    """
    # require: for all i in [0:len(pi)), pi[i] in [0:9)
    pi = [0]*n
    d  = r

    for i in reversed(range(n)):

        pi[i] = d % 10
        d     = d // 10

    return pi
    # ensure: r is the numeric representation of pi[len(pi)-n:)

def unrank(r: int, n: int) -> list[int]:
    """
    the permutation in position r in lexorder
    """
    # require: r in [0:n!)

    return decode(digify(dec2fac(r, n), n), n)
    # ensure: Pi^n_r = pi