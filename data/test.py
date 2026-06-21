import pandas as pd

ipl = pd.read_csv("IPL.csv", low_memory=False)
print(ipl.columns.tolist())

# print("Before:")
# print(ipl["date"].dtype)

# ipl["date"] = pd.to_datetime(
#     ipl["date"],
#     dayfirst=True,
#     errors="coerce"
# )

# # print("\nAfter:")
# # print(ipl["date"].dtype)

# # print("\nLatest Date:")
# # print(ipl["date"].max())

# # print("\nLatest 10 Dates:")
# # print(
# #     ipl["date"]
# #     .sort_values(ascending=False)
# #     .head(10)
# # )
# latest_match_id = (
#     ipl.sort_values("date", ascending=False)
#     ["match_id"]
#     .iloc[0]
# )

# print("Latest Match ID:", latest_match_id)

# latest_match = ipl[
#     ipl["match_id"] == latest_match_id
# ]

# summary = (
#     latest_match
#     .groupby("batting_team")
#     .agg({
#         "team_runs":"max",
#         "team_wicket":"max"
#     })
# )

# print(summary)

# print(
#     latest_match["match_won_by"]
#     .iloc[0]
# )