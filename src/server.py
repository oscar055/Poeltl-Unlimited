import os

from flask import Flask, url_for, render_template
from flask_restful import Api

from api import SearchForPlayer, GenerateRandomPlayer, GenerateRandomPlayerInfo, GenerateRandomTeamInfo, SearchForTeam, \
    SaveTeamLogo

app = Flask(__name__)
api = Api(app)

api.add_resource(SaveTeamLogo, "/logo/<string:team_abbr>")
api.add_resource(SearchForPlayer, "/player/<int:player_id>")
api.add_resource(SearchForTeam, "/team/<int:team_id>")
api.add_resource(GenerateRandomPlayer, "/player")
api.add_resource(GenerateRandomPlayerInfo, "/info")
api.add_resource(GenerateRandomTeamInfo, "/team")


@app.route('/')
def init():
    return render_template("mainpage.html")


@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)


def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path, endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)


if __name__ == '__main__':
    # Initialize Everything
    override_url_for('static', filename='mainpage.css')

    app.run(debug=True)
