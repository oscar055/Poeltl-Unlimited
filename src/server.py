import os

from flask import Flask, url_for, render_template, redirect
from flask_restful import Api

from api import SearchForPlayer, GenerateRandomPlayerInfo, GenerateRandomTeamInfo, SearchForTeam
from game import Game
from players import player_list

app = Flask(__name__)
api = Api(app)

api.add_resource(SearchForPlayer, "/player/<int:player_id>")
api.add_resource(SearchForTeam, "/team/<int:team_id>")
api.add_resource(GenerateRandomPlayerInfo, "/info")
api.add_resource(GenerateRandomTeamInfo, "/team")

game = Game()


@app.route('/')
def render_main_page():
    return render_template("mainpage.html",
                           data=game.guesses,
                           input_enabled=game.input_enabled,
                           guess_num=game.get_guess_num(),
                           player_list=player_list)


@app.route('/guess/<int:player_id>', methods=["POST"])
def render_main_page_guess(self, player_id: int):
    self.game.guess(player_id)

    return redirect(url_for('render_main_page'))


@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)


def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)


if __name__ == '__main__':
    override_url_for('static', filename='mainpage.css')

    app.run(debug=True)
