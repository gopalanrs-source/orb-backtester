"""
equity_curve.py

Purpose:
--------
Generate and visualize equity curve
from completed trades.

Responsibilities:
-----------------
1. Extract equity from trades
2. Create trade-by-trade equity curve
3. Save equity curve to CSV
4. Plot equity curve
5. Plot drawdown curve

Design Goals:
-------------
✔ Simple
✔ Reliable
✔ Compatible with existing pipeline
✔ Visualization-ready
"""

# --------------------------------------------------
# Imports
# --------------------------------------------------

import pandas as pd
import os
import matplotlib.pyplot as plt


# --------------------------------------------------
# Generate Equity Curve
# --------------------------------------------------

def generate_equity_curve(trades_df):
    """
    Generate equity curve file.

    Parameters
    ----------
    trades_df : pandas.DataFrame
        Completed trades with equity column

    Returns
    -------
    equity_df : pandas.DataFrame
        Equity curve data
    """

    print("\nGenerating Equity Curve...")

    # --------------------------------------------------
    # Safety Check
    # --------------------------------------------------

    if trades_df.empty:

        print("No trades available.")

        return pd.DataFrame()

    if "equity" not in trades_df.columns:

        print("Equity column not found.")

        return pd.DataFrame()


    # --------------------------------------------------
    # Create Equity Curve DataFrame
    # --------------------------------------------------

    equity_df = trades_df[

        [
            "exit_time",
            "equity",
            "drawdown"
        ]

    ].copy()


    # Rename timestamp column

    equity_df.rename(

        columns={

            "exit_time": "timestamp"

        },

        inplace=True

    )


    # Reset index

    equity_df.reset_index(

        drop=True,

        inplace=True

    )


    # --------------------------------------------------
    # Save Equity CSV
    # --------------------------------------------------

    os.makedirs(

        "reports",

        exist_ok=True

    )

    output_file = "reports/equity_curve.csv"

    equity_df.to_csv(

        output_file,

        index=False

    )

    print(

        f"Equity curve saved to: {output_file}"

    )

    print(

        "Total Equity Points:",

        len(equity_df)

    )

    return equity_df


# --------------------------------------------------
# Plot Equity Curve
# --------------------------------------------------

def plot_equity_curve(equity_df):
    """
    Plot equity and drawdown curves.
    """

    if equity_df.empty:

        print("No equity data to plot.")

        return


    print("\nPlotting Equity Curve...")


    os.makedirs(

        "reports",

        exist_ok=True

    )


    # --------------------------------------------------
    # Equity Curve Plot
    # --------------------------------------------------

    plt.figure()

    plt.plot(

        equity_df["equity"]

    )

    plt.title("Equity Curve")

    plt.xlabel("Trades")

    plt.ylabel("Equity")

    equity_plot_path = "reports/equity_curve.png"

    plt.savefig(

        equity_plot_path

    )

    plt.close()


    # --------------------------------------------------
    # Drawdown Plot
    # --------------------------------------------------

    plt.figure()

    plt.plot(

        equity_df["drawdown"]

    )

    plt.title("Drawdown Curve")

    plt.xlabel("Trades")

    plt.ylabel("Drawdown")

    drawdown_plot_path = "reports/drawdown_curve.png"

    plt.savefig(

        drawdown_plot_path

    )

    plt.close()


    print(

        f"Equity curve saved to: {equity_plot_path}"

    )

    print(

        f"Drawdown curve saved to: {drawdown_plot_path}"

    )