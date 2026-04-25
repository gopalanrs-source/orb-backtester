"""
trade_engine.py

Purpose:
--------
Execute trades based on ORB signals.

Responsibilities:
-----------------
1. Enter trade at signal time
2. Monitor candles until exit
3. Apply stop-loss logic
4. Apply time exit (15:25)
5. Prevent overlapping trades
6. Calculate MAE / MFE (NEW)

Design Goals:
-------------
✔ Realistic execution
✔ No overlapping trades
✔ Detailed trade analytics
✔ Future-ready for optimization
"""

# --------------------------------------------------
# Imports
# --------------------------------------------------

import pandas as pd

from datetime import timedelta

from src import config


# --------------------------------------------------
# Helper Function — Calculate Strike
# --------------------------------------------------

def get_option_strike(price, direction):
    """
    Determine option strike based on direction.

    LONG  → Sell PE below price
    SHORT → Sell CE above price
    """

    base_strike = round(price / 100) * 100

    if direction == "LONG":

        strike = (

            base_strike

            - config.OPTION_OTM_DISTANCE

        )

        option_type = "PE"

    else:

        strike = (

            base_strike

            + config.OPTION_OTM_DISTANCE

        )

        option_type = "CE"

    return strike, option_type


# --------------------------------------------------
# Main Trade Execution Function
# --------------------------------------------------

def run_trade_engine(df, signals_df):
    """
    Execute trades based on ORB signals.
    Includes:
    - Stop Loss
    - Time Exit
    - MAE / MFE Calculation
    """

    print("\nExecuting Trade Engine...")

    trades = []

    last_exit_time = None


    # --------------------------------------------------
    # Process each signal
    # --------------------------------------------------

    for _, signal in signals_df.iterrows():

        entry_time = signal["entry_time"]

        trade_date = signal["date"]

        direction = signal["direction"]

        stop_loss = signal["stop_loss"]

        trade_number = signal["trade_number"]


        # --------------------------------------------------
        # Prevent overlapping trades
        # --------------------------------------------------

        if last_exit_time is not None:

            if entry_time <= last_exit_time:

                continue


        # --------------------------------------------------
        # Get Entry Price
        # (next minute OPEN)
        # --------------------------------------------------

        if entry_time not in df.index:
            future_index = df.index[df.index >= entry_time]
            if len(future_index) == 0:
                continue
            entry_time = future_index[0]

        entry_price = df.loc[entry_time]["Open"]
    
        # --------------------------------------------------
        # Determine Strike
        # --------------------------------------------------

        strike, option_type = get_option_strike(

            entry_price,

            direction

        )


        # --------------------------------------------------
        # Prepare Trade Window
        # --------------------------------------------------

        exit_time_limit = pd.Timestamp.combine(

            entry_time.date(),

            pd.to_datetime(

                config.FORCE_EXIT_TIME

            ).time()

        )


        trade_window = df[

            (df.index >= entry_time)

            &

            (df.index <= exit_time_limit)

        ]


        # --------------------------------------------------
        # Initialize MAE / MFE trackers
        # --------------------------------------------------

        mae_points = 0
        mfe_points = 0


        # --------------------------------------------------
        # Scan candles
        # --------------------------------------------------

        exit_price = None

        exit_time = None

        exit_reason = None


        for ts, candle in trade_window.iterrows():

            high_price = candle["High"]

            low_price = candle["Low"]

            close_price = candle["Close"]


            # --------------------------------------------------
            # Update MAE / MFE
            # --------------------------------------------------

            if direction == "LONG":

                # MAE → worst move down
                adverse_move = (

                    low_price

                    - entry_price

                )

                # MFE → best move up
                favorable_move = (

                    high_price

                    - entry_price

                )

            else:  # SHORT

                adverse_move = (

                    entry_price

                    - high_price

                )

                favorable_move = (

                    entry_price

                    - low_price

                )


            mae_points = min(

                mae_points,

                adverse_move

            )

            mfe_points = max(

                mfe_points,

                favorable_move

            )


            # --------------------------------------------------
            # Stop Loss Check
            # --------------------------------------------------

            if direction == "LONG":

                if close_price < stop_loss:

                    exit_price = close_price

                    exit_time = ts

                    exit_reason = "STOP_LOSS"

                    break

            else:  # SHORT

                if close_price > stop_loss:

                    exit_price = close_price

                    exit_time = ts

                    exit_reason = "STOP_LOSS"

                    break


        # --------------------------------------------------
        # Time Exit if SL not hit
        # --------------------------------------------------

        if exit_price is None:

            exit_price = trade_window.iloc[-1]["Close"]

            exit_time = trade_window.index[-1]

            exit_reason = "TIME_EXIT"


        # Update last exit time
        last_exit_time = exit_time


        # --------------------------------------------------
        # Convert MAE/MFE → Amount
        # --------------------------------------------------

        quantity = (

            config.TRADE_LOT

            * config.LOT_SIZE

        )

        mae_amount = round(

            mae_points * quantity,

            2

        )

        mfe_amount = round(

            mfe_points * quantity,

            2

        )


        # --------------------------------------------------
        # Save Trade
        # --------------------------------------------------

        trade = {

            "date": trade_date,

            "trade_number": trade_number,

            "direction": direction,

            "entry_time": entry_time,

            "entry_price": entry_price,

            "strike": strike,

            "option_type": option_type,

            "stop_loss": stop_loss,

            "exit_time": exit_time,

            "exit_price": exit_price,

            "exit_reason": exit_reason,

            "mae_points": round(mae_points, 2),

            "mfe_points": round(mfe_points, 2),

            "mae_amount": mae_amount,

            "mfe_amount": mfe_amount

        }

        trades.append(trade)


    # --------------------------------------------------
    # Convert to DataFrame
    # --------------------------------------------------

    trades_df = pd.DataFrame(trades)

    print(

        "Total Trades Executed:",

        len(trades_df)

    )

    return trades_df