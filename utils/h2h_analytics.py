import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(BASE_DIR, "data", "IPL.csv")

df = pd.read_csv(CSV_PATH, low_memory=False)


def get_teams():
    return sorted(df['batting_team'].dropna().unique())


def get_h2h_stats(team1, team2, venue=None):

    h2h_df = df[
        (
            (df['batting_team'] == team1) &
            (df['bowling_team'] == team2)
        )
        |
        (
            (df['batting_team'] == team2) &
            (df['bowling_team'] == team1)
        )
    ]

    common_venues = sorted(
        h2h_df['venue'].dropna().unique()
    )

    if venue and venue != "All":
        h2h_df = h2h_df[
            h2h_df['venue'] == venue
        ]

    match_ids = h2h_df['match_id'].unique()

    total_matches = len(match_ids)

    wins_team1 = df[
        (df['match_won_by'] == team1) &
        (df['match_id'].isin(match_ids))
    ]['match_id'].nunique()

    wins_team2 = df[
        (df['match_won_by'] == team2) &
        (df['match_id'].isin(match_ids))
    ]['match_id'].nunique()

    innings_scores = (
        h2h_df.groupby(
            ['match_id', 'innings', 'batting_team']
        )['runs_total']
        .sum()
    )

    highest_score = (
        int(innings_scores.max())
        if not innings_scores.empty
        else 0
    )

    lowest_score = (
        int(innings_scores.min())
        if not innings_scores.empty
        else 0
    )

    recent_winner = "N/A"

    if len(match_ids) > 0:

        recent_match = max(match_ids)

        recent_winner = df[
            df['match_id'] == recent_match
        ]['match_won_by'].iloc[0]

    return {
        "matches": total_matches,
        "team1_wins": wins_team1,
        "team2_wins": wins_team2,
        "team1_win_pct": round(
            wins_team1 * 100 / total_matches, 2
        ) if total_matches else 0,
        "team2_win_pct": round(
            wins_team2 * 100 / total_matches, 2
        ) if total_matches else 0,
        "highest_score": highest_score,
        "lowest_score": lowest_score,
        "recent_winner": recent_winner,
        "venues": common_venues
    }