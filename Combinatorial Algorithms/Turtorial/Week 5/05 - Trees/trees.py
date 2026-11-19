# A Very Basic Tree Library
#
# This file is part of the Winter 2026 edition of the Combinatorial Algorithms
# course taught at the Guangdong Technion Israel Institute of Technology, Shantou, China
#
# copyright (C) 2026 Valentin Cassano
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

def height(tree:list) -> int:
    """
    the height of a tree
    """
    # require: true
    h = 0

    if len(tree) > 1: # tree is not a leaf

        children = tree[1:] # list of children

        for child in children:
            
            h = max(h, height(child))

        h = 1+h

    return h
    # ensure: h is the height of subtree rooted at v

def size(tree:list) -> int:
    """
    the size of a tree
    """
    # require: true
    s = 0

    if len(tree) > 1: # tree is not a leaf

        children = tree[1:] # list of children

        for child in children:
            
            s += size(child)

    return 1+s
    # ensure: h is the height of subtree rooted at v

def parents(tree:list, p:int = 0, pi:list[int] = []) -> list[int]:
    """
    the parents list of a tree with n nodes
    """
    # require: true

    if not pi: # pi == [] start of the recursion

        pi = [0]*size(tree)
        pi = parents(tree, 0, pi)

    else:

        pi[tree[0]] = p

        if len(tree) != 1: # tree is not a leaf

            children = tree[1:]
    
            for child in children:
    
                parents(child, tree[0], pi)

    return pi
    # ensure: for all i in [0:n), pi[i] is the parent of i