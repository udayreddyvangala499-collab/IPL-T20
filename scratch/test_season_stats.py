import pandas as pd
df = pd.read_csv('data/IPL.csv', low_memory=False)
player = "MS Dhoni"

# Batting
batting = df[df['batter'] == player]
if not batting.empty:
    b_stats = batting.groupby('season').agg(
        matches=('match_id', 'nunique'),
        runs=('batter_runs', 'sum'),
        balls=('balls_faced', 'sum'),
        fours=('batter_runs', lambda x: (x==4).sum()),
        sixes=('batter_runs', lambda x: (x==6).sum())
    )
    print("Batting:\n", b_stats.head())

# Bowling
bowling = df[df['bowler'] == player]
if not bowling.empty:
    bw_stats = bowling.groupby('season').agg(
        matches=('match_id', 'nunique'),
        wickets=('bowler_wicket', 'sum'),
        balls=('valid_ball', 'sum'),
        runs=('runs_bowler', 'sum')
    )
    print("Bowling:\n", bw_stats.head())

# Fielding
fielding = df[df['fielders'].str.contains(player, na=False)]
if not fielding.empty:
    f_stats = fielding.groupby('season').apply(lambda x: pd.Series({
        'catches': (x['wicket_kind'] == 'caught').sum(),
        'run_outs': (x['wicket_kind'] == 'run out').sum(),
        'stumpings': (x['wicket_kind'] == 'stumped').sum()
    })).reset_index()
    print("Fielding:\n", f_stats.head())
