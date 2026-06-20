from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():

    teams = [
        {"name": "Chennai Super Kings", "logo": "CSK.png"},
        {"name": "Mumbai Indians", "logo": "MI.jpg"},
        {"name": "Royal Challengers Bengaluru", "logo": "RCB.jpg"},
        {"name": "Kolkata Knight Riders", "logo": "KKR.png"}
    ]

    winners = [
        {"year": 2025, "team": "Royal Challengers Bengaluru", "logo": "RCB.jpg"},
        {"year": 2024, "team": "Kolkata Knight Riders", "logo": "KKR.png"},
        {"year": 2023, "team": "Chennai Super Kings", "logo": "CSK.png"},
        {"year": 2022, "team": "Gujarat Titans", "logo": "GT.jpg"}
    ]

    return render_template(
        "index.html",
        teams=teams,
        winners=winners,
        total_matches=1095,
        total_players=900,
        total_venues=50,
        total_seasons=18
    )


@app.route("/teams")
def teams():

    teams = [
        {
            "code": "CSK",
            "name": "Chennai Super Kings",
            "logo": "CSK.png"
        },
        {
            "code": "MI",
            "name": "Mumbai Indians",
            "logo": "MI.jpg"
        },
        {
            "code": "RCB",
            "name": "Royal Challengers Bengaluru",
            "logo": "RCB.jpg"
        },
        {
            "code": "KKR",
            "name": "Kolkata Knight Riders",
            "logo": "KKR.png"
        },
        {
            "code": "SRH",
            "name": "Sunrisers Hyderabad",
            "logo": "SRH.png"
        },
        {
            "code": "RR",
            "name": "Rajasthan Royals",
            "logo": "RR.jpg"
        },
        {
            "code": "DC",
            "name": "Delhi Capitals",
            "logo": "DC.png"
        },
        {
            "code": "PBKS",
            "name": "Punjab Kings",
            "logo": "PBKS.jpg"
        },
        {
            "code": "LSG",
            "name": "Lucknow Super Giants",
            "logo": "LSG.jpg"
        },
        {
            "code": "GT",
            "name": "Gujarat Titans",
            "logo": "GT.jpg"
        }
    ]

    team_data = {

        "code": "CSK",
        "name": "Chennai Super Kings",
        "logo": "CSK.png",
        "established": "2008",

        "matches": 234,
        "wins": 140,
        "losses": 90,
        "win_pct": 59.83,

        "bat_avg": 29.42,
        "strike_rate": 137.25,
        "bowl_avg": 26.18,
        "economy": 8.35,
        "fielding_pct": 84.67,

        "recent_match": {
            "team_score": "215/7",
            "opp_score": "137/9",
            "opponent": "DC",
            "opp_logo": "DC.png",
            "result": "Won by 78 Runs"
        },

        "records": {
            "highest_total": "246/5",
            "lowest_total": "79/10",
            "most_runs": "6243",
            "best_bowling": "5/18",
            "most_wickets": "140"
        },

        "batting": {

            "players": [
                "Ruturaj Gaikwad",
                "Shivam Dube",
                "Rachin Ravindra",
                "MS Dhoni",
                "R Jadeja"
            ],

            "runs": [583, 396, 222, 161, 255],
            "average": [53.0, 38.2, 35.1, 40.2, 28.3],
            "strike_rate": [145, 162, 141, 220, 136],
            "fifties": [4, 2, 1, 0, 1],
            "hundreds": [1, 0, 0, 0, 0],
            "fours": [58, 32, 24, 12, 18],
            "sixes": [24, 28, 10, 12, 9]

        },

        "bowling": {

            "players": [
                "Pathirana",
                "Mustafizur",
                "Jadeja",
                "Theekshana",
                "Chahar"
            ],

            "wickets": [19, 14, 12, 11, 10],
            "average": [18.2, 22.1, 24.5, 26.1, 28.2],
            "economy": [7.8, 8.0, 7.4, 8.2, 8.5],
            "strike_rate": [13.4, 16.8, 18.5, 19.2, 20.4],
            "maidens": [1, 0, 1, 0, 0],
            "four_wickets": [2, 1, 0, 0, 0],
            "five_wickets": [1, 0, 0, 0, 0]

        }
    }

    return render_template(
        "teams.html",
        teams=teams,
        team_data=team_data
    )


@app.route("/players")
def players():
    return "<h1>Players Page Coming Soon</h1>"


@app.route("/h2h")
def h2h():
    return "<h1>Head-to-Head Analytics Coming Soon</h1>"


@app.route("/match-insights")
def match_insights():
    return "<h1>Match Insights Coming Soon</h1>"


@app.route("/about")
def about():
    return "<h1>About Page Coming Soon</h1>"


if __name__ == "__main__":
    app.run(debug=True)