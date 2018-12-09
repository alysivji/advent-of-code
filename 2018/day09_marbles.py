from collections import defaultdict, deque
import re
from typing import NamedTuple


class GameDetails(NamedTuple):
    num_players: int
    last_marble: int
    high_score: int = None


def play_game(num_players, last_marble):
    player_scores = {idx: 0 for idx in range(num_players)}

    # set up game
    circle = [0]
    curr_marble = 1
    curr_idx = 0
    curr_player = 0

    for _ in range(1, last_marble + 1):
        if curr_marble % 23 == 0:
            pos = (curr_idx - 7) % len(circle)

            player_scores[curr_player] += curr_marble
            removed_marble = circle.pop(pos)
            player_scores[curr_player] += removed_marble
        else:
            pos = (curr_idx + 2) % len(circle)
            if pos == 0:
                pos = len(circle)
            circle.insert(pos, curr_marble)

        curr_idx = pos
        curr_player = (curr_player + 1) % num_players
        curr_marble += 1

    return player_scores


def play_game_deque(num_players, last_marble):
    scores = defaultdict(int)
    circle = deque([0])
    curr_player = 1

    for marble in range(1, last_marble):
        if marble % 23 == 0:
            circle.rotate(7)
            scores[curr_player] += marble + circle.pop()
            circle.rotate(-1)
        else:
            circle.rotate(-1)
            circle.append(marble)
        curr_player = (curr_player + 1) % num_players

    return scores


high_score = lambda scores: max(val for key, val in scores.items())


TEST_INPUT = """10 players; last marble is worth 1618 points: high score is 8317
13 players; last marble is worth 7999 points: high score is 146373
17 players; last marble is worth 1104 points: high score is 2764
21 players; last marble is worth 6111 points: high score is 54718
30 players; last marble is worth 5807 points: high score is 37305""".split(
    "\n"
)

test_game_details = [
    GameDetails(*map(int, re.findall(r"-?\d+", line))) for line in TEST_INPUT
]

for game in test_game_details:
    result = play_game(game.num_players, game.last_marble)
    assert high_score(result) == game.high_score

    # result = play_game_deque(game.num_players, game.last_marble)
    # import pdb; pdb.set_trace()
    # assert high_score(result) == game.high_score


if __name__ == "__main__":
    with open("data/day09_input.txt", "r") as f:
        problem_input = f.read().strip()
    deets = GameDetails(*map(int, re.findall(r"-?\d+", problem_input)))
    print(high_score(play_game(deets.num_players, deets.last_marble)))

    print(high_score(play_game_deque(deets.num_players, deets.last_marble)))
    print(high_score(play_game_deque(deets.num_players, deets.last_marble * 100)))
