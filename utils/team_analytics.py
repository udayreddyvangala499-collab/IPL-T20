import pandas as pd

df = pd.read_csv("data/IPL.csv", low_memory=False)

def get_teams():
    return sorted(df['batting_team'].dropna().unique())


def get_team_stats(team):

    matches_played = df[
        (df['batting_team'] == team) |
        (df['bowling_team'] == team)
    ]['match_id'].nunique()

    wins = df[
        df['match_won_by'] == team
    ]['match_id'].nunique()

    losses = matches_played - wins

    win_percentage = round(
        (wins / matches_played) * 100, 2
    ) if matches_played > 0 else 0

    total_runs = df[
        df['batting_team'] == team
    ]['runs_total'].sum()

    total_wickets = df[
        df['bowling_team'] == team
    ]['bowler_wicket'].sum()

    return {
        "matches": int(matches_played),
        "wins": int(wins),
        "losses": int(losses),
        "win_percentage": win_percentage,
        "runs": int(total_runs),
        "wickets": int(total_wickets)
    }