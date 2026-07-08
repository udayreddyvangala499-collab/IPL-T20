import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(BASE_DIR, "data", "IPL.csv")

_df = None

def get_df():
    global _df
    if _df is None:
        _df = pd.read_csv(CSV_PATH, low_memory=False)
    return _df