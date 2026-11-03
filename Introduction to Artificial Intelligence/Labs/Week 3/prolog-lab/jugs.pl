% The water jug problem: with jugs of 5 and 3 liters, measure exactly 4 liters.
% A state is jugs(X, Y): X liters in the 5-liter jug, Y liters in the 3-liter jug.

% move(State, Action, NextState)
move(jugs(_, Y), fill1,  jugs(5, Y)).
move(jugs(X, _), fill2,  jugs(X, 3)).
move(jugs(_, Y), empty1, jugs(0, Y)).
move(jugs(X, _), empty2, jugs(X, 0)).

% TODO 1: two more clauses of move/3, for the actions pour12 and pour21.
%         pour12 pours the 5-liter jug into the 3-liter one, until the first is empty or
%         the second is full; pour21 pours the other way.
%         Hint: T is min(X, 3 - Y) computes how many liters pour12 can pour.

goal(jugs(4, _)).
goal(jugs(_, 4)).

% solve(S, Actions): Actions is a list of actions that lead from S to a goal.
solve(S, []) :- goal(S).
solve(S, [A|As]) :- move(S, A, S1), solve(S1, As).

% TODO 2: solve_id(S, Actions): like solve, but trying shorter lists of actions first
%         (iterative deepening). One line: see the lecture.
