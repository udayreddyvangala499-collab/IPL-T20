# import pandas as pd

# df = pd.read_csv("IPL.csv", low_memory=False)
# df['date'] = pd.to_datetime(df['date'])

# for year in range(2008, 2026):

#     matches = df[df['date'].dt.year == year]['match_id'].nunique()

#     print(f"{year}: {matches} matches")

# import pandas as pd

# df = pd.read_csv("IPL.csv", low_memory=False)

# df['date'] = pd.to_datetime(df['date'])

# # # Filter 2008 matches
# df_2008 = df[df['date'].dt.year == 2008]

# # One row per match
# matches = (
#     df_2008.groupby('match_id')
#     .first()
#     .reset_index()
# )

# print(f"Total Matches Found: {len(matches)}\n")

# for i, row in enumerate(matches.itertuples(), start=1):
#     print(
#         f"Match {i}: "
#         f"{row.batting_team} vs {row.bowling_team} "
#         f"({row.date.date()})"
#     )

# # import pandas as pd

# df = pd.read_csv("IPL.csv", low_memory=False)

# total_runs = df['runs_total'].sum()

# print("Total Runs Scored:", total_runs)


# import pandas as pd

# df = pd.read_csv("IPL.csv", low_memory=False)

# df['date'] = pd.to_datetime(df['date'])
# t_runs=0;
# for year in range(2008, 2026):

#     runs = df[df['date'].dt.year == year]['runs_total'].sum()

#     t_runs += runs
#     print(f"{year}: {runs} runs")

# print(f"Total runs scored across all years: {t_runs}")


import pandas as pd

df = pd.read_csv("IPL.csv", low_memory=False)

# df['date'] = pd.to_datetime(df['date'])

# # Filter 2020 matches
# df_2020 = df[df['date'].dt.year == 2020]

# # Runs per team
# runs_per_team = (
#     df_2020.groupby('batting_team')['runs_total']
#     .sum()
#     .sort_values(ascending=False)
# )

# # print(runs_per_team)
# print([col for col in df.columns if "win" in col.lower()])
# # print(df['win_outcome'].dropna().unique()[:20])
# print(df.columns.tolist())
# for col in df.columns:
#     if 'team' in col.lower():
#         print(col)

import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

# from utils.team_analytics import get_team_stats

# from utils.team_analytics import get_team_stats

# print(get_team_stats("Mumbai Indians"))


from utils.players_analytics import get_player_stats

print(get_player_stats("V Kohli"))