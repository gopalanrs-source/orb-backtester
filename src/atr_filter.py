"""
atr_filter.py

Purpose:
--------
Build Daily ATR and filter signals
based on volatility conditions.

Design Goals:
-------------
✔ Daily ATR calculation
✔ Attach ATR to each signal
✔ Filter weak volatility days
✔ Config-driven behavior
"""

# --------------------------------------------------
# Imports
# --------------------------------------------------

import pandas as pd

from src import config


# --------------------------------------------------
# Build Daily ATR
# --------------------------------------------------

def build_daily_atr(df):
    """
    Build Daily ATR from intraday data.
    """

    print("\nBuilding Daily ATR...")

    # --------------------------------------------------
    # Convert to Daily OHLC
    # --------------------------------------------------

    daily_df = df.resample("D").agg({

        "High": "max",
        "Low": "min",
        "Close": "last"

    }).dropna()


    # --------------------------------------------------
    # True Range Calculation
    # --------------------------------------------------

    daily_df["prev_close"] = daily_df["Close"].shift(1)

    daily_df["tr1"] = (

        daily_df["High"]
        - daily_df["Low"]

    )

    daily_df["tr2"] = abs(

        daily_df["High"]
        - daily_df["prev_close"]

    )

    daily_df["tr3"] = abs(

        daily_df["Low"]
        - daily_df["prev_close"]

    )

    daily_df["TR"] = daily_df[

        ["tr1", "tr2", "tr3"]

    ].max(axis=1)


    # --------------------------------------------------
    # ATR Calculation
    # --------------------------------------------------

    daily_df["ATR"] = (

        daily_df["TR"]

        .rolling(

            window=config.ATR_PERIOD

        )

        .mean()

    )


    daily_df = daily_df[["ATR"]].dropna()

    print("Daily ATR built.")

    return daily_df


# --------------------------------------------------
# Apply ATR Filter
# --------------------------------------------------

def apply_atr_filter(df, signals_df):
    """
    Apply ATR-based ORB validation.
    """

    print("\nApplying ATR Filter...")

    daily_atr = build_daily_atr(df)


    # --------------------------------------------------
    # Attach ATR to signals
    # --------------------------------------------------

    signals_df["date"] = pd.to_datetime(
        signals_df["date"]
    )

    daily_atr.index = pd.to_datetime(
        daily_atr.index
    )

    signals_df = signals_df.merge(

        daily_atr,

        left_on="date",

        right_index=True,

        how="left"

    )


    # --------------------------------------------------
    # ATR-based ORB validation
    # --------------------------------------------------

    before_count = len(signals_df)

    min_required_range = (

        signals_df["ATR"]

        * config.MIN_ATR_MULTIPLIER

    )


    filtered_df = signals_df[

        signals_df["orb_range"]

        >= min_required_range

    ].copy()


    after_count = len(filtered_df)

    print("Signals Before ATR Filter:", before_count)
    print("Signals After ATR Filter:", after_count)

    return filtered_df