import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(BASE_DIR, "data", "IPL.csv")

df = pd.read_csv(CSV_PATH, low_memory=False)


# ==========================
# Seasons
# ==========================

def get_seasons():
    return sorted(df['season'].dropna().unique())


# ==========================
# Season Overview
# ==========================

def get_season_stats(season):

    season_df = df[
        df['season'].astype(str) == str(season)
    ]

    matches = season_df['match_id'].nunique()

    runs = season_df['runs_total'].sum()

    wickets = season_df['bowler_wicket'].sum()

    teams = sorted(
        season_df['batting_team']
        .dropna()
        .unique()
    )

    return {
        "matches": int(matches),
        "runs": int(runs),
        "wickets": int(wickets),
        "teams": teams
    }


# ==========================
# Season Top Performers
# ==========================

def get_season_top_performers(season):

    season_df = df[
        df['season'].astype(str) == str(season)
    ]

    runs_df = (
        season_df.groupby('batter')['runs_batter']
        .sum()
        .sort_values(ascending=False)
    )

    sixes_df = (
        season_df[
            season_df['runs_batter'] == 6
        ]
        .groupby('batter')
        .size()
        .sort_values(ascending=False)
    )

    wickets_df = (
        season_df.groupby('bowler')['bowler_wicket']
        .sum()
        .sort_values(ascending=False)
    )

    catches_df = (
        season_df[
            season_df['wicket_kind'] == 'caught'
        ]
        .groupby('fielders')
        .size()
        .sort_values(ascending=False)
    )

    return {

        # Batting
        "top_batter":
        runs_df.index[0] if not runs_df.empty else "N/A",

        "top_runs":
        int(runs_df.iloc[0]) if not runs_df.empty else 0,

        "most_sixes_player":
        sixes_df.index[0] if not sixes_df.empty else "N/A",

        "most_sixes":
        int(sixes_df.iloc[0]) if not sixes_df.empty else 0,

        # Bowling
        "top_bowler":
        wickets_df.index[0] if not wickets_df.empty else "N/A",

        "top_wickets":
        int(wickets_df.iloc[0]) if not wickets_df.empty else 0,

        # Fielding
        "top_fielder":
        catches_df.index[0] if not catches_df.empty else "N/A",

        "top_catches":
        int(catches_df.iloc[0]) if not catches_df.empty else 0
    }


# ==========================
# Team Performance
# ==========================

def get_team_season_stats(team, season):

    season_df = df[
        df['season'].astype(str) == str(season)
    ]

    team_df = season_df[
        (season_df['batting_team'] == team)
        |
        (season_df['bowling_team'] == team)
    ]

    matches = team_df['match_id'].nunique()

    wins = season_df[
        season_df['match_won_by'] == team
    ]['match_id'].nunique()

    losses = matches - wins

    win_pct = round(
        (wins / matches) * 100, 2
    ) if matches else 0

    runs = season_df[
        season_df['batting_team'] == team
    ]['runs_total'].sum()

    wickets = season_df[
        season_df['bowling_team'] == team
    ]['bowler_wicket'].sum()

    return {

        "matches": int(matches),
        "wins": int(wins),
        "losses": int(losses),
        "win_pct": float(win_pct),
        "runs": int(runs),
        "wickets": int(wickets)
    }


# ==========================
# Team Top Performers
# ==========================

def get_team_top_performers(team, season):

    season_df = df[
        df['season'].astype(str) == str(season)
    ]

    team_batting = season_df[
        season_df['batting_team'] == team
    ]

    team_bowling = season_df[
        season_df['bowling_team'] == team
    ]

    runs_df = (
        team_batting.groupby('batter')['runs_batter']
        .sum()
        .sort_values(ascending=False)
    )

    sixes_df = (
        team_batting[
            team_batting['runs_batter'] == 6
        ]
        .groupby('batter')
        .size()
        .sort_values(ascending=False)
    )

    wickets_df = (
        team_bowling.groupby('bowler')['bowler_wicket']
        .sum()
        .sort_values(ascending=False)
    )

    catches_df = (
        season_df[
            (season_df['wicket_kind'] == 'caught')
            &
            (
                (season_df['batting_team'] == team)
                |
                (season_df['bowling_team'] == team)
            )
        ]
        .groupby('fielders')
        .size()
        .sort_values(ascending=False)
    )

    return {

        # Batting
        "top_batter":
        runs_df.index[0] if not runs_df.empty else "N/A",

        "top_runs":
        int(runs_df.iloc[0]) if not runs_df.empty else 0,

        "most_sixes_player":
        sixes_df.index[0] if not sixes_df.empty else "N/A",

        "most_sixes":
        int(sixes_df.iloc[0]) if not sixes_df.empty else 0,

        # Bowling
        "top_bowler":
        wickets_df.index[0] if not wickets_df.empty else "N/A",

        "top_wickets":
        int(wickets_df.iloc[0]) if not wickets_df.empty else 0,

        # Fielding
        "top_fielder":
        catches_df.index[0] if not catches_df.empty else "N/A",

        "top_catches":
        int(catches_df.iloc[0]) if not catches_df.empty else 0
    }