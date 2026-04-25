"""
monthly_report.py

Purpose:
--------
Generate monthly performance analysis.

Responsibilities:
-----------------
1. Monthly PnL summary
2. Monthly win/loss stats
3. Best/Worst month
4. Monthly win rate
5. Save CSV output
"""

# --------------------------------------------------
# Imports
# --------------------------------------------------

import pandas as pd
import os


# --------------------------------------------------
# Main Function
# --------------------------------------------------

def generate_monthly_report(trades_df):

    print("\nGenerating Monthly Report...")

    if trades_df.empty:

        print("No trades available.")

        return pd.DataFrame()


    # --------------------------------------------------
    # Create Month Column
    # --------------------------------------------------

    trades_df["month"] = pd.to_datetime(

        trades_df["exit_time"]

    ).dt.to_period("M")


    # --------------------------------------------------
    # Monthly Aggregation
    # --------------------------------------------------

    monthly = trades_df.groupby(

        "month"

    ).agg({

        "pnl_amount": "sum"

    }).reset_index()


    monthly.rename(

        columns={

            "pnl_amount": "monthly_pnl"

        },

        inplace=True

    )


    # --------------------------------------------------
    # Cumulative PnL
    # --------------------------------------------------

    monthly["cumulative_pnl"] = (

        monthly["monthly_pnl"].cumsum()

    )


    # --------------------------------------------------
    # Monthly Stats
    # --------------------------------------------------

    winning_months = len(

        monthly[

            monthly["monthly_pnl"] > 0

        ]

    )


    losing_months = len(

        monthly[

            monthly["monthly_pnl"] < 0

        ]

    )


    total_months = len(monthly)


    monthly_win_rate = (

        winning_months

        / total_months

        * 100

    )


    best_month = monthly[

        "monthly_pnl"

    ].max()


    worst_month = monthly[

        "monthly_pnl"

    ].min()


    avg_monthly_profit = (

        monthly["monthly_pnl"].mean()

    )


    # --------------------------------------------------
    # Save CSV
    # --------------------------------------------------

    os.makedirs("reports", exist_ok=True)

    output_file = "reports/monthly_pnl.csv"

    monthly.to_csv(

        output_file,

        index=False

    )


    print(

        f"Monthly report saved to: {output_file}"

    )


    # --------------------------------------------------
    # Print Monthly Summary
    # --------------------------------------------------

    print("\nMonthly Performance Summary")

    print("---------------------------")

    print("Total Months:", total_months)

    print("Winning Months:", winning_months)

    print("Losing Months:", losing_months)

    print("Monthly Win Rate (%):",

          round(monthly_win_rate, 2))

    print("Best Month:",

          round(best_month, 2))

    print("Worst Month:",

          round(worst_month, 2))

    print("Average Monthly Profit:",

          round(avg_monthly_profit, 2))


    # --------------------------------------------------
    # Streak Calculation
    # --------------------------------------------------

    max_loss_streak = 0
    max_win_streak = 0

    current_loss = 0
    current_win = 0


    for pnl in monthly["monthly_pnl"]:

        if pnl < 0:

            current_loss += 1
            current_win = 0

        elif pnl > 0:

            current_win += 1
            current_loss = 0

        else:

            current_loss = 0
            current_win = 0


        max_loss_streak = max(
            max_loss_streak,
            current_loss
        )

        max_win_streak = max(
            max_win_streak,
            current_win
        )


    print("Longest Losing Streak (months):",
        max_loss_streak)

    print("Longest Winning Streak (months):",
        max_win_streak)

    # --------------------------------------------------
    # Recovery Duration Calculation
    # --------------------------------------------------

    peak = monthly["cumulative_pnl"].iloc[0]

    recovery_durations = []

    drawdown_start = None


    for i in range(len(monthly)):

        current_equity = monthly["cumulative_pnl"].iloc[i]

        if current_equity >= peak:

            # Recovery completed

            if drawdown_start is not None:

                duration = i - drawdown_start

                recovery_durations.append(duration)

                drawdown_start = None

            peak = current_equity

        else:

            if drawdown_start is None:

                drawdown_start = i


    if recovery_durations:

        max_recovery = max(recovery_durations)

    else:

        max_recovery = 0


    print(
        "Longest Recovery Duration (months):",
        max_recovery
    )

    # --------------------------------------------------
    # Drawdown Timeline Tracking
    # --------------------------------------------------

    peak = monthly["cumulative_pnl"].iloc[0]

    drawdowns = []

    drawdown_start = None


    for i in range(len(monthly)):

        equity = monthly["cumulative_pnl"].iloc[i]

        if equity >= peak:

            if drawdown_start is not None:

                drawdowns.append({

                    "start_index": drawdown_start,

                    "end_index": i,

                    "duration":

                        i - drawdown_start

                })

                drawdown_start = None

            peak = equity

        else:

            if drawdown_start is None:

                drawdown_start = i


    if drawdowns:

        worst_dd = max(
            drawdowns,
            key=lambda x: x["duration"]
        )

        start_month = monthly.iloc[
            worst_dd["start_index"]
        ]["month"]

        end_month = monthly.iloc[
            worst_dd["end_index"]
        ]["month"]

        duration = worst_dd["duration"]

        print("\nWorst Drawdown Timeline")

        print("-----------------------")

        print("Start Month:", start_month)

        print("Recovery Month:", end_month)

        print("Duration (months):", duration)

    return monthly