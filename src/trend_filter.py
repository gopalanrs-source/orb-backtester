"""
trend_filter.py

Purpose:
--------
Apply trend and quality filters to ORB signals.

Filters Included:
-----------------
1. Daily EMA Trend Filter
2. ORB Minimum Range Filter

Design Goals:
-------------
✔ Modular filtering
✔ Config-driven logic
✔ Clean signal filtering
✔ No modification of original data
"""

# --------------------------------------------------
# Imports
# --------------------------------------------------

import pandas as pd

from src import config


# --------------------------------------------------
# Build Daily EMA
# --------------------------------------------------

def build_daily_ema(df):
    """
    Build Daily EMA from intraday data.
    """

    print("\nBuilding Daily EMA...")

    # Create Daily Close
    daily_close = df["Close"].resample("D").last()

    # Calculate EMA
    daily_ema = daily_close.ewm(
        span=config.DAILY_EMA_PERIOD,
        adjust=False
    ).mean()

    daily_df = pd.DataFrame({

        "daily_close": daily_close,
        "daily_ema": daily_ema

    })

    print("Daily EMA built.")

    return daily_df


# --------------------------------------------------
# Apply EMA Trend Filter
# --------------------------------------------------

def apply_trend_filter(df, signals_df):
    """
    Apply EMA-based directional filter.

    LONG  → price > EMA
    SHORT → price < EMA
    """

    print("\nApplying EMA Trend Filter...")

    if signals_df.empty:

        print("No signals available.")

        return signals_df


    # Build EMA
    daily_df = build_daily_ema(df)


    # --------------------------------------------------
    # Prepare merge
    # --------------------------------------------------

    signals_df = signals_df.copy()

    signals_df["date_only"] = pd.to_datetime(
        signals_df["entry_time"]
    ).dt.date


    daily_df["date_only"] = daily_df.index.date


    merged_df = signals_df.merge(

        daily_df,

        on="date_only",

        how="left"

    )


    # --------------------------------------------------
    # Apply Conditions
    # --------------------------------------------------

    long_condition = (

        (merged_df["direction"] == "LONG")

        &

        (merged_df["entry_price"]

         > merged_df["daily_ema"])

    )


    short_condition = (

        (merged_df["direction"] == "SHORT")

        &

        (merged_df["entry_price"]

         < merged_df["daily_ema"])

    )


    filtered_df = merged_df[

        long_condition

        |

        short_condition

    ].copy()


    print(
        "Signals Before EMA Filter:",
        len(signals_df)
    )

    print(
        "Signals After EMA Filter:",
        len(filtered_df)
    )


    # Drop helper columns
    filtered_df.drop(

        columns=[

            "date_only",
            "daily_close",
            "daily_ema"

        ],

        inplace=True

    )


    return filtered_df


# --------------------------------------------------
# Apply ORB Range Filter
# --------------------------------------------------

def apply_orb_range_filter(signals_df):
    """
    Remove signals with weak ORB ranges.

    Uses:
        config.MIN_ORB_RANGE
    """

    print("\nApplying ORB Range Filter...")

    if signals_df.empty:

        print("No signals available.")

        return signals_df


    before_count = len(signals_df)


    filtered_df = signals_df[

        signals_df["orb_range"]

        >= config.MIN_ORB_RANGE

    ].copy()


    after_count = len(filtered_df)


    print(
        "Signals Before ORB Range Filter:",
        before_count
    )

    print(
        "Signals After ORB Range Filter:",
        after_count
    )


    return filtered_df