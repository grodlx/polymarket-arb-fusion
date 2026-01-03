import numpy as np
import pandas as pd

def get_market_correlations(history_dict):
    """Vypočítá korelační matici z historických cen trhů."""
    df = pd.DataFrame(history_dict)
    if df.empty:
        return pd.DataFrame()
    return df.corr()

def detect_anomalies(df):
    """Najde trhy, které se utrhly od trendu (Z-Score > 2)."""
    if df.empty: return None
    last_row = df.iloc[-1]
    z_scores = (last_row - df.mean()) / df.std()
    return z_scores
