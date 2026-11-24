% check.pl: checks part D. Run it in this folder with:  swipl check.pl
% Each test stops after 2 seconds, so a predicate that loops is reported, not left running.
:- initialization(main, main).
:- use_module(library(time)).

main :-
    catch(load_files(pancakes, [module(p), if(true)]), E, (print_message(error, E), fail)),
    format("~nPart D (pancakes.pl)~n"),
    check("flip(2, [3,1,2], X)", X1, p:flip(2, [3,1,2], X1), [[1,3,2]]),
    check("flip(3, [3,1,2], X)", X2, p:flip(3, [3,1,2], X2), [[2,1,3]]),
    check("flip backwards: flip(2, X, [1,3,2])", X3, p:flip(2, X3, [1,3,2]), [[3,1,2]]),
    check("moves of [3,1,2,4]", M4-N4, p:move([3,1,2,4], M4, N4),
          [flip(2)-[1,3,2,4], flip(3)-[2,1,3,4], flip(4)-[4,2,1,3]]),
    check("a sorted stack needs no moves", M5, once(p:solve_id([1,2,3], M5)), [[]]),
    check("solve_id finds fewest flips: [3,1,2]", L6, (once(p:solve_id([3,1,2], M6)), length(M6, L6)), [2]),
    check("solve_id finds fewest flips: [2,4,1,3]", L7, (once(p:solve_id([2,4,1,3], M7)), length(M7, L7)), [4]),
    check("solve_id finds fewest flips: [3,1,5,2,4]", L8, (once(p:solve_id([3,1,5,2,4], M8)), length(M8, L8)), [5]),
    check("solve_id's moves sort the stack", ok, (once(p:solve_id([6,2,4,1,5,3], M9)), apply_moves([6,2,4,1,5,3], M9, S9),
          S9 == [1,2,3,4,5,6], length(M9, 6)), [ok]),
    check("gaps([1,2,3,4], G)", G10, p:gaps([1,2,3,4], G10), [0]),
    check("gaps([4,3,2,1], G)", G11, p:gaps([4,3,2,1], G11), [1]),
    check("gaps([2,4,1,3], G)", G12, p:gaps([2,4,1,3], G12), [4]),
    nl.

% apply_moves(Stack, Moves, Result): independent of the code being checked.
apply_moves(S, [], S).
apply_moves(S, [flip(K)|Ms], R) :- length(T, K), append(T, Rest, S), reverse(T, RT), append(RT, Rest, S1), apply_moves(S1, Ms, R).

check(Name, Template, Goal, Expected) :-
    catch(call_with_time_limit(2, findall(Template, limit(20, Goal), Got)), E, true),
    (   var(E), Got == Expected -> format("  OK            ~w~n", [Name])
    ;   nonvar(E), E = error(existence_error(procedure, PI0), _) ->
        ( PI0 = _:PI -> true ; PI = PI0 ),
        format("  not done yet  ~w   (~w is not defined)~n", [Name, PI])
    ;   E == time_limit_exceeded -> format("  FAIL          ~w   (still running after 2 seconds: does it loop?)~n", [Name])
    ;   nonvar(E) -> format("  FAIL          ~w   (error: ~q)~n", [Name, E])
    ;   format("  FAIL          ~w   (expected ~q, got ~q)~n", [Name, Expected, Got])
    ).
