"""
signal_cache.py

Purpose:
--------
This module manages ORB signal caching.

Why Caching Is Needed:
----------------------
Generating ORB signals requires scanning large datasets.
Even if data loading is fast (via cache), signal generation
can still take noticeable time.

So we:

1. Generate ORB signals once
2. Save them into cache
3. Load them instantly on future runs

This dramatically improves development speed.

Cache File:
-----------
cache/orb_signals.pkl

Workflow:
---------
IF cache exists:
    Load signals from cache

ELSE:
    Generate signals
    Save to cache
    Return signals

Future Enhancement Possibility:
-------------------------------
If config parameters change (like ORB window),
we may rebuild signal cache automatically.
"""


# --------------------------------------------------
# Import Required Modules
# --------------------------------------------------

import os
import pandas as pd

# Import ORB signal generation logic
from src.orb_strategy import generate_orb_signals


# --------------------------------------------------
# Cache Configuration
# --------------------------------------------------

# Folder where cache files are stored
CACHE_FOLDER = "cache"

# ORB signal cache file path
SIGNAL_CACHE_FILE = os.path.join(
    CACHE_FOLDER,
    "orb_signals.pkl"
)


# --------------------------------------------------
# Function: get_orb_signals
# --------------------------------------------------
# Purpose:
# Load ORB signals from cache if available.
# Otherwise generate signals and save them.
#
# Parameters:
# df : pandas.DataFrame
#     1-minute OHLC market data
#
# Returns:
# signals_df : pandas.DataFrame
#     ORB signal dataset
# --------------------------------------------------

def get_orb_signals(df):

    print("\nPreparing ORB Signals...")

    # --------------------------------------------------
    # Step 1 — Check if Signal Cache Exists
    # --------------------------------------------------

    if os.path.exists(SIGNAL_CACHE_FILE):

        print("Loading ORB signals from cache...")

        signals_df = pd.read_pickle(
            SIGNAL_CACHE_FILE
        )

        print(
            f"Loaded {len(signals_df)} signals from cache."
        )

        return signals_df


    # --------------------------------------------------
    # Step 2 — Generate Signals (Cache Not Found)
    # --------------------------------------------------

    print("\nSignal cache not found.")

    print("Generating ORB signals...")

    signals_df = generate_orb_signals(df)

    print(
        f"\nSignals Generated: {len(signals_df)}"
    )


    # --------------------------------------------------
    # Step 3 — Save Signals to Cache
    # --------------------------------------------------

    print("\nSaving ORB signal cache...")

    # Ensure cache folder exists
    if not os.path.exists(CACHE_FOLDER):

        os.makedirs(CACHE_FOLDER)

    # Save signals to pickle file
    signals_df.to_pickle(
        SIGNAL_CACHE_FILE
    )

    print("ORB signal cache saved successfully.")


    # --------------------------------------------------
    # Step 4 — Return Signals
    # --------------------------------------------------

    return signals_df