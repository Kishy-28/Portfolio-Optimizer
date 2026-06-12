"""
Regime-Aware Forecast Analysis

Phase 9.5 — Regime & Forecast Research

This module analyzes forecast accuracy across different
market regimes.
"""

import pandas as pd


def align_forecasts_with_regimes(
    forecast_table,
    realized_forward_returns,
    regime_data
):
    """
    Align expected return forecasts, realized returns, and market regimes.

    This creates an asset-level forecast evaluation table where each row
    links a ticker's forecast to the market regime present at the forecast date.
    """

    if forecast_table is None or forecast_table.empty:
        raise ValueError("forecast_table cannot be empty.")

    if realized_forward_returns is None or realized_forward_returns.empty:
        raise ValueError("realized_forward_returns cannot be empty.")

    if regime_data is None or regime_data.empty:
        raise ValueError("regime_data cannot be empty.")

    required_regime_columns = ["market_regime"]

    for column in required_regime_columns:
        if column not in regime_data.columns:
            raise ValueError(f"regime_data must contain column: {column}")

    realized_clean = realized_forward_returns.dropna()

    if realized_clean.empty:
        raise ValueError("realized_forward_returns has no complete realized return rows.")

    forecast_date = realized_clean.index[-1]

    if forecast_date not in regime_data.index:
        regime_date = regime_data.index[regime_data.index <= forecast_date].max()
    else:
        regime_date = forecast_date

    market_regime = regime_data.loc[regime_date, "market_regime"]
    latest_realized_returns = realized_clean.loc[forecast_date]

    analysis_rows = []

    for _, row in forecast_table.iterrows():
        ticker = row["ticker"]

        if ticker not in latest_realized_returns.index:
            continue

        forecast_return = row["combined_forecast"]
        realized_return = latest_realized_returns[ticker]

        forecast_error = forecast_return - realized_return
        absolute_forecast_error = abs(forecast_error)
        squared_forecast_error = forecast_error ** 2

        correct_direction = (
            (forecast_return >= 0 and realized_return >= 0)
            or (forecast_return < 0 and realized_return < 0)
        )

        analysis_rows.append(
            {
                "forecast_date": forecast_date,
                "regime_date": regime_date,
                "market_regime": market_regime,
                "ticker": ticker,
                "forecast_return": forecast_return,
                "realized_return": realized_return,
                "forecast_error": forecast_error,
                "absolute_forecast_error": absolute_forecast_error,
                "squared_forecast_error": squared_forecast_error,
                "correct_direction": correct_direction,
            }
        )

    return pd.DataFrame(analysis_rows)


def summarize_forecast_accuracy_by_regime(regime_forecast_analysis):
    """
    Summarize forecast accuracy by market regime.
    """

    if regime_forecast_analysis is None or regime_forecast_analysis.empty:
        raise ValueError("regime_forecast_analysis cannot be empty.")

    summary = (
        regime_forecast_analysis.groupby("market_regime")
        .agg(
            observations=("ticker", "count"),
            average_forecast_return=("forecast_return", "mean"),
            average_realized_return=("realized_return", "mean"),
            average_forecast_error=("forecast_error", "mean"),
            mean_absolute_error=("absolute_forecast_error", "mean"),
            mean_squared_error=("squared_forecast_error", "mean"),
            directional_accuracy=("correct_direction", "mean"),
        )
        .reset_index()
    )

    summary["root_mean_squared_error"] = summary["mean_squared_error"] ** 0.5

    return summary.sort_values(
        by="mean_absolute_error",
        ascending=True
    ).reset_index(drop=True)


def identify_best_forecast_regime(regime_forecast_summary):
    """
    Identify the regime with the lowest mean absolute forecast error.
    """

    if regime_forecast_summary is None or regime_forecast_summary.empty:
        return None

    best_row = regime_forecast_summary.sort_values(
        by="mean_absolute_error",
        ascending=True
    ).iloc[0]

    return best_row.to_dict()


def identify_worst_forecast_regime(regime_forecast_summary):
    """
    Identify the regime with the highest mean absolute forecast error.
    """

    if regime_forecast_summary is None or regime_forecast_summary.empty:
        return None

    worst_row = regime_forecast_summary.sort_values(
        by="mean_absolute_error",
        ascending=False
    ).iloc[0]

    return worst_row.to_dict()