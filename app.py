from flask import Flask, render_template
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

# ==========================================
# TEAMS PAGE
# ==========================================
@app.route("/teams")
def teams():
  return team_details("CSK")


@app.route("/teams/<team>")
def team_details(team):

  team = TEAM_NAME_MAP.get(team, team)

  batting_df = df[df["batting_team"] == team]
  bowling_df = df[df["bowling_team"] == team]

  matches = df[
      (df["batting_team"] == team) |
      (df["bowling_team"] == team)
  ]["match_id"].nunique()

  wins = df[
      df["match_won_by"] == team
  ]["match_id"].nunique()

  losses = max(matches - wins, 0)

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

  total_runs = int(batting_df["batter_runs"].sum())

  total_balls = int(
      batting_df["batter_balls"].sum()
  )

  strike_rate = round(
      (total_runs / total_balls) * 100,
      2
  ) if total_balls else 0

  batting_average = round(
      batting_df["batter_runs"].mean(),
      2
  ) if not batting_df.empty else 0

  runs_per_match = round(
      total_runs / matches,
      2
  ) if matches else 0

  match_totals = batting_df.groupby(
      "match_id"
  )["runs_total"].sum()

  highest_score = int(
      match_totals.max()
  ) if not match_totals.empty else 0

  valid_totals = match_totals[
      match_totals > 0
  ]

  lowest_total = int(
      valid_totals.min()
  ) if not valid_totals.empty else 0

  boundary_percentage = round(
      (
          batting_df["batter_runs"]
          .isin([4, 6])
          .sum()
          / len(batting_df)
      ) * 100,
      2
  ) if len(batting_df) else 0

  batting = {
      "average": batting_average,
      "strike_rate": strike_rate,
      "total_runs": total_runs,
      "highest_score": highest_score,
      "boundary_percentage": boundary_percentage,
      "runs_per_match": runs_per_match
  }

  wickets = int(
      bowling_df["bowler_wicket"].sum()
  )

  balls = int(
      bowling_df["valid_ball"].sum()
  )

  overs = balls / 6 if balls else 0

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

      "wickets_per_match": round(
          wickets / matches,
          2
      ) if matches else 0
  }

  records = {
      "highest_total": highest_score,

      "lowest_total": lowest_total,

      "most_runs": batting_df.groupby(
          "batter"
      )["batter_runs"]
      .sum()
      .idxmax()
      if not batting_df.empty else "-",

      "best_bowling": "-",

      "most_wickets": bowling_df.groupby(
          "bowler"
      )["bowler_wicket"]
      .sum()
      .idxmax()
      if not bowling_df.empty else "-"
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
      records=records
  )



# ==========================================
# PLAYERS PAGE
# ==========================================

@app.route("/players")
def players():

    players_list = sorted(
        pd.concat(
            [
                df["batter"],
                df["bowler"]
            ]
        ).dropna().unique()
    )

    return render_template(
        "players.html",
        players=players_list
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