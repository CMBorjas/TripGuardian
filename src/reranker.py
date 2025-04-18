# src/reranker.py
import pandas as pd
def rerank_routes(df):
    """
    Calculate a total route score based on delay, walktime,crowidn and safety.
    Higher is better.
    """
    df["total_score"] = (
        100
        - (df["walk_time"] * 1.5
        + df["delay_minutes"] * 2
        + df["crowdedness_score"] * 1.2
        + (100 - df["safety_score"]))
        + df.get("alert_penalty",0)
    )
    df = df.sort_values("total_score", ascending=False)
    return df
