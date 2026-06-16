import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(BASE_DIR, "data", "IPL.csv")

df = pd.read_csv(CSV_PATH, low_memory=False)


def get_teams():
    return sorted(df['batting_team'].dropna().unique())


def get_team_stats(team):

    team_df = df[
        (df['batting_team'] == team) |
        (df['bowling_team'] == team)
    ]

    matches = team_df['match_id'].nunique()

    wins = df[
        df['match_won_by'] == team
    ]['match_id'].nunique()

    losses = matches - wins

    win_percentage = round(
        (wins / matches) * 100, 2
    ) if matches else 0

    runs = df[
        df['batting_team'] == team
    ]['runs_total'].sum()

    wickets = df[
        df['bowling_team'] == team
    ]['bowler_wicket'].sum()

    venues = sorted(
        team_df['venue']
        .dropna()
        .unique()
    )

    return {
        "matches": int(matches),
        "wins": int(wins),
        "losses": int(losses),
        "win_percentage": float(win_percentage),
        "runs": int(runs),
        "wickets": int(wickets),
        "venues": venues
    }


def get_team_venue_stats(team, venue):

    venue_df = df[
        (
            (df['batting_team'] == team) |
            (df['bowling_team'] == team)
        )
        &
        (df['venue'] == venue)
    ]

    match_ids = venue_df['match_id'].unique()

    matches = len(match_ids)

    wins = df[
        (df['match_won_by'] == team)
        &
        (df['match_id'].isin(match_ids))
    ]['match_id'].nunique()

    losses = matches - wins

    win_percentage = round(
        (wins / matches) * 100, 2
    ) if matches else 0

    runs = venue_df[
        venue_df['batting_team'] == team
    ]['runs_total'].sum()

    wickets = venue_df[
        venue_df['bowling_team'] == team
    ]['bowler_wicket'].sum()

    return {
        "matches": int(matches),
        "wins": int(wins),
        "losses": int(losses),
        "win_percentage": float(win_percentage),
        "runs": int(runs),
        "wickets": int(wickets)
    }