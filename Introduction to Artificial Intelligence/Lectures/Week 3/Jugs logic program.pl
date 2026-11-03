% Lecture 3, slides 23 and 24: the water jugs, and search for free.

% A state is jugs(X, Y): X liters in the 5-liter jug, Y in the 3-liter jug.
move(jugs(X, Y), fill1,  jugs(5, Y)):- X < 5.
move(jugs(X, Y), fill2,  jugs(X, 3)):- Y < 3.
move(jugs(X, Y), empty1, jugs(0, Y)):- X > 0.
move(jugs(X, Y), empty2, jugs(X, 0)):- Y > 0.
move(jugs(X, Y), pour12, jugs(X1, Y1)) :- T is min(X, 3 - Y), X1 is X - T, Y1 is Y + T.
move(jugs(X, Y), pour21, jugs(X1, Y1)) :- T is min(Y, 5 - X), X1 is X + T, Y1 is Y - T.

goal(jugs(4, _)).
goal(jugs(_, 4)).

solve(S, []) :- goal(S).
solve(S, [A|As]) :- move(S, A, S1), solve(S1, As).

solve_id(S, As) :- length(As, _), solve(S, As).
