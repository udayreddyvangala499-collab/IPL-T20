import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(BASE_DIR, "data", "IPL.csv")

from utils.data_loader import get_df

df = get_df()

TEAM_MAPPING = {
    "Deccan Chargers": "Sunrisers Hyderabad",
    "Delhi Daredevils": "Delhi Capitals",
    "Kings XI Punjab": "Punjab Kings",
    "Royal Challengers Bangalore": "Royal Challengers Bengaluru",
    "Rising Pune Supergiant": "Rising Pune Supergiants"
}

df["batting_team"] = df["batting_team"].replace(TEAM_MAPPING)
df["bowling_team"] = df["bowling_team"].replace(TEAM_MAPPING)
df["match_won_by"] = df["match_won_by"].replace(TEAM_MAPPING)


def get_teams():
    return sorted(
        pd.concat(
            [
                df["batting_team"],
                df["bowling_team"]
            ]
        ).dropna().unique()
    )


def get_h2h_stats(team1, team2, season="All IPL Seasons"):
    
    h2h = df[
        (
            (df["batting_team"] == team1) &
            (df["bowling_team"] == team2)
        )
        |
        (
            (df["batting_team"] == team2) &
            (df["bowling_team"] == team1)
        )
    ].copy()
    
    if season != "All IPL Seasons":
        h2h = h2h[h2h["season"].astype(str) == str(season)]

    match_ids = h2h["match_id"].unique()
    total_matches = len(match_ids)
    
    if total_matches == 0:
        return {"matches": 0}

    wins1 = h2h[h2h["match_won_by"] == team1]["match_id"].nunique()
    wins2 = h2h[h2h["match_won_by"] == team2]["match_id"].nunique()
    
    # Tie logic
    ties = h2h[h2h["result_type"] == "tie"]["match_id"].nunique()
    no_result = h2h[h2h["result_type"] == "no result"]["match_id"].nunique()
    
    # Innings Averages
    innings_scores = h2h.groupby(["match_id", "innings", "batting_team"])["runs_total"].sum().reset_index()
    innings1_avg = innings_scores[innings_scores["innings"] == 1]["runs_total"].mean()
    innings2_avg = innings_scores[innings_scores["innings"] == 2]["runs_total"].mean()
    
    # Highest and Lowest totals
    # We need to get wickets as well. Wickets = count of non-null player_out
    innings_summary = h2h.groupby(["match_id", "innings", "batting_team", "season"]).agg(
        runs=("runs_total", "sum"),
        wickets=("player_out", "count")
    ).reset_index()
    
    highest_total_t1 = None
    highest_total_t2 = None
    lowest_total_t1 = None
    lowest_total_t2 = None
    
    SHORT_NAMES = {
        "Chennai Super Kings": "CSK",
        "Mumbai Indians": "MI",
        "Royal Challengers Bengaluru": "RCB",
        "Kolkata Knight Riders": "KKR",
        "Sunrisers Hyderabad": "SRH",
        "Delhi Capitals": "DC",
        "Punjab Kings": "PBKS",
        "Rajasthan Royals": "RR",
        "Lucknow Super Giants": "LSG",
        "Gujarat Titans": "GT",
        "Pune Warriors": "PWI",
        "Kochi Tuskers Kerala": "KTK",
        "Gujarat Lions": "GL",
        "Rising Pune Supergiants": "RPS"
    }

    team1_short = SHORT_NAMES.get(team1, team1[:3].upper())
    team2_short = SHORT_NAMES.get(team2, team2[:3].upper())
    
    if not innings_summary.empty:
        # Team 1
        t1_summary = innings_summary[innings_summary["batting_team"] == team1]
        if not t1_summary.empty:
            max_t1_idx = t1_summary["runs"].idxmax()
            min_t1_idx = t1_summary["runs"].idxmin()
            
            ht1_row = t1_summary.loc[max_t1_idx]
            lt1_row = t1_summary.loc[min_t1_idx]
            
            highest_total_t1 = {
                "score": f"{ht1_row['runs']}/{ht1_row['wickets']}",
                "desc": f"{team1_short} vs {team2_short}, {ht1_row['season']}"
            }
            lowest_total_t1 = {
                "score": f"{lt1_row['runs']}/{lt1_row['wickets']}",
                "desc": f"{team1_short} vs {team2_short}, {lt1_row['season']}"
            }
            
        # Team 2
        t2_summary = innings_summary[innings_summary["batting_team"] == team2]
        if not t2_summary.empty:
            max_t2_idx = t2_summary["runs"].idxmax()
            min_t2_idx = t2_summary["runs"].idxmin()
            
            ht2_row = t2_summary.loc[max_t2_idx]
            lt2_row = t2_summary.loc[min_t2_idx]
            
            highest_total_t2 = {
                "score": f"{ht2_row['runs']}/{ht2_row['wickets']}",
                "desc": f"{team2_short} vs {team1_short}, {ht2_row['season']}"
            }
            lowest_total_t2 = {
                "score": f"{lt2_row['runs']}/{lt2_row['wickets']}",
                "desc": f"{team2_short} vs {team1_short}, {lt2_row['season']}"
            }

    # Recent Match
    # First ensure date is datetime for correct chronological sorting
    h2h_temp = h2h.copy()
    h2h_temp["date"] = pd.to_datetime(h2h_temp["date"], format='mixed', dayfirst=True)
    recent_matches = (
        h2h_temp.drop_duplicates(subset=["match_id"])
        .sort_values(by="date", ascending=False)
    )
    
    recent_winner = None
    if not recent_matches.empty:
        rm = recent_matches.iloc[0]
        rw_team_full = rm["match_won_by"]
        rw_team_short = SHORT_NAMES.get(rw_team_full, rw_team_full[:3].upper()) if pd.notna(rw_team_full) else "No Result"
        
        recent_winner = {
            "team": rw_team_short,
            "desc": rm["win_outcome"] if pd.notna(rm["win_outcome"]) else "",
            "date": pd.to_datetime(rm["date"]).strftime("%d %b, %Y") if pd.notna(rm["date"]) else ""
        }
        
    recent_matches_list = []
    for _, row in recent_matches.head(5).iterrows():
        recent_matches_list.append({
            "date": pd.to_datetime(row["date"]).strftime("%d %b, %Y") if pd.notna(row["date"]) else "",
            "season": row["season"],
            "venue": row["venue"],
            "winner": row["match_won_by"] if pd.notna(row["match_won_by"]) else "No Result",
            "margin": row["win_outcome"] if pd.notna(row["win_outcome"]) else "-"
        })
        
    # Venue Wise Record
    venue_stats_dict = []
    venues = h2h["venue"].dropna().unique()
    for v in venues:
        v_matches = h2h[h2h["venue"] == v]
        v_total = v_matches["match_id"].nunique()
        v_wins1 = v_matches[v_matches["match_won_by"] == team1]["match_id"].nunique()
        v_wins2 = v_matches[v_matches["match_won_by"] == team2]["match_id"].nunique()
        v_nr = v_total - v_wins1 - v_wins2
        
        v_innings = v_matches.groupby(["match_id", "batting_team"])["runs_total"].sum()
        v_highest = ""
        if not v_innings.empty:
            v_max = v_innings.max()
            v_max_team = v_innings.idxmax()[1]
            v_highest = f"{v_max} ({v_max_team})"
            
        venue_stats_dict.append({
            "venue": v,
            "total": v_total,
            "wins1": v_wins1,
            "wins2": v_wins2,
            "nr": v_nr,
            "highest": v_highest
        })
        
    venue_stats_dict.sort(key=lambda x: x["total"], reverse=True)
    
    # Top Performers (Batting)
    batting = h2h.groupby(["batter", "batting_team"]).agg(
        matches=("match_id", "nunique"),
        runs=("runs_batter", "sum"),
        balls=("valid_ball", "sum"),
        outs=("player_out", "count")
    ).reset_index()
    
    batting = batting[batting["runs"] > 0]
    batting["avg"] = batting.apply(lambda x: round(x["runs"] / x["outs"], 2) if x["outs"] > 0 else "-", axis=1)
    batting["sr"] = batting.apply(lambda x: round((x["runs"] / x["balls"]) * 100, 2) if x["balls"] > 0 else 0, axis=1)
    top_batsmen = batting.sort_values("runs", ascending=False).head(5).to_dict("records")
    
    # Top Performers (Bowling)
    bowling = h2h.groupby(["bowler", "bowling_team"]).agg(
        matches=("match_id", "nunique"),
        wickets=("bowler_wicket", "sum"),
        runs_given=("runs_bowler", "sum"),
        balls_bowled=("valid_ball", "sum")
    ).reset_index()
    
    bowling = bowling[bowling["wickets"] > 0]
    bowling["econ"] = bowling.apply(lambda x: round((x["runs_given"] / x["balls_bowled"]) * 6, 2) if x["balls_bowled"] > 0 else 0, axis=1)
    top_bowlers = bowling.sort_values("wickets", ascending=False).head(5).to_dict("records")
    
    # AI Match Insights
    insights = []
    
    # Insight 1: Recent dominance
    if not recent_matches.empty:
        last_10 = recent_matches.head(10)
        t1_recent = last_10[last_10["match_won_by"] == team1].shape[0]
        t2_recent = last_10[last_10["match_won_by"] == team2].shape[0]
        if t1_recent > t2_recent:
            insights.append(f"{team1} has won {t1_recent} of the last {len(last_10)} H2H matches.")
        elif t2_recent > t1_recent:
            insights.append(f"{team2} has won {t2_recent} of the last {len(last_10)} H2H matches.")
        else:
            insights.append(f"The last {len(last_10)} matches have been evenly split.")
            
    # Insight 2: Venue dominance
    if len(venue_stats_dict) > 0:
        top_venue = venue_stats_dict[0]
        if top_venue["wins1"] > top_venue["wins2"]:
            insights.append(f"{team1} dominates at {top_venue['venue']}, winning {int((top_venue['wins1']/top_venue['total'])*100)}% of matches.")
        elif top_venue["wins2"] > top_venue["wins1"]:
            insights.append(f"{team2} dominates at {top_venue['venue']}, winning {int((top_venue['wins2']/top_venue['total'])*100)}% of matches.")
            
    # Insight 3: Average 1st innings score
    if pd.notna(innings1_avg):
        insights.append(f"Average first innings score in H2H matches is {int(innings1_avg)} runs.")
        
    # Insight 4: Toss impact
       # Insight 4: Toss impact
    toss_impact = h2h[
        h2h["toss_winner"].astype(str) ==
        h2h["match_won_by"].astype(str)
    ]["match_id"].nunique()

    if total_matches > 0:
        insights.append(
            f"Toss has an impact in {int((toss_impact / total_matches) * 100)}% of H2H matches."
        )

    return {
        "matches": total_matches,
        "team1_wins": wins1,
        "team2_wins": wins2,
        "no_result": no_result,
        "ties": ties,
        "team1_win_pct": round(wins1 * 100 / total_matches, 2) if total_matches else 0,
        "team2_win_pct": round(team2_wins * 100 / total_matches, 2) if total_matches else 0,
        "innings1_avg": round(innings1_avg, 2) if pd.notna(innings1_avg) else 0,
        "innings2_avg": round(innings2_avg, 2) if pd.notna(innings2_avg) else 0,
        "highest_total_t1": highest_total_t1,
        "highest_total_t2": highest_total_t2,
        "lowest_total_t1": lowest_total_t1,
        "lowest_total_t2": lowest_total_t2,
        "recent_winner": recent_winner,
        "recent_matches": recent_matches_list,
        "venue_stats": venue_stats_dict,
        "top_batsmen": top_batsmen,
        "top_bowlers": top_bowlers,
        "insights": insights,
        "seasons": sorted(h2h["season"].dropna().unique().tolist(), reverse=True)
    }