from flask import Flask, render_template

app = Flask(__name__)
from utils.home_stats import get_home_stats

from flask import request
from utils.team_analytics import get_teams, get_team_stats


@app.route('/')
def home():
    stats = get_home_stats()
    print(stats)
    return render_template('index.html', stats=stats)
# @app.route('/')
# def home():
#     return render_template('index.html')

@app.route('/teams', methods=['GET', 'POST'])
def team():

    teams = get_teams()
    stats = None
cd
    if request.method == 'POST':
        selected_team = request.form['team']
        stats = get_team_stats(selected_team)

    return render_template(
        'teams.html',
        teams=teams,
        stats=stats
    )

@app.route('/players')
def players():
    return render_template('players.html')

@app.route('/h2h')
def h2h():
    return render_template('h2h.html')

@app.route('/match-insights')
def match_insights():
    return render_template('match_insights.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == "__main__":
    app.run(debug=True)