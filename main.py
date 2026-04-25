"""
main.py

Purpose:
--------
Main execution file for ORB backtesting system.

Responsibilities:
-----------------
1. Load Futures Data
2. Generate ORB Signals
3. Apply Filters
    - EMA Trend Filter
    - ORB Range Filter
    - ATR Filter
4. Execute Trades
5. Calculate PnL
6. Generate Reports
7. Save Results

Design Goals:
-------------
✔ Modular pipeline
✔ Filter-driven architecture
✔ Easy debugging
✔ Scalable system
"""

# --------------------------------------------------
# Imports
# --------------------------------------------------

from src import config

from src.data_loader import load_data
from src.signal_cache import get_orb_signals

from src.trend_filter import (
    apply_trend_filter,
    apply_orb_range_filter
)

from src.atr_filter import apply_atr_filter

from src.trade_engine import run_trade_engine
from src.pnl_engine import calculate_pnl

from src.equity_curve import (
    generate_equity_curve,
    plot_equity_curve
)

from src.performance_report import (
    generate_performance_report
)

from src.monthly_report import (
    generate_monthly_report
)

from src.monthly_plot import (
    plot_monthly_equity
)

import pandas as pd
import os


# --------------------------------------------------
# Main Execution Function
# --------------------------------------------------

def main():

    print("\n==============================")
    print(" STEP 1 — Load Market Data")
    print("==============================")

    df = load_data()

    print("\nData Loaded Successfully")
    print("Data Shape:", df.shape)


    # --------------------------------------------------
    # STEP 2 — Load ORB Signals
    # --------------------------------------------------

    print("\n==============================")
    print(" STEP 2 — Load ORB Signals")
    print("==============================")

    signals_df = get_orb_signals(df)


    # --------------------------------------------------
    # Apply EMA Trend Filter
    # --------------------------------------------------

    if config.USE_TREND_FILTER:

        signals_df = apply_trend_filter(
            df,
            signals_df
        )


    # --------------------------------------------------
    # Apply ORB Range Filter
    # --------------------------------------------------

    if config.USE_ORB_RANGE_FILTER:

        signals_df = apply_orb_range_filter(
            signals_df
        )


    # --------------------------------------------------
    # Apply ATR Filter
    # --------------------------------------------------

    if config.USE_ATR_FILTER:

        signals_df = apply_atr_filter(
            df,
            signals_df
        )


    # --------------------------------------------------
    # ORB Diagnostics
    # --------------------------------------------------

    print("\nORB Signal Summary")
    print("----------------------")

    print(
        "Total Signals Generated:",
        len(signals_df)
    )

    print("\nORB Range Statistics")
    print("----------------------")

    print(
        signals_df["orb_range"].describe()
    )


    # --------------------------------------------------
    # STEP 3 — Run Trade Engine
    # --------------------------------------------------

    print("\n==============================")
    print(" STEP 3 — Run Trade Engine")
    print("==============================")

    trades_df = run_trade_engine(
        df,
        signals_df
    )

    print("\nTrade Execution Summary")
    print("----------------------")

    print(
        "Total Trades Executed:",
        len(trades_df)
    )

    print("\nSample Trades:")

    print(
        trades_df.head()
    )


    # --------------------------------------------------
    # STEP 4 — Calculate PnL
    # --------------------------------------------------

    print("\n==============================")
    print(" STEP 4 — Calculate PnL")
    print("==============================")

    if trades_df.empty:

        print("\nNo trades available for PnL calculation.")

    else:

        trades_df, pnl_summary = calculate_pnl(
            trades_df
        )

        print("\nPnL Summary")
        print("----------------------")

        for key, value in pnl_summary.items():

            print(f"{key}: {value}")


    # --------------------------------------------------
    # STEP 5 — Generate Equity Curve
    # --------------------------------------------------

    print("\n==============================")
    print(" STEP 5 — Generate Equity Curve")
    print("==============================")

    equity_df = generate_equity_curve(
        trades_df
    )

    plot_equity_curve(
        equity_df
    )


    # --------------------------------------------------
    # STEP 6 — Performance Report
    # --------------------------------------------------

    print("\n==============================")
    print(" STEP 6 — Generate Performance Report")
    print("==============================")

    performance_report = generate_performance_report(
        trades_df
    )

    print("\nPerformance Summary")
    print("----------------------")

    for key, value in performance_report.items():

        print(f"{key}: {value}")


    # --------------------------------------------------
    # STEP 7 — Monthly Report
    # --------------------------------------------------

    print("\n==============================")
    print(" STEP 7 — Monthly Report")
    print("==============================")

    monthly_df = generate_monthly_report(
        trades_df
    )

    plot_monthly_equity(
        monthly_df
    )


    # --------------------------------------------------
    # STEP 8 — Save Results
    # --------------------------------------------------

    print("\n==============================")
    print(" STEP 8 — Save Results")
    print("==============================")

    output_path = "reports/trades_with_pnl.csv"

    os.makedirs(
        "reports",
        exist_ok=True
    )

    trades_df.to_csv(
        output_path,
        index=False
    )

    print("\nTrades saved to:", output_path)


    # --------------------------------------------------
    # Completed
    # --------------------------------------------------

    print("\n==============================")
    print(" BACKTEST COMPLETED")
    print("==============================")



# --------------------------------------------------
# Entry Point
# --------------------------------------------------

if __name__ == "__main__":

    main()