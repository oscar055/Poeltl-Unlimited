from flask_restful import Resource

from poeltl import generate_random_player_id, search_player_info, search_team_info, search_team, get_team_logo


class SearchForPlayer(Resource):
    def get(self, player_id):
        return search_player_info(player_id)


class SearchForTeam(Resource):
    def get(self, team_id):
        return search_team(team_id)


class GenerateRandomPlayer(Resource):
    def get(self):
        return generate_random_player_id()


class GenerateRandomPlayerInfo(Resource):
    def get(self):
        return search_player_info(generate_random_player_id())


class GenerateRandomTeamInfo(Resource):
    def get(self):
        return search_team_info(
            search_player_info(generate_random_player_id())["team_abbr"])


class SaveTeamLogo(Resource):
    def get(self, team_abbr):
        get_team_logo(abbr=team_abbr.lower())

        return {1: "success"}

