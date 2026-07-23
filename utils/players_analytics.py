import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(BASE_DIR, "data", "IPL.csv")

from utils.data_loader import get_df

df = get_df()


def get_players():
    return sorted(df['batter'].dropna().unique())


def get_player_stats(player):

    batting_df = df[df['batter'] == player]
    bowling_df = df[df['bowler'] == player]

    # ------------------------
    # Batting Statistics
    # ------------------------

    matches = batting_df['match_id'].nunique()

    runs = batting_df['runs_batter'].sum()

    balls = batting_df['balls_faced'].sum()

    dismissals = batting_df[
        batting_df['player_out'] == player
    ].shape[0]

    average = round(
        runs / dismissals, 2
    ) if dismissals > 0 else 0

    strike_rate = round(
        (runs / balls) * 100, 2
    ) if balls > 0 else 0

    fours = batting_df[
        batting_df['runs_batter'] == 4
    ].shape[0]

    sixes = batting_df[
        batting_df['runs_batter'] == 6
    ].shape[0]

    # ------------------------
    # Bowling Statistics
    # ------------------------

    wickets = bowling_df['bowler_wicket'].sum()

    runs_conceded = bowling_df['runs_bowler'].sum()

    balls_bowled = bowling_df['valid_ball'].sum()

    overs = round(balls_bowled / 6, 1)

    economy = round(
        runs_conceded / (balls_bowled / 6), 2
    ) if balls_bowled > 0 else 0

    bowling_average = round(
        runs_conceded / wickets, 2
    ) if wickets > 0 else 0

    # ------------------------
    # Fielding Statistics
    # ------------------------

    catches = df[
        (
            df['fielders']
            .fillna('')
            .str.contains(player, regex=False)
        )
        &
        (
            df['wicket_kind'] == 'caught'
        )
    ].shape[0]

    run_outs = df[
        (
            df['fielders']
            .fillna('')
            .str.contains(player, regex=False)
        )
        &
        (
            df['wicket_kind'] == 'run out'
        )
    ].shape[0]

    stumpings = df[
        (
            df['fielders']
            .fillna('')
            .str.contains(player, regex=False)
        )
        &
        (
            df['wicket_kind'] == 'stumped'
        )
    ].shape[0]

    total_dismissals = catches + run_outs + stumpings

    # ------------------------
    # Return Stats
    # ------------------------

    return {

        # Batting
        "matches": int(matches),
        "runs": int(runs),
        "balls": int(balls),
        "average": float(average),
        "strike_rate": float(strike_rate),
        "fours": int(fours),
        "sixes": int(sixes),

        # Bowling
        "wickets": int(wickets),
        "overs": float(overs),
        "economy": float(economy),
        "bowling_average": float(bowling_average),

        # Fielding
        "catches": int(catches),
        "run_outs": int(run_outs),
        "stumpings": int(stumpings),
        "total_dismissals": int(total_dismissals)
    }