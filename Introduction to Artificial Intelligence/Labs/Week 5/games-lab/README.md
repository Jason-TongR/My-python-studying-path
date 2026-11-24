# Lab: adversarial search

In this lab you write alpha-beta search, play tic-tac-toe against your own program, and
give a Connect Four program an evaluation function.

You need Python 3.10 or later, and nothing else. Run the commands in this folder (on
some systems, type `python3` instead of `python`):

```
python main.py nim 20                  who wins Nim with 1 to 20 sticks, with perfect play
python main.py tictactoe count         nodes visited by minimax and by alpha-beta
python main.py tictactoe play          play tic-tac-toe against alpha-beta (you are O)
python main.py tictactoe play first    ... and you move first (you are X)
python main.py connect4 play 6         play Connect Four against depth-6 alpha-beta
python main.py connect4 match 4        your evaluation against the center evaluation, depth 4
python main.py connect4 play-timed 1   play against iterative deepening, 1 second per move
```

| File | What it contains | What you do |
|---|---|---|
| `game.py` | what a game is, players, and `play` | read it |
| `nim.py`, `tictactoe.py`, `connect4.py` | the three games | write `evaluation` in `connect4.py` |
| `search.py` | minimax (complete), alpha-beta, players | write `alphabeta` (and `iterative_deepening_player`) |
| `main.py` | runs the games and experiments | run it |

MAX is the player who moves first (X in tic-tac-toe and Connect Four), and utilities are
always for MAX: MAX wants them high, MIN wants them low. In every game an action is a
number: the sticks to take, the square (0 to 8), or the column (0 to 6).

## Exercises

1. **Nim.** Run `python main.py nim 20`. With which numbers of sticks does the player to
   move lose? Prove it. How should you play from 13 sticks?
2. **Alpha-beta.** Write `alphabeta` in `search.py`; `minimax`, just above it, is your
   model. Then run `python main.py tictactoe count`.
   - How many nodes do minimax and alpha-beta visit? Do they find the same value?
   - Why does the order in which the squares are tried change the number of nodes?
3. **Play tic-tac-toe.** Run `python main.py tictactoe play`, and
   `python main.py tictactoe play first`. Can you win? Why not?
4. **Connect Four.** Write `evaluation` in `connect4.py`. Play against it with
   `python main.py connect4 play 6`, then test it with `python main.py connect4 match 4`,
   which plays 40 games against `center_evaluation`. Can you make yours win most of them?
5. **If you have time.**
   - Write `iterative_deepening_player` in `search.py`, and play against it with
     `python main.py connect4 play-timed 1`. How deep does it search in one second?
   - Read `utility` in `connect4.py`: why is a win worth more when more squares are empty?
     What would go wrong without it?
