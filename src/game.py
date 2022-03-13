from random import choice

from players import players_full_dict
from variables import PARTIAL, WRONG, CORRECT


def generate_random_player():
    return players_full_dict[choice(list(players_full_dict.keys()))]


def convert_height(height: str) -> str:
    feet, inches = height.split("-")

    return feet + "'" + inches + "\""


def height_to_inches(height: str) -> int:
    height_split = height[:-1].split("'")

    return int(height_split[0]) * 12 + int(height_split[1])


def height_difference(positive: str, negative: str):
    return height_to_inches(positive) - height_to_inches(negative)


class Game:
    guess_num: int
    correct: bool
    score: str

    player: dict
    guesses: dict

    input_enabled: bool

    def __init__(self):
        self.guesses = {}
        self.guess_num = 1
        self.correct = False

        self.player = generate_random_player()
        self.player["ht"] = convert_height(self.player["ht"])

        self.score = "{name}\n".format(name=self.player["name"])

        self.input_enabled = True

    def guess(self, player_id: int):
        self.guesses[str(self.guess_num)] = players_full_dict[player_id]
        self.guesses[str(self.guess_num)]["ht"] = convert_height(self.guesses[str(self.guess_num)]["ht"])

        self.score += self.score_guess(self.guesses[str(self.guess_num)])

        if self.guesses[str(self.guess_num)]["id"] == self.player["id"]:
            self.input_enabled = False
            correct = True
        else:
            self.guess_num += 1

    def check_name(self):
        if self.guesses[str(self.guess_num)]["name"] == self.player["name"]:
            self.guesses[str(self.guess_num)]["name_accuracy"] = "green"
            return CORRECT

        self.guesses[str(self.guess_num)]["name_accuracy"] = ""
        return WRONG

    def check_team(self):
        if self.guesses[str(self.guess_num)]["team"] == self.player["team"]:
            self.guesses[str(self.guess_num)]["team_accuracy"] = "green"
            return CORRECT

        if self.player["prev_teams"].__contains__(self.guesses[str(self.guess_num)]["team_id"]):
            self.guesses[str(self.guess_num)]["team_accuracy"] = "yellow"
            return PARTIAL

        self.guesses[str(self.guess_num)]["team_accuracy"] = ""
        return WRONG

    def check_conf(self):
        if self.guesses[str(self.guess_num)]["conf"] == self.player["conf"]:
            self.guesses[str(self.guess_num)]["conf_accuracy"] = "green"
            return CORRECT

        self.guesses[str(self.guess_num)]["conf_accuracy"] = ""
        return WRONG

    def check_div(self):
        if self.guesses[str(self.guess_num)]["div"] == self.player["div"]:
            self.guesses[str(self.guess_num)]["div_accuracy"] = "green"
            return CORRECT

        self.guesses[str(self.guess_num)]["div_accuracy"] = ""
        return WRONG

    def check_pos(self):
        if self.guesses[str(self.guess_num)]["pos"] == self.player["pos"]:
            self.guesses[str(self.guess_num)]["pos_accuracy"] = "green"
            return CORRECT

        self.guesses[str(self.guess_num)]["pos_accuracy"] = ""
        return WRONG

    def check_ht(self):
        if self.guesses[str(self.guess_num)]["ht"] == self.player["ht"]:
            self.guesses[str(self.guess_num)]["ht_accuracy"] = "green"
            return CORRECT

        if height_to_inches(self.guesses[str(self.guess_num)]["ht"]) < height_to_inches(self.player["ht"]):
            self.guesses[str(self.guess_num)]["ht_direction"] = "↑"
        else:
            self.guesses[str(self.guess_num)]["ht_direction"] = "↓"

        if abs(height_difference(self.guesses[str(self.guess_num)]["ht"], self.player["ht"])) <= 2:
            self.guesses[str(self.guess_num)]["ht_accuracy"] = "yellow"
            return PARTIAL

        self.guesses[str(self.guess_num)]["ht_accuracy"] = ""
        return WRONG

    def check_age(self):
        if self.guesses[str(self.guess_num)]["age"] == self.player["age"]:
            self.guesses[str(self.guess_num)]["age_accuracy"] = "green"
            return CORRECT

        if self.guesses[str(self.guess_num)]["age"] < self.player["age"]:
            self.guesses[str(self.guess_num)]["age_direction"] = "↑"
        else:
            self.guesses[str(self.guess_num)]["age_direction"] = "↓"

        if abs(self.guesses[str(self.guess_num)]["age"] - self.player["age"]) <= 2:
            self.guesses[str(self.guess_num)]["age_accuracy"] = "yellow"
            return PARTIAL

        self.guesses[str(self.guess_num)]["age_accuracy"] = ""
        return WRONG

    def check_num(self):
        if self.guesses[str(self.guess_num)]["num"] == self.player["num"]:
            self.guesses[str(self.guess_num)]["num_accuracy"] = "green"
            return CORRECT

        if self.guesses[str(self.guess_num)]["num"] < self.player["num"]:
            self.guesses[str(self.guess_num)]["num_direction"] = "↑"
        else:
            self.guesses[str(self.guess_num)]["ht_direction"] = "↓"

        if abs(self.guesses[str(self.guess_num)]["num"] - self.player["num"]) <= 2:
            self.guesses[str(self.guess_num)]["num_accuracy"] = "yellow"
            return PARTIAL

        self.guesses[str(self.guess_num)]["num_accuracy"] = ""
        return WRONG

    def get_guess_num(self):
        return self.guess_num

    def get_score(self):
        return self.score

    def score_guess(self, guess: dict):
        self.score += self.check_name() + \
                      self.check_team() + \
                      self.check_conf() + \
                      self.check_div() + \
                      self.check_pos() + \
                      self.check_ht() + \
                      self.check_age() + \
                      self.check_num()

        return self.score + " " + guess["name"]
