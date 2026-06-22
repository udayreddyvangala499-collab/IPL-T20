import pandas as pd

df = pd.read_csv("IPL.csv", low_memory=False)

TEAM_MAPPING = {
    "Deccan Chargers": "Sunrisers Hyderabad",
    "Delhi Daredevils": "Delhi Capitals",
    "Kings XI Punjab": "Punjab Kings",
    "Royal Challengers Bangalore": "Royal Challengers Bengaluru"
}

df["match_won_by"] = df["match_won_by"].replace(TEAM_MAPPING)

matches_df = df[
    ["match_id", "match_won_by"]
].drop_duplicates("match_id")

print(
    matches_df["match_won_by"]
    .value_counts()
    .head(15)
)