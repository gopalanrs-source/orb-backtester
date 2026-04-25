"""
data_loader.py

Purpose:
--------
Load NIFTY Futures data efficiently.

Key Features:
-------------
✔ Loads CSV only once
✔ Saves processed data to cache
✔ Loads cache instantly next time
✔ Handles schema inconsistencies
✔ Filters only NIFTY-I.NFO
✔ Logs skipped files
✔ Validates cache integrity

Cache File:
-----------
cache/nifty_futures.pkl
"""

import os
import pandas as pd


# --------------------------------------------------
# Cache File Path
# --------------------------------------------------

CACHE_FOLDER = "cache"

CACHE_FILE = os.path.join(
    CACHE_FOLDER,
    "nifty_futures.pkl"
)


# --------------------------------------------------
# Get All CSV Files
# --------------------------------------------------

def get_all_csv_files(base_path="data"):
    """
    Recursively scan data folder
    and return list of all CSV files.
    """

    file_list = []

    for root, dirs, files in os.walk(base_path):

        for file in files:

            if file.endswith(".csv"):

                full_path = os.path.join(root, file)

                file_list.append(full_path)

    file_list.sort()

    print(f"Total CSV files found: {len(file_list)}")

    return file_list


# --------------------------------------------------
# Process Single File
# --------------------------------------------------

def process_single_file(file_path):
    """
    Read one CSV file
    Filter NIFTY-I.NFO
    Create Datetime index
    Return cleaned dataframe
    """

    try:

        # Skip tiny files
        if os.path.getsize(file_path) < 1000:

            return None

        # Read CSV
        df = pd.read_csv(
            file_path,
            sep=",",
            engine="python",
            on_bad_lines="skip"
        )

    except Exception:

        print(f"Unreadable file skipped: {file_path}")

        with open("skipped_files.log", "a") as f:

            f.write(file_path + "\n")

        return None


    try:

        # --------------------------------------------------
        # Normalize column names
        # --------------------------------------------------

        df.columns = df.columns.str.strip()

        column_map = {

            "DATE": "Date",
            "TIME": "Time",
            "OPEN": "Open",
            "HIGH": "High",
            "LOW": "Low",
            "CLOSE": "Close",
            "VOLUME": "Volume",
            "OPEN INTEREST": "Open Interest"

        }

        df.rename(columns=column_map, inplace=True)


        # --------------------------------------------------
        # Validate required columns
        # --------------------------------------------------

        required_cols = [

            "Ticker",
            "Date",
            "Time",
            "Open",
            "High",
            "Low",
            "Close"

        ]

        for col in required_cols:

            if col not in df.columns:

                return None


        # --------------------------------------------------
        # Filter NIFTY Futures only
        # --------------------------------------------------

        df = df[
            df["Ticker"] == "NIFTY-I.NFO"
        ].copy()

        if df.empty:

            return None


        # --------------------------------------------------
        # Create Datetime Index
        # --------------------------------------------------

        df["Datetime"] = pd.to_datetime(

            df["Date"].astype(str)
            + " "
            + df["Time"].astype(str),

            dayfirst=True,
            errors="coerce"

        )

        df.dropna(subset=["Datetime"], inplace=True)

        df.set_index("Datetime", inplace=True)


        # --------------------------------------------------
        # Keep Required Columns
        # --------------------------------------------------

        keep_cols = [

            "Open",
            "High",
            "Low",
            "Close"

        ]

        if "Volume" in df.columns:

            keep_cols.append("Volume")

        if "Open Interest" in df.columns:

            keep_cols.append("Open Interest")

        df = df[keep_cols]


        # Sort index
        df.sort_index(inplace=True)

        return df


    except Exception:

        with open("skipped_files.log", "a") as f:

            f.write(file_path + "\n")

        return None


# --------------------------------------------------
# Load Data (With Cache Safety)
# --------------------------------------------------

def load_data():
    """
    Main data loading function.

    Uses cache if available.
    Rebuilds cache if corrupted.
    """

    print("\nLoading data...\n")


    # --------------------------------------------------
    # Step 1 — Load From Cache
    # --------------------------------------------------

    if os.path.exists(CACHE_FILE):

        print("Loading data from cache...")

        df = pd.read_pickle(CACHE_FILE)

        print(
            f"Loaded {len(df)} rows from cache."
        )


        # --------------------------------------------------
        # CRITICAL CACHE VALIDATION
        # --------------------------------------------------

        if not isinstance(
            df.index,
            pd.DatetimeIndex
        ):

            print(
                "WARNING: Cache index invalid!"
            )

            print(
                "Rebuilding cache..."
            )

            # Delete corrupted cache
            os.remove(CACHE_FILE)

            # Reload fresh
            return load_data()


        return df


    # --------------------------------------------------
    # Step 2 — Build Cache
    # --------------------------------------------------

    print("Cache not found. Building cache...")

    all_files = get_all_csv_files()

    all_data = []

    valid_files = 0
    skipped_files = 0


    for i, file_path in enumerate(
        all_files,
        start=1
    ):

        if i % 50 == 0:

            print(
                f"Processing file {i} of {len(all_files)}"
            )

        df = process_single_file(file_path)

        if df is not None:

            valid_files += 1

            all_data.append(df)

        else:

            skipped_files += 1


    if not all_data:

        print(
            "WARNING: No NIFTY-I.NFO data found!"
        )

        return pd.DataFrame()


    # --------------------------------------------------
    # Combine All Files
    # --------------------------------------------------

    combined_df = pd.concat(all_data)

    combined_df.sort_index(inplace=True)


    # --------------------------------------------------
    # Save Cache
    # --------------------------------------------------

    print("\nSaving cache...")

    if not os.path.exists(CACHE_FOLDER):

        os.makedirs(CACHE_FOLDER)

    combined_df.to_pickle(CACHE_FILE)

    print("Cache saved.")


    # --------------------------------------------------
    # Summary
    # --------------------------------------------------

    print("\nData Loading Summary")

    print("----------------------")

    print("Valid files loaded:", valid_files)

    print("Skipped files:", skipped_files)

    print(
        "Total rows loaded:",
        len(combined_df)
    )

    return combined_df