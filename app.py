from flask import Flask, render_template

app = Flask(__name__)
from utils.home_stats import get_home_stats

from flask import request
from utils.team_analytics import get_teams, get_team_stats

from utils.players_analytics import get_players, get_player_stats
from utils.h2h_analytics import (
    get_teams,
    get_h2h_stats
)
from utils.match_insights import (
    get_seasons,
    get_season_stats,
    get_season_top_performers,
    get_team_season_stats,
    get_team_top_performers
)

@app.route('/')
def home():
    stats = get_home_stats()
    print(stats)
    return render_template('index.html', stats=stats)
# @app.route('/')
# def home():
#     return render_template('index.html')
from utils.team_analytics import (
    get_teams,
    get_team_stats,
    get_team_venue_stats
)

@app.route('/teams', methods=['GET', 'POST'])
def teams():

    teams = get_teams()

    stats = None
    venue_stats = None

    selected_team = None
    selected_venue = None

    if request.method == "POST":

        selected_team = request.form["team"]

        stats = get_team_stats(selected_team)

        selected_venue = request.form.get("venue")

        if selected_venue:

            venue_stats = get_team_venue_stats(
                selected_team,
                selected_venue
            )

    return render_template(
        "teams.html",
        teams=teams,
        stats=stats,
        venue_stats=venue_stats,
        selected_team=selected_team,
        selected_venue=selected_venue
    )
from utils.players_analytics import get_players, get_player_stats

@app.route('/players', methods=['GET', 'POST'])
def players():

    players = get_players()

    stats = None
    selected_player = None

    if request.method == 'POST':

        selected_player = request.form['player']

        # Case-insensitive search
        player_map = {
            p.lower(): p
            for p in players
        }

        actual_player = player_map.get(
            selected_player.lower()
        )

        if actual_player:
            stats = get_player_stats(actual_player)

    return render_template(
        'players.html',
        players=players,
        stats=stats,
        selected_player=selected_player
    )
from utils.h2h_analytics import (
    get_teams,
    get_h2h_stats
)

@app.route('/h2h', methods=['GET', 'POST'])
def h2h():

    teams = get_teams()

    overall_stats = None
    venue_stats = None

    team1 = None
    team2 = None

    selected_venue = "All"

    if request.method == 'POST':

        team1 = request.form['team1']
        team2 = request.form['team2']

        selected_venue = request.form.get(
            'venue',
            'All'
        )

        overall_stats = get_h2h_stats(
            team1,
            team2
        )

        if selected_venue != "All":

            venue_stats = get_h2h_stats(
                team1,
                team2,
                selected_venue
            )

    return render_template(
        "h2h.html",
        teams=teams,
        overall_stats=overall_stats,
        venue_stats=venue_stats,
        team1=team1,
        team2=team2,
        selected_venue=selected_venue
    )
from utils.match_insights import (
    get_seasons,
    get_season_stats,
    get_season_top_performers,
    get_team_season_stats,
    get_team_top_performers
)

@app.route('/match-insights', methods=['GET', 'POST'])
def match_insights():

    seasons = get_seasons()

    stats = None
    season_performers = None

    team_stats = None
    team_performers = None

    selected_season = None
    selected_team = None

    if request.method == "POST":

        selected_season = request.form["season"]

        stats = get_season_stats(
            selected_season
        )

        season_performers = get_season_top_performers(
            selected_season
        )

        selected_team = request.form.get(
            "team"
        )

        if selected_team:

            team_stats = get_team_season_stats(
                selected_team,
                selected_season
            )

            team_performers = get_team_top_performers(
                selected_team,
                selected_season
            )

    return render_template(
        "match_insights.html",
        seasons=seasons,
        stats=stats,
        season_performers=season_performers,
        team_stats=team_stats,
        team_performers=team_performers,
        selected_season=selected_season,
        selected_team=selected_team
    )
@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == "__main__":
    app.run(debug=True)