from flask import (
    Flask,
    render_template,
    url_for,
    request,
    redirect
)
import pandas as pd

import pandas as pd
app = Flask(__name__)

# ==========================================
# LOAD DATASET
# ==========================================

try:
    df = pd.read_csv(
        "data/IPL.csv",
        low_memory=False
    )

    print("IPL Dataset Loaded Successfully")
    TEAM_MAPPING = {
    "Deccan Chargers": "Sunrisers Hyderabad",
    "Delhi Daredevils": "Delhi Capitals",
    "Kings XI Punjab": "Punjab Kings",
    "Royal Challengers Bangalore": "Royal Challengers Bengaluru"
}

    if not df.empty:
      df["batting_team"] = df["batting_team"].replace(TEAM_MAPPING)
      df["bowling_team"] = df["bowling_team"].replace(TEAM_MAPPING)


except Exception as e:

    print("Dataset Error:", e)
    df = pd.DataFrame()

# ==========================================
# TEAM LOGOS
# ==========================================
df["match_won_by"] = (
    df["match_won_by"]
    .replace(TEAM_MAPPING)
)
LOGO_MAP = {
    "Chennai Super Kings": "CSK.png",
    "Mumbai Indians": "MI.jpg",
    "Royal Challengers Bengaluru": "RCB.jpg",
    "Royal Challengers Bangalore": "RCB.jpg",
    "Kolkata Knight Riders": "KKR.png",
    "Sunrisers Hyderabad": "SRH.png",
    "Rajasthan Royals": "RR.jpg",
    "Delhi Capitals": "DC.png",
    "Punjab Kings": "PBKS.jpg",
    "Kings XI Punjab": "PBKS.jpg",
    "Lucknow Super Giants": "LSG.jpg",
    "Gujarat Titans": "GT.jpg"
}
SHORT_NAMES = {
    "Chennai Super Kings": "CSK",
    "Mumbai Indians": "MI",
    "Royal Challengers Bengaluru": "RCB",
    "Kolkata Knight Riders": "KKR",
    "Sunrisers Hyderabad": "SRH",
    "Rajasthan Royals": "RR",
    "Delhi Capitals": "DC",
    "Punjab Kings": "PBKS",
    "Lucknow Super Giants": "LSG",
    "Gujarat Titans": "GT"
}
TEAM_NAME_MAP = {
    "CSK": "Chennai Super Kings",
    "MI": "Mumbai Indians",
    "RCB": "Royal Challengers Bengaluru",
    "KKR": "Kolkata Knight Riders",
    "SRH": "Sunrisers Hyderabad",
    "RR": "Rajasthan Royals",
    "DC": "Delhi Capitals",
    "PBKS": "Punjab Kings",
    "LSG": "Lucknow Super Giants",
    "GT": "Gujarat Titans"
}
RECENT_CHAMPIONS = [
    {
        "year": 2025,
        "team": "Royal Challengers Bengaluru",
        "logo": "RCB.jpg"
    },
    {
        "year": 2024,
        "team": "Kolkata Knight Riders",
        "logo": "KKR.png"
    },
    {
        "year": 2023,
        "team": "Chennai Super Kings",
        "logo": "CSK.png"
    },
    {
        "year": 2022,
        "team": "Gujarat Titans",
        "logo": "GT.jpg"
    }
]

# ==========================================
# HOME
# ==========================================

@app.route("/")
def home():

    if df.empty:

        return render_template(
            "index.html",
            total_matches=0,
            total_players=0,
            total_venues=0,
            total_seasons=0,
            teams=[],
            winners=[]
        )

    # KPI STATS

    total_matches = df["match_id"].nunique()

    total_players = pd.concat(
        [
            df["batter"],
            df["bowler"]
        ]
    ).dropna().nunique()

    total_venues = df["venue"].dropna().nunique()

    total_seasons = df["season"].dropna().nunique()

    # TEAMS

    CURRENT_TEAMS = [
    "Chennai Super Kings",
    "Mumbai Indians",
    "Royal Challengers Bengaluru",
    "Kolkata Knight Riders",
    "Sunrisers Hyderabad",
    "Rajasthan Royals",
    "Delhi Capitals",
    "Punjab Kings",
    "Lucknow Super Giants",
    "Gujarat Titans"
]

    team_names = sorted(
    [
        team for team in pd.concat(
            [
                df["batting_team"],
                df["bowling_team"]
            ]
        ).dropna().unique()
        if team in CURRENT_TEAMS
    ]
)

    teams = []

    for team in team_names:

        teams.append({
            "name": team,
            "logo": LOGO_MAP.get(
                team,
                "IPL1.jpg"
            )
        })

        
    return render_template(
      "index.html",
      teams=teams,
      winners=RECENT_CHAMPIONS,
      total_matches=total_matches,
      total_players=total_players,
      total_venues=total_venues,
      total_seasons=total_seasons
)
@app.route("/teams")
def teams():
    return team_details("CSK")


@app.route("/teams/<team>")
def team_details(team):

    team = TEAM_NAME_MAP.get(team, team)

    match_summary = df[
        [
            "match_id",
            "date",
            "venue",
            "batting_team",
            "bowling_team",
            "match_won_by",
            "win_outcome"
        ]
    ].drop_duplicates(subset=["match_id"])

    batting_df = df[df["batting_team"] == team]
    bowling_df = df[df["bowling_team"] == team]

    matches = match_summary[
        (match_summary["batting_team"] == team) |
        (match_summary["bowling_team"] == team)
    ].shape[0]

    wins = match_summary[
        match_summary["match_won_by"] == team
    ].shape[0]

    losses = matches - wins

    win_percentage = round(
        (wins / matches) * 100,
        2
    ) if matches else 0

    selected_team = {
        "name": team,
        "short_name": SHORT_NAMES.get(team, ""),
        "logo": LOGO_MAP.get(team, "IPL1.jpg"),
        "matches": matches,
        "wins": wins,
        "losses": losses,
        "win_percentage": win_percentage
    }

    total_runs = int(
        batting_df["batter_runs"].sum()
    )

    total_balls = int(
        batting_df["batter_balls"].sum()
    )

    strike_rate = round(
        (total_runs / total_balls) * 100,
        2
    ) if total_balls else 0

    runs_per_match = round(
        total_runs / matches,
        2
    ) if matches else 0

    innings_totals = batting_df.groupby(
        ["match_id", "innings"]
    )["runs_total"].sum()

    highest_total = int(
        innings_totals.max()
    ) if not innings_totals.empty else 0

    lowest_total = int(
        innings_totals[innings_totals > 0].min()
    ) if not innings_totals.empty else 0

    boundary_percentage = round(
        (
            batting_df["batter_runs"]
            .isin([4, 6])
            .sum()
            / len(batting_df)
        ) * 100,
        2
    ) if len(batting_df) else 0

    most_runs_scorer = (
        batting_df.groupby("batter")["batter_runs"]
        .sum()
        .idxmax()
        if not batting_df.empty else "-"
    )

    player_scores = batting_df.groupby(
        ["match_id", "batter"]
    )["batter_runs"].sum()

    centuries = int(
        (player_scores >= 100).sum()
    )

    batting = {
        "runs_per_match": runs_per_match,
				"total_runs": total_runs,
				"strike_rate": strike_rate,
				"highest_score": highest_total,
				"boundary_percentage": boundary_percentage,
				"most_runs": most_runs_scorer,
				"centuries": centuries
    }

    wickets = int(
        bowling_df["bowler_wicket"].sum()
    )

    balls = int(
        bowling_df["valid_ball"].sum()
    )

    overs = balls / 6 if balls else 0

    most_wicket_taker = (
        bowling_df.groupby("bowler")["bowler_wicket"]
        .sum()
        .idxmax()
        if not bowling_df.empty else "-"
    )

    bowling = {
        "average": round(
            bowling_df["runs_total"].sum() / wickets,
            2
        ) if wickets else 0,

        "economy": round(
            bowling_df["runs_total"].sum() / overs,
            2
        ) if overs else 0,

        "total_wickets": wickets,

        "dot_ball_percentage": round(
            (
                len(
                    bowling_df[
                        bowling_df["runs_total"] == 0
                    ]
                )
                / len(bowling_df)
            ) * 100,
            2
        ) if len(bowling_df) else 0,

        "strike_rate": round(
            balls / wickets,
            2
        ) if wickets else 0,

        "most_wickets": most_wicket_taker
    }

    records = {
        "highest_total": highest_total,
        "lowest_total": lowest_total,
        "most_runs": most_runs_scorer,
        "most_wickets": most_wicket_taker,
        "best_bowling": most_wicket_taker
    }
    team_matches = match_summary[
        (match_summary["batting_team"] == team) |
        (match_summary["bowling_team"] == team)
    ]

    if not team_matches.empty:

        team_matches = team_matches.copy()

        team_matches["date"] = pd.to_datetime(
            team_matches["date"],
            errors="coerce"
        )

        latest_match = team_matches.sort_values(
            "date",
            ascending=False
        ).iloc[0]

        opponent = (
            latest_match["bowling_team"]
            if latest_match["batting_team"] == team
            else latest_match["batting_team"]
        )

        recent_match = {
            "opponent": opponent,
            "venue": latest_match["venue"],
            "date": latest_match["date"].strftime("%d-%m-%Y"),
            "result": latest_match["win_outcome"]
        }

    else:

        recent_match = {
            "opponent": "-",
            "venue": "-",
            "date": "-",
            "result": "-"
        }

    teams = []

    for team_name in SHORT_NAMES.keys():

        teams.append({
            "name": team_name,
            "short_name": SHORT_NAMES[team_name],
            "logo": LOGO_MAP[team_name]
        })

    return render_template(
        "teams.html",
        teams=teams,
        selected_team=selected_team,
        batting=batting,
        bowling=bowling,
        records=records,
        recent_match=recent_match
    )

# ==========================================
# PLAYERS PAGE
# ==========================================
@app.route("/players")
def players():

    search = request.args.get(
        "search",
        ""
    ).strip()

    all_players = sorted(
        df["batter"]
        .dropna()
        .unique()
    )

    if search:

        matching_players = [
            p for p in all_players
            if search.lower() in p.lower()
        ]

        if matching_players:

            return redirect(
                url_for(
                    "player_details",
                    player=matching_players[0]
                )
            )

    return player_details("V Kohli")

@app.route("/players/<player>")
def player_details(player):

    batting_df = df[
        df["batter"] == player
    ].copy()

    bowling_df = df[
        df["bowler"] == player
    ].copy()

    # ==========================================
    # PLAYER OVERVIEW
    # ==========================================

    matches = batting_df["match_id"].nunique()

    total_runs = int(
        batting_df["runs_batter"].sum()
    )

    total_balls = int(
        batting_df["balls_faced"].sum()
    )

    dismissals = int(
        (df["player_out"] == player).sum()
    )

    average = round(
        total_runs / dismissals,
        2
    ) if dismissals else total_runs

    strike_rate = round(
        (total_runs / total_balls) * 100,
        2
    ) if total_balls else 0

    primary_team = "-"

    if not batting_df.empty:

        primary_team = batting_df[
            "batting_team"
        ].mode()[0]

    selected_player = {
    "name": player,
    "team": primary_team,
    "logo": LOGO_MAP.get(primary_team, "IPL1.jpg"),
    "matches": matches,
    "runs": total_runs,
    "average": average,
    "strike_rate": strike_rate
}
    # ==========================================
    # BATTING STATS
    # ==========================================

    innings_scores = batting_df.groupby(
        "match_id"
    )["runs_batter"].sum()

    highest_score = int(
        innings_scores.max()
    ) if not innings_scores.empty else 0

    fifties = int(
        (
            (innings_scores >= 50) &
            (innings_scores < 100)
        ).sum()
    )

    centuries = int(
        (innings_scores >= 100).sum()
    )

    batting = {
        "matches": matches,
        "runs": total_runs,
        "average": average,
        "strike_rate": strike_rate,
        "fifties": fifties,
        "centuries": centuries
    }

    # ==========================================
    # BOWLING STATS
    # ==========================================
    

    wickets = int(
        bowling_df["bowler_wicket"].sum()
    )

    runs_conceded = int(
        bowling_df["runs_bowler"].sum()
    )

    balls_bowled = int(
        bowling_df["valid_ball"].sum()
    )

    overs = balls_bowled / 6 if balls_bowled else 0

    bowling_average = round(
        runs_conceded / wickets,
        2
    ) if wickets else 0

    economy = round(
        runs_conceded / overs,
        2
    ) if overs else 0

    bowling_sr = round(
        balls_bowled / wickets,
        2
    ) if wickets else 0

    best_bowling = "-"
    five_wickets = 0

    if not bowling_df.empty:

        wickets_per_match = bowling_df.groupby(
            "match_id"
        )["bowler_wicket"].sum()

        five_wickets = int(
            (wickets_per_match >= 5).sum()
        )

        if not wickets_per_match.empty:

            best_match_id = wickets_per_match.idxmax()

            best_match_df = bowling_df[
                bowling_df["match_id"] == best_match_id
            ]

            best_wickets = int(
                best_match_df["bowler_wicket"].sum()
            )

            best_runs = int(
                best_match_df["runs_bowler"].sum()
            )

            best_bowling = f"{best_wickets}/{best_runs}"

    bowling = {
        "wickets": wickets,
        "average": bowling_average,
        "economy": economy,
        "strike_rate": bowling_sr,
        "best": best_bowling,
        "five_wickets": five_wickets
    }
    # ==========================================
    # SEASON WISE STATS
    # ==========================================

    season_stats = []

    for season in sorted(
        batting_df["season"]
        .dropna()
        .unique(),
        reverse=True
    ):

        season_df = batting_df[
            batting_df["season"] == season
        ]

        season_runs = int(
            season_df["runs_batter"].sum()
        )

        season_balls = int(
            season_df["balls_faced"].sum()
        )

        season_matches = season_df[
            "match_id"
        ].nunique()

        season_dismissals = df[
            (df["season"] == season) &
            (df["player_out"] == player)
        ].shape[0]

        season_scores = season_df.groupby(
            "match_id"
        )["runs_batter"].sum()

        season_average = round(
            season_runs / season_dismissals,
            2
        ) if season_dismissals else season_runs

        season_sr = round(
            (season_runs / season_balls) * 100,
            2
        ) if season_balls else 0

        season_stats.append({

            "season": season,

            "matches": season_matches,

            "runs": season_runs,

            "average": season_average,

            "strike_rate": season_sr,

            "fifties": int(
                (
                    (season_scores >= 50) &
                    (season_scores < 100)
                ).sum()
            ),

            "centuries": int(
                (season_scores >= 100).sum()
            ),

            "highest_score": int(
                season_scores.max()
            ) if not season_scores.empty else 0
        })

      # ==========================================
    # RECENT INNINGS
    # ==========================================

    recent_innings = []

    recent_matches = batting_df.groupby(
        ["match_id", "date"]
    ).agg({
        "runs_batter": "sum",
        "balls_faced": "sum",
        "batting_team": "first",
        "bowling_team": "first"
    }).reset_index()

    recent_matches["date"] = pd.to_datetime(
        recent_matches["date"],
        errors="coerce"
    )

    recent_matches = recent_matches.sort_values(
        "date",
        ascending=False
    ).head(5)

    for _, row in recent_matches.iterrows():

        recent_innings.append({

            "date": row["date"].strftime("%d-%m-%Y")
            if pd.notnull(row["date"])
            else "-",

            "opponent": row["bowling_team"],

            "runs": int(row["runs_batter"]),

            "balls": int(row["balls_faced"]),

            "strike_rate": round(
                (row["runs_batter"] /
                 row["balls_faced"]) * 100,
                2
            ) if row["balls_faced"] else 0
        })

    # ==========================================
    # CAREER RECORDS
    # ==========================================

    records = {

        "highest_score": highest_score,

        "total_fifties": fifties,

        "total_centuries": centuries,

        "best_bowling": best_bowling,

        "total_fours": int(
            (batting_df["runs_batter"] == 4).sum()
        ),

        "total_sixes": int(
            (batting_df["runs_batter"] == 6).sum()
        )
    }

    # ==========================================
    # PLAYER LIST
    # ==========================================

    players = sorted(
        df["batter"]
        .dropna()
        .unique()
    )

    return render_template(
        "players.html",
        players=players,
        selected_player=selected_player,
        batting=batting,
        bowling=bowling,
        season_stats=season_stats,
        recent_innings=recent_innings,
        records=records
    )
# ==========================================
# H2H PAGE
# ==========================================

@app.route("/h2h")
def h2h():

    teams = sorted(
        pd.concat(
            [
                df["batting_team"],
                df["bowling_team"]
            ]
        ).dropna().unique()
    )

    return render_template(
        "h2h.html",
        teams=teams
    )

# ==========================================
# MATCH INSIGHTS
# ==========================================

@app.route("/match-insights")
def match_insights():

    venues = sorted(
        df["venue"].dropna().unique()
    )

    return render_template(
        "match_insights.html",
        venues=venues
    )

# ==========================================
# ABOUT
# ==========================================

@app.route("/about")
def about():

    return render_template(
        "about.html"
    )

# ==========================================
# RUN APP
# ==========================================

if __name__ == "__main__":

    app.run(
        debug=True
    )