% Lecture 3, slides 21 and 22: paths in a graph with a cycle.

edge(a, b).
edge(b, c).
edge(c, a).
edge(c, d).

path(X, Y) :- edge(X, Y).
path(X, Y) :- edge(X, Z), path(Z, Y).

path(X, Y, Path) :- walk(X, Y, [X], Reversed), reverse(Reversed, Path).

walk(X, X, Visited, Visited).
walk(X, Y, Visited, Path) :-
    edge(X, Z), \+ member(Z, Visited),
    walk(Z, Y, [Z|Visited], Path).
