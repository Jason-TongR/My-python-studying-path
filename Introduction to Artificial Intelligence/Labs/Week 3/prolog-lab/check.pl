% check.pl: checks the exercises of the lab. Run it with:  swipl check.pl
% Each test stops after 2 seconds, so a predicate that loops is reported, not left running.
:- initialization(main, main).
:- use_module(library(time)).

main :-
    load(family, fam), load(lists, lst), load(jugs, jug),
    section("1. Family (family.pl)"),
    check("sibling(ann, X)", X1, fam:sibling(ann, X1), [pat]),
    check("sibling(bob, X)", X2, fam:sibling(bob, X2), [liz]),
    check("sibling(ann, ann) is false", yes, fam:sibling(ann, ann), []),
    check("all ancestors of jim", L1, fam:setof(A1, ancestor(A1, jim), L1), [[bob, pam, pat, tom]]),
    check("all descendants of tom", L2, fam:setof(D2, ancestor(tom, D2), L2), [[ann, bob, jim, liz, pat, sue]]),
    check("extra: cousin(ann, X)", L3, fam:setof(C3, cousin(ann, C3), L3), [[sue]]),
    section("2. Lists (lists.pl)"),
    check("last_of([a,b,c], X)", X4, lst:last_of([a,b,c], X4), [c]),
    check("prefix_of(P, [1,2])", P5, lst:prefix_of(P5, [1,2]), [[], [1], [1,2]]),
    check("member_of(X, [a,b,c])", X6, lst:member_of(X6, [a,b,c]), [a, b, c]),
    check("adjacent(X, Y, [1,2,3])", X7-Y7, lst:adjacent(X7, Y7, [1,2,3]), [1-2, 2-3]),
    section("3. Water jugs (jugs.pl)"),
    check("move(jugs(5, 0), pour12, S)", S8, (has_move(pour12), jug:move(jugs(5, 0), pour12, S8)), [jugs(2, 3)]),
    check("move(jugs(1, 3), pour21, S)", S9, (has_move(pour21), jug:move(jugs(1, 3), pour21, S9)), [jugs(4, 0)]),
    check("solve_id(jugs(0, 0), As): a shortest solution", N10,
          (once(jug:solve_id(jugs(0, 0), As10)), valid_jugs(As10), length(As10, N10)), [6]),
    nl.

load(File, Module) :-
    catch(load_files(File, [module(Module), if(true)]), E, (print_message(error, E), fail)), !.
load(File, _) :- format("could not load ~w.pl~n", [File]).

section(Title) :- format("~n~w~n", [Title]).

% check(Name, Template, Goal, Expected): all the answers of Goal (at most 20), as Template, are Expected.
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

% has_move(Action): move/3 has a clause for Action (else the exercise is not done yet).
has_move(Action) :-
    (   catch(clause(jug:move(_, Action, _), _), _, fail) -> true
    ;   format(atom(What), "move/3 for ~w", [Action]),
        throw(error(existence_error(procedure, What), _))
    ).

% Checks written independently of the lab's code.
valid_jugs(Actions) :- foldl(apply_action, Actions, 0-0, X-Y), (X =:= 4 ; Y =:= 4), !.
apply_action(fill1, _-Y, 5-Y).
apply_action(fill2, X-_, X-3).
apply_action(empty1, _-Y, 0-Y).
apply_action(empty2, X-_, X-0).
apply_action(pour12, X-Y, X1-Y1) :- T is min(X, 3 - Y), X1 is X - T, Y1 is Y + T.
apply_action(pour21, X-Y, X1-Y1) :- T is min(Y, 5 - X), X1 is X + T, Y1 is Y - T.
