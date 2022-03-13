import time

from nba_api.stats.endpoints import commonplayerinfo
from nba_api.stats.static import players

from players import players_full_dict, player_list, player_id_dict
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
    time.sleep(1.5)

    for active_player in active_players:
        if active_player["id"] in players_full_dict:
            # players_full_dict[active_player["id"]] = \
            #     search_player_info(player_id=active_player["id"], request_limit=1.5)
            player_list.add(active_player["full_name"])
            player_id_dict[active_player["full_name"]] = active_player["id"]
        else:
            player_info = commonplayerinfo.CommonPlayerInfo(player_id=active_player["id"]) \
                .get_normalized_dict()["CommonPlayerInfo"][0]
            time.sleep(1.5)
            if valid_player(player_info):
                players_full_dict[active_player["id"]] = \
                    search_player_info(player_id=active_player["id"],
                                       player_info=player_info,
                                       request_limit=1.5)
                player_list.add(active_player["full_name"])
                player_id_dict[active_player["full_name"]] = active_player["id"]

        temp_full_dict = players_full_dict
        temp_player_list = player_list
        temp_player_id_dict = player_id_dict

        with open("players.py", "w") as f:
            f.write("players_full_dict = " + str(temp_full_dict) + "\n\n" +
                    "player_list = " + str(temp_player_list) + "\n\n" +
                    "player_id_dict = " + str(temp_player_id_dict) + "\n")
            f.close()


if __name__ == '__main__':
    main()
