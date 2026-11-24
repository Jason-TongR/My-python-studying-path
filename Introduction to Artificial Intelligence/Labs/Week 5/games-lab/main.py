"""Run the lab's games and experiments.

    python main.py nim 20                     who wins Nim with 1 to 20 sticks, with perfect play
    python main.py tictactoe count            nodes visited by minimax and by alpha-beta
    python main.py tictactoe play             play tic-tac-toe against alpha-beta (you are O)
    python main.py tictactoe play first       ... and you move first (you are X)
    python main.py connect4 play 6            play Connect Four against depth-6 alpha-beta
    python main.py connect4 match 4           your evaluation against the center evaluation, depth 4
    python main.py connect4 play-timed 1      play against iterative deepening, 1 second per move
"""
import math
import random
import sys
import time

from connect4 import ConnectFour, center_evaluation, evaluation
from game import human_player, play
from nim import Nim
from search import (Counter, alphabeta, alphabeta_player, best_action, iterative_deepening_player,
                    minimax)
from tictactoe import TicTacToe


def nim_table(n: int) -> None:
    for sticks in range(1, n + 1):
        game = Nim(sticks)
        value = minimax(game, game.initial_state(), Counter())
        if value > 0:
            move = best_action(game, game.initial_state(), lambda s: minimax(game, s, Counter()))
            print(f"{sticks:3} sticks: the player to move wins, by taking {move}")
        else:
            print(f"{sticks:3} sticks: the player to move loses")


def tictactoe_count() -> None:
    plain = TicTacToe()
    ordered = TicTacToe([4, 0, 2, 6, 8, 1, 3, 5, 7])
    counter = Counter()
    start = time.time()
    value = minimax(plain, plain.initial_state(), counter)
    print(f"minimax:                           value {value:+.0f}, {counter.nodes:,} nodes ({time.time() - start:.2f} s)")
    for name, game in (("squares in order", plain), ("center and corners first", ordered)):
        counter = Counter()
        start = time.time()
        value = alphabeta(game, game.initial_state(), -math.inf, math.inf, counter)
        print(f"alpha-beta, {name:24} value {value:+.0f}, {counter.nodes:,} nodes ({time.time() - start:.2f} s)")


def tictactoe_play(human_first: bool) -> None:
    game = TicTacToe([4, 0, 2, 6, 8, 1, 3, 5, 7])
    you, computer = human_player(game), alphabeta_player(game)
    utility = play(game, you if human_first else computer, computer if human_first else you)
    yours = utility if human_first else -utility
    print("you win!" if yours > 0 else "a draw." if yours == 0 else "you lose.")


def connect4_play(depth: int, seconds: float | None = None) -> None:
    game = ConnectFour()
    computer = (alphabeta_player(game, depth, evaluation) if seconds is None
                else iterative_deepening_player(game, seconds, evaluation))
    first = input("do you want to move first? [y/n] ").strip().lower().startswith("y")
    you = human_player(game)
    utility = play(game, you if first else computer, computer if first else you)
    yours = utility if first else -utility
    print("you win!" if yours > 0 else "a draw." if yours == 0 else "you lose.")


def connect4_match(depth: int, openings: int = 20) -> None:
    """Your evaluation against center_evaluation, both at the same depth: each random opening
    (one random move each) is played twice, with the colors swapped."""
    game = ConnectFour()
    rng = random.Random(7)
    results = {"X": [0, 0, 0], "O": [0, 0, 0]}   # your wins, draws, losses, by your color
    for _ in range(openings):
        state = game.initial_state()
        for _ in range(2):
            state = game.result(state, rng.choice(game.actions(state)))
        for yours_is_x in (True, False):
            mine = alphabeta_player(game, depth, evaluation)
            theirs = alphabeta_player(game, depth, center_evaluation)
            utility = play(game, mine if yours_is_x else theirs, theirs if yours_is_x else mine,
                           start=state, verbose=False)
            yours = utility if yours_is_x else -utility
            results["X" if yours_is_x else "O"][0 if yours > 0 else 1 if yours == 0 else 2] += 1
    for color in ("X", "O"):
        w, d, l = results[color]
        print(f"your evaluation playing {color}: {w} wins, {d} draws, {l} losses")


def main(args: list[str]) -> None:
    if len(args) == 2 and args[0] == "nim":
        nim_table(int(args[1]))
    elif args == ["tictactoe", "count"]:
        tictactoe_count()
    elif len(args) in (2, 3) and args[:2] == ["tictactoe", "play"]:
        tictactoe_play(len(args) == 3 and args[2] == "first")
    elif len(args) == 3 and args[:2] == ["connect4", "play"]:
        connect4_play(int(args[2]))
    elif len(args) == 3 and args[:2] == ["connect4", "match"]:
        connect4_match(int(args[2]))
    elif len(args) == 3 and args[:2] == ["connect4", "play-timed"]:
        connect4_play(0, float(args[2]))
    else:
        print(__doc__)


if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except NotImplementedError as e:
        print("not implemented yet:", e)
    except (KeyboardInterrupt, EOFError):
        print()
