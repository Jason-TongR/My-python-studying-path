% Lists with append/3.

% append(Xs, Ys, Zs): Zs is the list Xs followed by the list Ys.
append([], Ys, Ys).
append([X|Xs], Ys, [X|Zs]) :- append(Xs, Ys, Zs).

% Write each of these with ONE call to append/3, and no recursion.

% TODO 1: last_of(Xs, X): X is the last element of the list Xs.

% TODO 2: prefix_of(P, Xs): the list P is a prefix of the list Xs.

% TODO 3: member_of(X, Xs): X is an element of the list Xs.

% TODO 4: adjacent(X, Y, Xs): X and Y are next to each other in Xs, X first.
