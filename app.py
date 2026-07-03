from flask import (
    Flask,
    render_template,
    url_for,
    request,
    redirect
)

from utils.h2h_analytics import get_teams, get_h2h_stats
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
ALL_CHAMPIONS = []

if not df.empty and 'stage' in df.columns:
    try:
        finals = df[df['stage'] == 'Final'].drop_duplicates('season')
        for _, row in finals.sort_values('season', ascending=False, key=lambda x: x.astype(str)).iterrows():
            season_str = str(row['season'])
            year = int(season_str[-2:]) + 2000 if '/' in season_str else int(season_str)
            ALL_CHAMPIONS.append({
                "year": year,
                "team": row['match_won_by'],
                "logo": LOGO_MAP.get(row['match_won_by'], 'IPL1.jpg')
            })
    except Exception as e:
        print("Error calculating champions:", e)

RECENT_CHAMPIONS = ALL_CHAMPIONS[:4]

TEAM_CAPTAINS = {
    "Chennai Super Kings": "MS Dhoni",
    "Mumbai Indians": "Rohit Sharma",
    "Royal Challengers Bengaluru": "Virat Kohli",
    "Kolkata Knight Riders": "Shreyas Iyer",
    "Sunrisers Hyderabad": "Pat Cummins",
    "Rajasthan Royals": "Sanju Samson",
    "Delhi Capitals": "Rishabh Pant",
    "Punjab Kings": "Shikhar Dhawan",
    "Lucknow Super Giants": "KL Rahul",
    "Gujarat Titans": "Shubman Gill"
}

ORANGE_CAPS = {}
PURPLE_CAPS = {}

if not df.empty and 'season' in df.columns:
    try:
        season_runs = df.groupby(['season', 'batter', 'batting_team'])['batter_runs'].sum().reset_index()
        top_batters = season_runs.loc[season_runs.groupby('season')['batter_runs'].idxmax()]
        for _, row in top_batters.iterrows():
            ORANGE_CAPS[row['season']] = {"player": row['batter'], "team": row['batting_team'], "runs": int(row['batter_runs'])}
            
        season_wickets = df.groupby(['season', 'bowler', 'bowling_team'])['bowler_wicket'].sum().reset_index()
        top_bowlers = season_wickets.loc[season_wickets.groupby('season')['bowler_wicket'].idxmax()]
        for _, row in top_bowlers.iterrows():
            PURPLE_CAPS[row['season']] = {"player": row['bowler'], "team": row['bowling_team'], "wickets": int(row['bowler_wicket'])}
    except Exception as e:
        print("Error calculating caps:", e)

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
            bowling_df["runs_bowler"].sum() / wickets,
            2
        ) if wickets else 0,

        "economy": round(
            bowling_df["runs_bowler"].sum() / overs,
            2
        ) if overs else 0,

        "total_wickets": wickets,

        "dot_ball_percentage": round(
            (
                len(
                    bowling_df[
                        bowling_df["runs_bowler"] == 0
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

    # ==========================================
    # NEW DATA EXTRACTS
    # ==========================================
    
    # 1. Champions
    champions = [c["year"] for c in ALL_CHAMPIONS if c["team"] == team]
    
    # 2. Top 5 Scorers (Orange Cap style)
    try:
        top_scorers = (
            batting_df.groupby("batter")["batter_runs"]
            .sum()
            .sort_values(ascending=False)
            .head(5)
            .reset_index()
        )
        top_5_scorers = [
            {"name": row["batter"], "runs": int(row["batter_runs"])}
            for _, row in top_scorers.iterrows()
        ]
    except:
        top_5_scorers = []
    
    # 3. Top 5 Wicket Takers (Purple Cap style)
    try:
        top_bowlers = (
            bowling_df.groupby("bowler")["bowler_wicket"]
            .sum()
            .sort_values(ascending=False)
            .head(5)
            .reset_index()
        )
        top_5_wicket_takers = [
            {"name": row["bowler"], "wickets": int(row["bowler_wicket"])}
            for _, row in top_bowlers.iterrows()
        ]
    except:
        top_5_wicket_takers = []
    
    # 4. Top 3 Main Players
    top_players = [
        {"title": "Top Scorer", "name": most_runs_scorer, "stat": f"{total_runs} Runs"},
        {"title": "Top Wicket Taker", "name": most_wicket_taker, "stat": f"{wickets} Wickets"},
        {"title": "Highest Total", "name": selected_team["name"], "stat": f"{highest_total} Runs"}
    ]

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
        recent_match=recent_match,
        champions=champions,
        top_5_scorers=top_5_scorers,
        top_5_wicket_takers=top_5_wicket_takers,
        top_players=top_players
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

# PLAYER SEARCH AUTOCOMPLETE API
@app.route("/api/players-suggest")
def players_suggest():
    from flask import jsonify
    query = request.args.get("q", "").strip().lower()
    if not query or len(query) < 1:
        return jsonify([])
    all_players = sorted(df["batter"].dropna().unique())
    matches = [p for p in all_players if query in p.lower()][:10]
    return jsonify(matches)

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
            ) if not season_scores.empty else 0,
            
            "fours": int(
                (season_df["runs_batter"] == 4).sum()
            ),
            
            "sixes": int(
                (season_df["runs_batter"] == 6).sum()
            )
        })

    # ==========================================
    # BOWLING SEASON STATS
    # ==========================================
    bowling_season_stats = []
    if not bowling_df.empty:
        for season in sorted(bowling_df["season"].dropna().unique(), reverse=True):
            s_df = bowling_df[bowling_df["season"] == season]
            s_matches = s_df["match_id"].nunique()
            s_wickets = int(s_df["bowler_wicket"].sum())
            s_balls = int(s_df["valid_ball"].sum())
            s_runs = int(s_df["runs_bowler"].sum())
            s_overs = s_balls / 6 if s_balls else 0
            
            bowling_season_stats.append({
                "season": season,
                "matches": s_matches,
                "wickets": s_wickets,
                "runs": s_runs,
                "economy": round(s_runs / s_overs, 2) if s_overs else 0,
                "average": round(s_runs / s_wickets, 2) if s_wickets else 0,
                "strike_rate": round(s_balls / s_wickets, 2) if s_wickets else 0
            })

    # ==========================================
    # FIELDING SEASON STATS
    # ==========================================
    fielding_season_stats = []
    fielding_df = df[df["fielders"].str.contains(player, na=False, regex=False)]
    if not fielding_df.empty:
        for season in sorted(fielding_df["season"].dropna().unique(), reverse=True):
            f_df = fielding_df[fielding_df["season"] == season]
            fielding_season_stats.append({
                "season": season,
                "catches": int((f_df["wicket_kind"] == "caught").sum()),
                "run_outs": int((f_df["wicket_kind"] == "run out").sum()),
                "stumpings": int((f_df["wicket_kind"] == "stumped").sum())
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
        bowling_season_stats=bowling_season_stats,
        fielding_season_stats=fielding_season_stats,
        recent_innings=recent_innings,
        records=records
    )
# ==========================================
# H2H PAGE
# ==========================================


@app.route("/h2h")
def h2h():

    ESTABLISHED_MAP = {
        "Chennai Super Kings": 2008,
        "Mumbai Indians": 2008,
        "Royal Challengers Bengaluru": 2008,
        "Kolkata Knight Riders": 2008,
        "Sunrisers Hyderabad": 2013,
        "Rajasthan Royals": 2008,
        "Delhi Capitals": 2008,
        "Punjab Kings": 2008,
        "Lucknow Super Giants": 2022,
        "Gujarat Titans": 2022
    }

    team_names = get_teams()
    teams_list = []
    for t_name in team_names:
        sh_name = SHORT_NAMES.get(t_name, t_name)
        teams_list.append({
            "name": t_name,
            "short_name": sh_name,
            "logo": LOGO_MAP.get(t_name, "IPL1.jpg"),
            "established": ESTABLISHED_MAP.get(t_name, 2008)
        })

    team1_short = request.args.get("team1", "CSK")
    team2_short = request.args.get("team2", "MI")
    season = request.args.get("season", "All IPL Seasons")

    team1_full = TEAM_NAME_MAP.get(team1_short, team1_short)
    team2_full = TEAM_NAME_MAP.get(team2_short, team2_short)

    stats = get_h2h_stats(team1_full, team2_full, season)
    
    t1_info = next((t for t in teams_list if t["short_name"] == team1_short), {})
    t2_info = next((t for t in teams_list if t["short_name"] == team2_short), {})

    return render_template(
        "h2h.html",
        teams=teams_list,
        team1=team1_short,
        team2=team2_short,
        team1_name=team1_full,
        team2_name=team2_full,
        team1_info=t1_info,
        team2_info=t2_info,
        season=season,
        stats=stats
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
# WINNERS / CHAMPIONS
# ==========================================

@app.route("/winners")
def winners():

    return render_template(
        "winners.html",
        champions=ALL_CHAMPIONS
    )

# ==========================================
# RUN APP
# ==========================================

if __name__ == "__main__":

    app.run(
        debug=True
    )