"""
equity_plot.py

Purpose:
--------
Plot equity and drawdown curves.

Output Files:
-------------
reports/equity_curve.png
reports/drawdown_curve.png
"""

# --------------------------------------------------
# Imports
# --------------------------------------------------

import matplotlib.pyplot as plt
import os


# --------------------------------------------------
# Main Plot Function
# --------------------------------------------------

def plot_equity_curve(equity_df):

    print("\nPlotting Equity Curve...")

    # Safety check
    if equity_df.empty:

        print("No equity data available.")
        return


    # Ensure reports folder exists
    os.makedirs("reports", exist_ok=True)


    # --------------------------------------------------
    # Equity Curve Plot
    # --------------------------------------------------

    plt.figure()

    plt.plot(
        equity_df["timestamp"],
        equity_df["equity"]
    )

    plt.title("Equity Curve")

    plt.xlabel("Trades")

    plt.ylabel("Equity")

    plt.xticks(rotation=45)

    plt.tight_layout()

    equity_file = "reports/equity_curve.png"

    plt.savefig(equity_file)

    plt.close()

    print(
        f"Equity curve saved to: {equity_file}"
    )


    # --------------------------------------------------
    # Drawdown Plot
    # --------------------------------------------------

    plt.figure()

    plt.plot(
        equity_df["timestamp"],
        equity_df["drawdown"]
    )

    plt.title("Drawdown Curve")

    plt.xlabel("Trades")

    plt.ylabel("Drawdown")

    plt.xticks(rotation=45)

    plt.tight_layout()

    dd_file = "reports/drawdown_curve.png"

    plt.savefig(dd_file)

    plt.close()

    print(
        f"Drawdown curve saved to: {dd_file}"
    )