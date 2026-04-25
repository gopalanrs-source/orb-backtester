"""
monthly_plot.py

Purpose:
--------
Plot monthly equity curve.

Output:
-------
reports/monthly_equity_curve.png
"""

# --------------------------------------------------
# Imports
# --------------------------------------------------

import matplotlib.pyplot as plt
import os


# --------------------------------------------------
# Plot Monthly Equity
# --------------------------------------------------

def plot_monthly_equity(monthly_df):

    print("\nPlotting Monthly Equity Curve...")


    # --------------------------------------------------
    # Safety Checks
    # --------------------------------------------------

    if monthly_df.empty:

        print("No monthly data available.")

        return


    # Work on copy (avoid warning)

    monthly_df = monthly_df.copy()


    os.makedirs(

        "reports",

        exist_ok=True

    )


    # --------------------------------------------------
    # Prepare X-axis labels
    # --------------------------------------------------

    monthly_df["month_str"] = (

        monthly_df["month"]

        .astype(str)

    )


    # --------------------------------------------------
    # Monthly Equity Plot
    # --------------------------------------------------

    plt.figure(figsize=(12, 6))

    plt.plot(

        monthly_df["month_str"],

        monthly_df["cumulative_pnl"]

    )

    plt.title("Monthly Equity Curve")

    plt.xlabel("Month")

    plt.ylabel("Cumulative Profit")


    # Rotate labels

    plt.xticks(

        rotation=45

    )


    plt.tight_layout()


    file_path = (

        "reports/monthly_equity_curve.png"

    )


    plt.savefig(

        file_path

    )

    plt.close()


    print(

        f"Monthly equity plot saved to: {file_path}"

    )