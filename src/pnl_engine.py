"""
pnl_engine.py

Purpose:
--------
Calculate Profit & Loss (PnL) for executed trades.

Responsibilities:
-----------------
1. Calculate Points PnL
2. Convert Points → Monetary PnL
3. Build Equity Curve
4. Calculate Drawdown (NEGATIVE values)
5. Generate Trade Performance Summary

Design Philosophy:
------------------
✔ Clean readable logic
✔ Debug-friendly prints
✔ Uses config-driven parameters
✔ Industry-standard drawdown format
✔ Rounded financial outputs
"""

# --------------------------------------------------
# Imports
# --------------------------------------------------

import pandas as pd

from src import config


# --------------------------------------------------
# Main Function
# --------------------------------------------------

def calculate_pnl(trades_df):
    """
    Calculate PnL for all executed trades.

    Parameters
    ----------
    trades_df : pandas.DataFrame

        Expected columns:
        - entry_price
        - exit_price
        - direction

    Returns
    -------
    trades_df : pandas.DataFrame

        Adds:
        - pnl_points
        - pnl_amount
        - equity
        - drawdown

    summary : dict

        Contains:
        - total trades
        - win rate
        - net profit
        - max drawdown
        - final equity
    """

    # --------------------------------------------------
    # Safety Check — No Trades
    # --------------------------------------------------

    if trades_df.empty:

        print(
            "\nNo trades available for PnL calculation."
        )

        return trades_df, {}


    print("\nCalculating PnL...")


    # --------------------------------------------------
    # Step 1 — Determine Quantity
    # --------------------------------------------------

    quantity = (

        config.TRADE_LOT

        * config.LOT_SIZE

    )

    print(
        f"Effective Quantity Used: {quantity}"
    )


    # --------------------------------------------------
    # Step 2 — Calculate Points PnL
    # --------------------------------------------------

    pnl_points_list = []

    for _, row in trades_df.iterrows():

        entry_price = row["entry_price"]

        exit_price = row["exit_price"]

        direction = row["direction"]


        # LONG Trade Logic

        if direction == "LONG":

            points = (

                exit_price

                - entry_price

            )


        # SHORT Trade Logic

        else:

            points = (

                entry_price

                - exit_price

            )


        # Round to avoid float garbage

        points = round(points, 2)

        pnl_points_list.append(points)


    trades_df["pnl_points"] = pnl_points_list


    # --------------------------------------------------
    # Step 3 — Convert Points → Money
    # --------------------------------------------------

    trades_df["pnl_amount"] = (

        trades_df["pnl_points"]

        * quantity

    )

    # Round monetary values

    trades_df["pnl_amount"] = (

        trades_df["pnl_amount"]

        .round(2)

    )


    # --------------------------------------------------
    # Step 4 — Build Equity Curve
    # --------------------------------------------------

    starting_capital = config.CAPITAL

    running_equity = starting_capital

    equity_list = []

    for pnl in trades_df["pnl_amount"]:

        running_equity += pnl

        running_equity = round(running_equity, 2)

        equity_list.append(running_equity)


    trades_df["equity"] = equity_list


    # --------------------------------------------------
    # Step 5 — Calculate Drawdown (NEGATIVE FORMAT)
    # --------------------------------------------------

    peak_equity = starting_capital

    drawdown_list = []

    for equity_value in trades_df["equity"]:

        # Update peak

        if equity_value > peak_equity:

            peak_equity = equity_value


        # NEGATIVE drawdown

        drawdown = (

            equity_value

            - peak_equity

        )

        drawdown = round(drawdown, 2)

        drawdown_list.append(drawdown)


    trades_df["drawdown"] = drawdown_list


    # --------------------------------------------------
    # Step 6 — Generate Summary Statistics
    # --------------------------------------------------

    total_trades = len(trades_df)


    winning_trades = len(

        trades_df[

            trades_df["pnl_amount"] > 0

        ]

    )


    losing_trades = len(

        trades_df[

            trades_df["pnl_amount"] < 0

        ]

    )


    net_profit = trades_df[

        "pnl_amount"

    ].sum()


    max_drawdown = trades_df[

        "drawdown"

    ].min()   # Most negative value


    win_rate = (

        winning_trades

        / total_trades

        * 100

    )


    final_equity = trades_df[

        "equity"

    ].iloc[-1]


    # --------------------------------------------------
    # Summary Dictionary
    # --------------------------------------------------

    summary = {

        "Total Trades":

            total_trades,

        "Winning Trades":

            winning_trades,

        "Losing Trades":

            losing_trades,

        "Win Rate (%)":

            round(win_rate, 2),

        "Net Profit":

            round(net_profit, 2),

        "Max Drawdown":

            round(max_drawdown, 2),

        "Final Equity":

            round(final_equity, 2)

    }


    print("\nPnL Calculation Completed.")


    return trades_df, summary