"""
performance_report.py

Purpose:
--------
Generate high-level performance statistics
from completed trades.

Responsibilities:
-----------------
1. Compute core trading metrics
2. Evaluate risk vs reward
3. Provide strategy health indicators
"""

# --------------------------------------------------
# Imports
# --------------------------------------------------

import pandas as pd

from src import config


# --------------------------------------------------
# Main Function
# --------------------------------------------------

def generate_performance_report(trades_df):
    """
    Generate system-level performance metrics.
    """

    print("\nGenerating Performance Report...")


    # --------------------------------------------------
    # Basic Counts
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


    # --------------------------------------------------
    # Win Rate
    # --------------------------------------------------

    win_rate = (

        winning_trades

        / total_trades

        * 100

    )


    # --------------------------------------------------
    # Average Win / Loss
    # --------------------------------------------------

    avg_win = trades_df[

        trades_df["pnl_amount"] > 0

    ]["pnl_amount"].mean()


    avg_loss = trades_df[

        trades_df["pnl_amount"] < 0

    ]["pnl_amount"].mean()


    # --------------------------------------------------
    # Profit Factor
    # --------------------------------------------------

    gross_profit = trades_df[

        trades_df["pnl_amount"] > 0

    ]["pnl_amount"].sum()


    gross_loss = abs(

        trades_df[

            trades_df["pnl_amount"] < 0

        ]["pnl_amount"].sum()

    )


    profit_factor = (

        gross_profit

        / gross_loss

    )


    # --------------------------------------------------
    # Expectancy
    # --------------------------------------------------

    expectancy = (

        (win_rate / 100 * avg_win)

        +

        ((100 - win_rate) / 100 * avg_loss)

    )


    # --------------------------------------------------
    # Return %
    # --------------------------------------------------

    net_profit = trades_df[

        "pnl_amount"

    ].sum()


    return_pct = (

        net_profit

        / config.CAPITAL

        * 100

    )


    # --------------------------------------------------
    # Max Drawdown %
    # --------------------------------------------------

    max_drawdown = trades_df[

        "drawdown"

    ].min()


    max_drawdown_pct = (

        abs(max_drawdown)

        / config.CAPITAL

        * 100

    )


    # --------------------------------------------------
    # Final Report
    # --------------------------------------------------

    report = {

        "Total Trades":
            total_trades,

        "Winning Trades":
            winning_trades,

        "Losing Trades":
            losing_trades,

        "Win Rate (%)":
            round(win_rate, 2),

        "Average Win":
            round(avg_win, 2),

        "Average Loss":
            round(avg_loss, 2),

        "Profit Factor":
            round(profit_factor, 2),

        "Expectancy":
            round(expectancy, 2),

        "Return (%)":
            round(return_pct, 2),

        "Max Drawdown (%)":
            round(max_drawdown_pct, 2)

    }


    print("\nPerformance Report Completed.")

    return report