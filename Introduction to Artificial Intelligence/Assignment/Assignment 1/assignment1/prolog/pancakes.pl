% The pancake problem in Prolog. A stack is a list of pancake sizes, the top first:
% [3, 1, 2] has pancake 3 on top. It is sorted when the sizes increase downwards.

% TODO: flip(K, Stack, Flipped): Flipped is Stack with its top K pancakes in reverse
%       order. Use length/2, append/3 and reverse/2.

% TODO: move(Stack, flip(K), Next): Next is Stack after flipping its top K pancakes, for
%       every K from 2 to the number of pancakes. Hint: between/3.

% sorted_stack(Stack): the sizes increase from the top down.
sorted_stack(Stack) :- msort(Stack, Stack).

% TODO: solve(Stack, Moves): Moves is a list of moves that sorts Stack (depth-first).

% TODO: solve_id(Stack, Moves): like solve, but trying shorter lists of moves first
%       (iterative deepening).

% TODO: gaps(Stack, G): G is the number of gaps in Stack, with the plate counting as a
%       pancake of size N + 1 under the stack: the gap heuristic of part B.
