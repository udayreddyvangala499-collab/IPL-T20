import pandas as pd

df = pd.read_csv("IPL.csv", low_memory=False)
kohli = df[df["batter"] == "V Kohli"]

print(kohli[
    ["runs_batter", "batter_runs"]
].head(20))
print(
    kohli[
        [
            "balls_faced",
            "batter_balls"
        ]
    ].head(20)
)

# print("\n========== ALL COLUMNS ==========\n")
# for col in df.columns:
#     print(col)

# print("\n========== DATASET SHAPE ==========\n")
# print(df.shape)

# print("\n========== SAMPLE DATA ==========\n")
# print(df.head())

# print("\n========== UNIQUE PLAYERS (BATTERS) ==========\n")
# print(df["batter"].dropna().nunique())

# print("\n========== UNIQUE PLAYERS (BOWLERS) ==========\n")
# print(df["bowler"].dropna().nunique())

# print("\n========== SAMPLE BATTERS ==========\n")
# print(df["batter"].dropna().unique()[:20])

# print("\n========== SAMPLE BOWLERS ==========\n")
# print(df["bowler"].dropna().unique()[:20])

# print("\n========== SEASONS ==========\n")
# print(sorted(df["season"].dropna().unique()))

# print("\n========== TEAMS ==========\n")
# print(sorted(df["batting_team"].dropna().unique()))

# print("\n========== IMPORTANT PLAYER ANALYTICS COLUMNS ==========\n")

# important_cols = [
#     "match_id",
#     "date",
#     "season",
#     "batting_team",
#     "bowling_team",
#     "batter",
#     "batter_runs",
#     "batter_balls",
#     "bowler",
#     "bowler_wicket",
#     "runs_bowler",
#     "player_out",
#     "venue"
# ]

# for col in important_cols:
#     print(
#         f"{col} ->",
#         "Available" if col in df.columns else "Missing"
#     )
# player = "V Kohli"

# player_df = df[df["batter"] == player]

# print("\nPLAYER:", player)

# print("\nRows:")
# print(player_df.shape)

# print("\nColumns:")
# print(player_df.columns.tolist())

# print("\nSample:")
# print(
#     player_df[
#         [
#             "match_id",
#             "date",
#             "season",
#             "batting_team",
#             "bowling_team",
#             "batter_runs",
#             "batter_balls"
#         ]
#     ].head(20)
# )