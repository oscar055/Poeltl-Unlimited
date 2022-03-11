import datetime
import os
from random import randint

import requests
from nba_api.stats.static import players, teams
from nba_api.stats.endpoints import commonplayerinfo, playercareerstats

import emoji

from variables import NBA_TEAM_ABBREVIATIONS, LOGO_URL, LOGO_LOCATION, NBA_TEAM_CONFERENCES, NBA_TEAM_DIVISIONS, \
    MAX_GUESSES, PARTIAL, CORRECT, WRONG


def get_path(path: str):
    return os.path.join(os.path.dirname(__file__), path)


def get_team_logo(abbr: str):
    with open(get_path(LOGO_LOCATION.format(abbr=abbr)), 'wb') as f:
        response = requests.get(LOGO_URL.format(abbr=abbr.lower()), stream=True)

        if not response.ok:
            print(response)

        for block in response.iter_content(1024):
            if not block:
                break

            f.write(block)


def generate_random_player_id():
    player_list = players.get_active_players()

    return player_list[randint(0, len(player_list))]["id"]


def search_player_info(player_id: int):
    player_info = commonplayerinfo.CommonPlayerInfo(player_id=player_id).get_normalized_dict()
    team_logo = get_path(LOGO_LOCATION.format(abbr=player_info["CommonPlayerInfo"][0]["TEAM_ABBREVIATION"]))

    birth_date = datetime.datetime.fromisoformat(player_info["CommonPlayerInfo"][0]["BIRTHDATE"][0:10])

    previous_teams = set()
    career_stats = playercareerstats.PlayerCareerStats(player_id=player_id).get_normalized_dict()
    for season in career_stats["SeasonTotalsRegularSeason"]:
        previous_teams.add(season["TEAM_ID"])
    previous_teams.remove(player_info["CommonPlayerInfo"][0]["TEAM_ID"])

    return {
        "id": player_id,
        "name": player_info["CommonPlayerInfo"][0]["DISPLAY_FIRST_LAST"],
        "team_abbr": player_info["CommonPlayerInfo"][0]["TEAM_ABBREVIATION"],
        "team_logo": team_logo,
        "team_id": player_info["CommonPlayerInfo"][0]["TEAM_ID"],
        "prev_teams": list(previous_teams),
        "conf": NBA_TEAM_CONFERENCES[player_info["CommonPlayerInfo"][0]["TEAM_ABBREVIATION"]],
        "div": NBA_TEAM_DIVISIONS[player_info["CommonPlayerInfo"][0]["TEAM_ABBREVIATION"]],
        "pos": player_info["CommonPlayerInfo"][0]["POSITION"],
        "ht": player_info["CommonPlayerInfo"][0]["HEIGHT"],
        "age": abs((datetime.datetime.now() - birth_date).days) // 365,
        "#": int(player_info["CommonPlayerInfo"][0]["JERSEY"])
    }


def search_player_by_name(player_name: str):
    return search_player_info(players.find_players_by_full_name(player_name)[0]["id"])


def search_team_info(team_abbreviation: str):
    return teams.find_team_by_abbreviation(team_abbreviation)


def search_team(team_id: int):
    return teams.find_team_name_by_id(team_id)


def height_to_int(height: str):
    foot, inches = height.split("-")

    return int(foot) * 12 + int(inches)


def compare_name(actual, expected):
    if actual["name"] == expected["name"]:
        return CORRECT
    return WRONG


def compare_team(actual, expected):
    if actual["team_id"] == expected["team_id"]:
        return CORRECT
    if expected["prev_teams"].__contains__(actual["team_id"]):
        return PARTIAL
    return WRONG


def compare_conf(actual, expected):
    if actual["conf"] == expected["conf"]:
        return CORRECT
    return WRONG


def compare_div(actual, expected):
    if actual["div"] == expected["div"]:
        return CORRECT
    return WRONG


def compare_pos(actual, expected):
    if actual["pos"] == expected["pos"]:
        return CORRECT
    if expected["pos"].__contains__(actual["pos"]) or actual["pos"].__contains__(expected["pos"]):
        return PARTIAL
    return WRONG


def compare_players(actual, expected):
    guess_result = "Name ({})".format(actual["name"])
    guess_result += compare_name(actual, expected)

    guess_result += "Team ({})".format(actual["team_abbr"])
    guess_result += compare_team(actual, expected)

    guess_result += "Conf ({})".format(actual["conf"])
    guess_result += compare_conf(actual, expected)

    guess_result += "Div ({})".format(actual["div"])
    guess_result += compare_div(actual, expected)

    guess_result += "Pos ({})".format(actual["pos"])
    guess_result += compare_pos(actual, expected)

    actual_height = height_to_int(actual["ht"])
    expected_height = height_to_int(expected["ht"])

    guess_result += "Ht"
    if actual_height == expected_height:
        guess_result += CORRECT
    else:
        if abs(actual_height - expected_height) <= 2:
            guess_result += PARTIAL
        else:
            guess_result += WRONG
        if actual_height < expected_height:
            guess_result += "{}↑".format(actual["ht"])
        else:
            guess_result += "{}↓".format(actual["ht"])

    guess_result += "Age"
    if actual["age"] == expected["age"]:
        guess_result += CORRECT
    else:
        if abs(actual["age"] - expected["age"]) <= 2:
            guess_result += PARTIAL
        else:
            guess_result += WRONG
        if actual["age"] < expected["age"]:
            guess_result += "{}↑".format(actual["age"])
        else:
            guess_result += "{}↓".format(actual["age"])

    guess_result += "#"
    if actual["#"] == expected["#"]:
        guess_result += CORRECT
    else:
        if abs(actual["#"] - expected["#"]) <= 2:
            guess_result += PARTIAL
        else:
            guess_result += WRONG
        if actual["#"] < expected["#"]:
            guess_result += "{}↑".format(actual["#"])
        else:
            guess_result += "{}↓".format(actual["#"])

    return guess_result


def score_guess(actual, expected):
    guess_result = ""
    guess_result += compare_name(actual, expected)

    guess_result += compare_team(actual, expected)

    guess_result += compare_conf(actual, expected)

    guess_result += compare_div(actual, expected)

    guess_result += compare_pos(actual, expected)

    if actual["ht"] == expected["ht"]:
        guess_result += CORRECT
    else:
        if abs(height_to_int(actual["ht"]) - height_to_int(expected["ht"])) <= 2:
            guess_result += PARTIAL
        else:
            guess_result += WRONG

    if actual["age"] == expected["age"]:
        guess_result += CORRECT
    else:
        if abs(actual["age"] - expected["age"]) <= 2:
            guess_result += PARTIAL
        else:
            guess_result += WRONG

    if actual["#"] == expected["#"]:
        guess_result += CORRECT
    else:
        if abs(actual["#"] - expected["#"]) <= 2:
            guess_result += PARTIAL
        else:
            guess_result += WRONG

    return guess_result + " " + actual["name"]


def game():
    player_id = generate_random_player_id()
    random_player = search_player_info(player_id=player_id)

    done = False

    while not done:
        guess_num = 1
        correct = False
        score = "-- {name} --\n".format(name=random_player["name"])

        while guess_num <= MAX_GUESSES:
            guess = input(f"Guess #{guess_num} of {MAX_GUESSES}: ")

            guessed_player = search_player_by_name(guess)

            print(emoji.emojize(compare_players(guessed_player, random_player)))

            score += score_guess(guessed_player, random_player) + "\n"

            if guessed_player == random_player:
                correct = True
                break

            guess_num += 1

        if correct:
            print("\nWell done!\n")
        else:
            print("\nBetter luck next time!\n")

        print("The correct answer was", random_player["name"], end="\n\n")

        print(emoji.emojize(score))

        play_again = input("Would you like to play again? (y/n): ")
        done = False if play_again == "y" else True


if __name__ == '__main__':
    game()
