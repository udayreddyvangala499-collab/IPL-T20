import pandas as pd

df = pd.read_csv("data/IPL.csv")
print("Unique Seasons:")
print(df['season'].astype(str).unique())

def get_home_stats():

    total_matches = df['match_id'].nunique()

    total_seasons = pd.to_datetime(df['date']).dt.year.nunique()

    total_teams = len(
        pd.Series(
            df['batting_team'].tolist() +
            df['bowling_team'].tolist()
        ).unique()
    )

    total_players = len(
        pd.Series(
            df['batter'].tolist() +
            df['bowler'].tolist()
        ).unique()
    )

    total_runs = df['runs_total'].sum()

    total_wickets = df['bowler_wicket'].sum()
    

    return {
    "matches": int(total_matches),
    "seasons": int(total_seasons),
    "teams": int(total_teams),
    "players": int(total_players),
    "runs": int(total_runs),
    "wickets": int(total_wickets)
}
