# Lab: logic programming in Prolog

In this lab you write your first Prolog programs: relations about a family and about
lists, and the water jug problem as a search in a few lines.

## Getting started

You need SWI-Prolog 9 or later: download it from swi-prolog.org (Download, then Stable
release), or install it with `brew install swi-prolog` on macOS or
`sudo apt install swi-prolog` on Ubuntu.

```
swipl family.pl          start Prolog and load a file
?- parent(tom, X).       a query; it ends with a full stop
X = bob ;                type ; for another answer, or Enter to stop
?- make.                 reload the files you have changed
?- halt.                 quit
```

`swipl check.pl` checks every exercise and reports each test as OK, FAIL or not done
yet. It stops any test that runs for more than 2 seconds.

| File | What it contains | What you do |
|---|---|---|
| `family.pl` | facts about a family, and a few rules | write `sibling/2` and `ancestor/2` |
| `lists.pl` | `append/3` | write four predicates, one line each |
| `jugs.pl` | the water jug problem | write two moves, and iterative deepening |
| `check.pl` | tests for all the exercises | run it |

## Prolog in one table

| Prolog | Meaning |
|---|---|
| `parent(tom, bob).` | a fact |
| `h(X) :- b1(X), b2(X).` | h(X) is true if b1(X) and b2(X) are |
| `X`, `Ys`, `_` | variables: an uppercase letter or `_` first |
| `tom`, `[]` | constants, called atoms |
| `[1, 2, 3]`, `[H\|T]` | lists: H is the first element, and T the rest |
| `X = Y` | unify X and Y; this is not an assignment |
| `X is A + 1` | compute A + 1, and unify the result with X |
| `A =:= B`, `A =\= B`, `A < B` | compare numbers |
| `\+ G`, `X \= Y` | G cannot be proved; X and Y cannot be unified |
| `% ...` | a comment |

There are no functions and no return values: a function f(x) = y becomes a relation
`f(X, Y)`, which you can use in both directions.

## Exercises

1. **Family** (`family.pl`). Load the file and ask who Bob's children are, who Ann's
   grandparents are, and who is a mother. Then write `sibling/2` and `ancestor/2`.
   - Use `ancestor` in every direction: `ancestor(tom, X)`, `ancestor(X, jim)`,
     `ancestor(tom, jim)`.
   - In the recursive clause of `ancestor`, swap the two goals so that the recursive call
     comes first. What happens, and why? Then swap them back.
2. **Lists** (`lists.pl`). Write `last_of/2`, `prefix_of/2`, `member_of/2` and
   `adjacent/3`, each with a single call to `append/3` and no recursion. Try them in every
   direction: `prefix_of(P, [a,b,c])`, `adjacent(X, Y, [1,2,3])`, and `member_of(b, L)`.
   What happens in the last one?
3. **Water jugs** (`jugs.pl`). Write the moves `pour12` and `pour21`. Then:
   - Ask `solve(jugs(0, 0), As)`. What happens, and why?
   - Write `solve_id/2` and ask `solve_id(jugs(0, 0), As)`. Ask for more answers with `;`:
     what do you notice?
4. **If you have time.** Write `cousin/2` in `family.pl`: X and Y are cousins if a parent
   of X and a parent of Y are siblings.
