% Lecture 3, slide 8: one definition, many uses.

append([], Ys, Ys).
append([X|Xs], Ys, [X|Zs]) :- append(Xs, Ys, Zs).
