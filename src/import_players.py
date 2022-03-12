import time

from nba_api.stats.endpoints import commonplayerinfo
from nba_api.stats.static import players
from requests import ReadTimeout

from poeltl import search_player_info


def valid_player(player_info: dict):
    return player_info["DISPLAY_FIRST_LAST"] != "" \
           and player_info["BIRTHDATE"] != "" \
           and player_info["HEIGHT"] != "" \
           and player_info["JERSEY"] != "" \
           and player_info["POSITION"] != "" \
           and player_info["TEAM_ID"] != "" \
           and player_info["TEAM_ABBREVIATION"] != ""


def main():
    active_players = players.get_active_players()

    with open("players.py", "w") as f:
        f.write("player_list = {\n")

        for active_player in active_players:
            while True:
                try:
                    player_info = commonplayerinfo.CommonPlayerInfo(player_id=active_player["id"]) \
                        .get_normalized_dict()["CommonPlayerInfo"][0]
                except ReadTimeout:
                    continue
                else:
                    if valid_player(player_info):
                        break

            player = search_player_info(active_player["id"], player_info, 5)

            # Write to file
            f.write("\t" + str(active_player["id"]) + ": " + str(player) + ",\n")

            print(player)

            time.sleep(5)

        f.write("}\n")
        f.close()


if __name__ == '__main__':
    main()
