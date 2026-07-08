import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(BASE_DIR, "data", "IPL.csv")

_df = None

USE_COLS = [
    "match_id",
    "date",
    "season",
    "stage",
    "venue",
    "innings",

    "batting_team",
    "bowling_team",
    "match_won_by",
    "win_outcome",

    "batter",
    "bowler",
    "fielders",
    "player_out",
    "player_of_match",

    "runs_total",
    "runs_batter",
    "runs_bowler",

    "balls_faced",
    "batter_balls",
    "valid_ball",

    "bowler_wicket",
    "wicket_kind"
]

DTYPES = {
    "match_id": "int32",

    "batting_team": "category",
    "bowling_team": "category",
    "match_won_by": "category",

    "venue": "category",
    "stage": "category",
    "season": "category",

    "batter": "category",
    "bowler": "category",
    "fielders": "string",
    "player_out": "category",
    "player_of_match": "category",

    "wicket_kind": "category",

    "runs_total": "int16",
    "runs_batter": "int8",
    "runs_bowler": "int8",
    "balls_faced": "int8",
    "batter_balls": "int8",
    "valid_ball": "int8",
    "bowler_wicket": "int8"
}


def get_df():
    global _df

    if _df is None:
        _df = pd.read_csv(
						CSV_PATH,
						usecols=USE_COLS,
						dtype=DTYPES,
						parse_dates=["date"],
						dayfirst=True
				)
    return _df