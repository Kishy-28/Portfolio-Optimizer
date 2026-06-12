"""
Forecast Evaluation Engine

Phase 9.4 — Regime & Forecast Research

This module evaluates expected return forecasts against realized
future returns.
"""

import pandas as pd


def calculate_realized_forward_returns(
    prices,
    forward_window=63
):
    """
    Calculate realized forward returns over a future holding window.
    """

    if prices is None or prices.empty:
        raise ValueError("prices cannot be empty.")

    if len(prices) <= forward_window:
        raise ValueError("Not enough price data for the forward return window.")

    realized_returns = prices.shift(-forward_window) / prices - 1

    return realized_returns


def evaluate_forecast_accuracy(
    forecast_table,
    realized_forward_returns
):
    """
    Compare forecasted expected returns against realized forward returns.
    """

    if forecast_table is None or forecast_table.empty:
        raise ValueError("forecast_table cannot be empty.")

    if realized_forward_returns is None or realized_forward_returns.empty:
        raise ValueError("realized_forward_returns cannot be empty.")

    latest_realized_returns = realized_forward_returns.dropna().iloc[-1]

    evaluation_rows = []

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

        evaluation_rows.append(
            {
                "ticker": ticker,
                "forecast_return": forecast_return,
                "realized_return": realized_return,
                "forecast_error": forecast_error,
                "absolute_forecast_error": absolute_forecast_error,
                "squared_forecast_error": squared_forecast_error,
                "correct_direction": correct_direction,
            }
        )

    return pd.DataFrame(evaluation_rows)


def summarize_forecast_evaluation(forecast_evaluation):
    """
    Summarize forecast accuracy across assets.
    """

    if forecast_evaluation is None or forecast_evaluation.empty:
        raise ValueError("forecast_evaluation cannot be empty.")

    mean_absolute_error = forecast_evaluation["absolute_forecast_error"].mean()
    mean_squared_error = forecast_evaluation["squared_forecast_error"].mean()
    root_mean_squared_error = mean_squared_error ** 0.5
    directional_accuracy = forecast_evaluation["correct_direction"].mean()

    summary = pd.DataFrame(
        [
            {
                "mean_absolute_error": mean_absolute_error,
                "mean_squared_error": mean_squared_error,
                "root_mean_squared_error": root_mean_squared_error,
                "directional_accuracy": directional_accuracy,
            }
        ]
    )

    return summary