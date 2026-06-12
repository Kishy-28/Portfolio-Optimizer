"""
Regime & Forecast Research Dashboard

Phase 9.8 — Regime & Forecast Research

This module consolidates all Phase 9 regime and forecast research
outputs into one institutional dashboard.
"""

import pandas as pd


def create_regime_forecast_dashboard(
    latest_market_regime,
    best_regime,
    worst_regime,
    best_forecast_regime,
    worst_forecast_regime,
    best_forecast_model,
    worst_forecast_model,
    adaptive_forecast_recommendation,
):
    dashboard_rows = []

    dashboard_rows.append(
        {
            "category": "Current Market Regime",
            "metric": "Latest Regime",
            "value": latest_market_regime.get("market_regime")
            if latest_market_regime
            else None,
        }
    )

    dashboard_rows.append(
        {
            "category": "Regime Performance",
            "metric": "Best Regime",
            "value": best_regime.get("market_regime")
            if best_regime
            else None,
        }
    )

    dashboard_rows.append(
        {
            "category": "Regime Performance",
            "metric": "Worst Regime",
            "value": worst_regime.get("market_regime")
            if worst_regime
            else None,
        }
    )

    dashboard_rows.append(
        {
            "category": "Forecast Reliability",
            "metric": "Best Forecast Regime",
            "value": best_forecast_regime.get("market_regime")
            if best_forecast_regime
            else None,
        }
    )

    dashboard_rows.append(
        {
            "category": "Forecast Reliability",
            "metric": "Worst Forecast Regime",
            "value": worst_forecast_regime.get("market_regime")
            if worst_forecast_regime
            else None,
        }
    )

    dashboard_rows.append(
        {
            "category": "Forecast Model Ranking",
            "metric": "Best Forecast Model",
            "value": best_forecast_model.get("forecast_model")
            if best_forecast_model
            else None,
        }
    )

    dashboard_rows.append(
        {
            "category": "Forecast Model Ranking",
            "metric": "Worst Forecast Model",
            "value": worst_forecast_model.get("forecast_model")
            if worst_forecast_model
            else None,
        }
    )

    if (
        adaptive_forecast_recommendation is not None
        and not adaptive_forecast_recommendation.empty
    ):
        recommendation = adaptive_forecast_recommendation.iloc[0]

        dashboard_rows.append(
            {
                "category": "Adaptive Forecast Recommendation",
                "metric": "Recommended Forecast Model",
                "value": recommendation.get("recommended_forecast_model"),
            }
        )

        dashboard_rows.append(
            {
                "category": "Adaptive Forecast Recommendation",
                "metric": "Expected Forecast Error",
                "value": recommendation.get("expected_forecast_error"),
            }
        )

    return pd.DataFrame(dashboard_rows)


def create_regime_strategy_dashboard(
    best_strategy_by_regime,
    worst_strategy_by_regime
):
    dashboard_rows = []

    if best_strategy_by_regime is not None and not best_strategy_by_regime.empty:
        for _, row in best_strategy_by_regime.iterrows():
            dashboard_rows.append(
                {
                    "market_regime": row["market_regime"],
                    "metric": "Best Strategy",
                    "strategy": row["strategy"],
                    "sharpe_ratio": row["sharpe_ratio"],
                    "annual_return": row["annual_return"],
                    "volatility": row["volatility"],
                    "max_drawdown": row["max_drawdown"],
                }
            )

    if worst_strategy_by_regime is not None and not worst_strategy_by_regime.empty:
        for _, row in worst_strategy_by_regime.iterrows():
            dashboard_rows.append(
                {
                    "market_regime": row["market_regime"],
                    "metric": "Worst Strategy",
                    "strategy": row["strategy"],
                    "sharpe_ratio": row["sharpe_ratio"],
                    "annual_return": row["annual_return"],
                    "volatility": row["volatility"],
                    "max_drawdown": row["max_drawdown"],
                }
            )

    return pd.DataFrame(dashboard_rows)