"""
Adaptive Forecast Research Engine

Phase 9.7 — Regime & Forecast Research

This module compares forecast models and recommends the best
forecast model based on current market regime conditions.
"""

import pandas as pd


def create_forecast_model_evaluation(
    forecast_table,
    realized_forward_returns
):
    if forecast_table is None or forecast_table.empty:
        raise ValueError("forecast_table cannot be empty.")

    if realized_forward_returns is None or realized_forward_returns.empty:
        raise ValueError("realized_forward_returns cannot be empty.")

    realized_clean = realized_forward_returns.dropna()

    if realized_clean.empty:
        raise ValueError("realized_forward_returns has no complete realized return rows.")

    latest_realized_returns = realized_clean.iloc[-1]

    forecast_model_columns = {
        "Historical Mean": "historical_mean_forecast",
        "Exponential Weighted": "exponential_weighted_forecast",
        "Momentum": "momentum_forecast",
        "Combined": "combined_forecast",
    }

    evaluation_rows = []

    for model_name, column_name in forecast_model_columns.items():
        if column_name not in forecast_table.columns:
            continue

        model_errors = []
        model_squared_errors = []
        correct_directions = []

        for _, row in forecast_table.iterrows():
            ticker = row["ticker"]

            if ticker not in latest_realized_returns.index:
                continue

            forecast_return = row[column_name]
            realized_return = latest_realized_returns[ticker]

            forecast_error = forecast_return - realized_return

            model_errors.append(abs(forecast_error))
            model_squared_errors.append(forecast_error ** 2)

            correct_direction = (
                (forecast_return >= 0 and realized_return >= 0)
                or (forecast_return < 0 and realized_return < 0)
            )

            correct_directions.append(correct_direction)

        if len(model_errors) == 0:
            continue

        mean_absolute_error = sum(model_errors) / len(model_errors)
        mean_squared_error = sum(model_squared_errors) / len(model_squared_errors)
        root_mean_squared_error = mean_squared_error ** 0.5
        directional_accuracy = sum(correct_directions) / len(correct_directions)

        evaluation_rows.append(
            {
                "forecast_model": model_name,
                "observations": len(model_errors),
                "mean_absolute_error": mean_absolute_error,
                "mean_squared_error": mean_squared_error,
                "root_mean_squared_error": root_mean_squared_error,
                "directional_accuracy": directional_accuracy,
            }
        )

    forecast_model_evaluation = pd.DataFrame(evaluation_rows)

    if forecast_model_evaluation.empty:
        return forecast_model_evaluation

    return forecast_model_evaluation.sort_values(
        by=["mean_absolute_error", "root_mean_squared_error"],
        ascending=[True, True]
    ).reset_index(drop=True)


def identify_best_forecast_model(forecast_model_evaluation):
    if forecast_model_evaluation is None or forecast_model_evaluation.empty:
        return None

    best_row = forecast_model_evaluation.sort_values(
        by=["mean_absolute_error", "root_mean_squared_error"],
        ascending=[True, True]
    ).iloc[0]

    return best_row.to_dict()


def identify_worst_forecast_model(forecast_model_evaluation):
    if forecast_model_evaluation is None or forecast_model_evaluation.empty:
        return None

    worst_row = forecast_model_evaluation.sort_values(
        by=["mean_absolute_error", "root_mean_squared_error"],
        ascending=[False, False]
    ).iloc[0]

    return worst_row.to_dict()


def create_adaptive_forecast_recommendation(
    latest_market_regime,
    regime_forecast_summary,
    forecast_model_evaluation
):
    if latest_market_regime is None:
        raise ValueError("latest_market_regime cannot be None.")

    if forecast_model_evaluation is None or forecast_model_evaluation.empty:
        raise ValueError("forecast_model_evaluation cannot be empty.")

    current_regime = latest_market_regime["market_regime"]

    best_model = identify_best_forecast_model(forecast_model_evaluation)

    expected_forecast_error = best_model["mean_absolute_error"]

    regime_specific_error = None
    regime_directional_accuracy = None

    if (
        regime_forecast_summary is not None
        and not regime_forecast_summary.empty
        and "market_regime" in regime_forecast_summary.columns
    ):
        matching_regime = regime_forecast_summary[
            regime_forecast_summary["market_regime"] == current_regime
        ]

        if not matching_regime.empty:
            regime_specific_error = matching_regime.iloc[0]["mean_absolute_error"]
            regime_directional_accuracy = matching_regime.iloc[0]["directional_accuracy"]

    recommendation = pd.DataFrame(
        [
            {
                "current_market_regime": current_regime,
                "recommended_forecast_model": best_model["forecast_model"],
                "expected_forecast_error": expected_forecast_error,
                "regime_specific_forecast_error": regime_specific_error,
                "regime_directional_accuracy": regime_directional_accuracy,
            }
        ]
    )

    return recommendation