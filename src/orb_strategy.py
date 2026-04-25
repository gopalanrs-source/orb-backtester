# --------------------------------------------------
# ORB Strategy Module
# --------------------------------------------------

import pandas as pd
from datetime import timedelta

from src import config


# --------------------------------------------------
# Helper: Convert string time to pandas time
# --------------------------------------------------

def _to_time(time_str):
    return pd.to_datetime(time_str).time()


# --------------------------------------------------
# Main Function
# --------------------------------------------------

def generate_orb_signals(df):
    """
    Generate ORB breakout signals.

    Parameters
    ----------
    df : pandas.DataFrame
        1-minute OHLC dataframe
        Index must be datetime

    Returns
    -------
    signals_df : pandas.DataFrame
        ORB signals dataframe
    """

    signals = []

    market_open_time = _to_time(config.MARKET_OPEN_TIME)
    last_entry_time = _to_time(config.LAST_ENTRY_TIME)

    buffer_points = config.BREAKOUT_BUFFER_POINTS
    max_trades = config.MAX_TRADES_PER_DAY

    orb_minutes = config.ORB_WINDOW_MINUTES

    stop_loss_percent = config.STOP_LOSS_PERCENT

    # Group data by date
    grouped = df.groupby(df.index.date)

    for trade_date, day_df in grouped:

        day_df = day_df.copy()

        trade_count = 0

        # --------------------------------------------------
        # Step 1 — Calculate ORB
        # --------------------------------------------------

        orb_end_time = (
            pd.Timestamp.combine(
                pd.Timestamp(trade_date),
                market_open_time
            )
            + timedelta(minutes=orb_minutes)
        ).time()

        orb_df = day_df[
            (day_df.index.time >= market_open_time) &
            (day_df.index.time < orb_end_time)
        ]

        if orb_df.empty:
            continue

        orb_high = orb_df["High"].max()
        orb_low = orb_df["Low"].min()

        orb_range = orb_high - orb_low

        # --------------------------------------------------
        # Step 2 — Build 5-minute candles
        # --------------------------------------------------

        # --------------------------------------------------
        # Build 5-minute candles (RIGHT aligned)
        # This ensures:
        # 14:05 candle = 14:00 → 14:04:59
        # --------------------------------------------------

        five_min_df = day_df.resample(
            "5min",
            label="right",
            closed="right"
        ).agg({

            "Open": "first",

            "High": "max",

            "Low": "min",

            "Close": "last",

            "Volume": "sum"

        })

        five_min_df.dropna(inplace=True)

        # --------------------------------------------------
        # Step 3 — Scan for Breakouts
        # --------------------------------------------------

        long_trigger = orb_high + buffer_points
        short_trigger = orb_low - buffer_points

        for idx, row in five_min_df.iterrows():

            current_time = idx.time()

            if current_time <= orb_end_time:
                continue

            if current_time > last_entry_time:
                break

            if trade_count >= max_trades:
                break

            close_price = row["Close"]

            direction = None

            # LONG condition
            if (
                config.ALLOW_LONG and
                close_price > long_trigger
            ):
                direction = "LONG"

            # SHORT condition
            elif (
                config.ALLOW_SHORT and
                close_price < short_trigger
            ):
                direction = "SHORT"

            if direction is None:
                continue

            # --------------------------------------------------
            # Step 4 — Calculate Stop Loss
            # --------------------------------------------------

            if direction == "LONG":

                stop_loss = (
                    orb_high
                    - (orb_range * stop_loss_percent)
                )

            else:  # SHORT

                stop_loss = (
                    orb_low
                    + (orb_range * stop_loss_percent)
                )

            # --------------------------------------------------
            # Step 5 — Entry Time Adjustment
            # Use candle close time directly.
            # Trade engine will pick next available minute.
            # --------------------------------------------------

            entry_time = idx

            signal = {
                "date": trade_date,
                "entry_time": entry_time,
                "direction": direction,
                "entry_price": close_price,
                "orb_high": orb_high,
                "orb_low": orb_low,
                "orb_range": orb_range,
                "stop_loss": stop_loss,
                "trade_number": trade_count + 1
            }

            signals.append(signal)

            trade_count += 1

        # End of day loop

    # --------------------------------------------------
    # Convert to DataFrame
    # --------------------------------------------------

    signals_df = pd.DataFrame(signals)

    return signals_df