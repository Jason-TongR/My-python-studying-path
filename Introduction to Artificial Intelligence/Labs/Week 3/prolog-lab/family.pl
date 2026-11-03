% Family relations.

% parent(P, C): P is a parent of C.
parent(tom, bob).
parent(tom, liz).
parent(pam, bob).
parent(bob, ann).
parent(bob, pat).
parent(liz, sue).
parent(pat, jim).

female(pam).
female(liz).
female(ann).
female(pat).
female(sue).
male(tom).
male(bob).
male(jim).

% grandparent(X, Z): X is a grandparent of Z.
grandparent(X, Z) :- parent(X, Y), parent(Y, Z).

% mother(X, Y): X is the mother of Y.
mother(X, Y) :- parent(X, Y), female(X).

% TODO 1: sibling(X, Y): X and Y have a parent in common, and are not the same person.
%         X \= Y means that X and Y cannot be unified.

% TODO 2: ancestor(X, Y): X is a parent of Y, or a parent of an ancestor of Y.

% TODO 3 (extra): cousin(X, Y): a parent of X and a parent of Y are siblings.
