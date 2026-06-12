"""
Regime Attribution Engine

Phase 9.2 — Regime & Forecast Research

This module analyzes portfolio performance inside each detected
market regime.
"""

import pandas as pd


def calculate_max_drawdown_from_returns(returns):
    if returns is None or returns.empty:
        return 0.0

    growth_curve = (1 + returns).cumprod()
    running_max = growth_curve.cummax()
    drawdown = (growth_curve / running_max) - 1

    return drawdown.min()


def calculate_regime_attribution(
    regime_data,
    risk_free_rate=0.02,
    trading_days=252
):
    """
    Calculate portfolio performance attribution by market regime.
    """

    if regime_data is None or regime_data.empty:
        raise ValueError("regime_data cannot be empty.")

    required_columns = ["market_regime", "daily_return"]

    for column in required_columns:
        if column not in regime_data.columns:
            raise ValueError(f"regime_data must contain column: {column}")

    attribution_rows = []

    for regime, group in regime_data.groupby("market_regime"):
        returns = group["daily_return"].dropna()

        if returns.empty:
            continue

        days = len(returns)
        average_daily_return = returns.mean()
        total_return = (1 + returns).prod() - 1
        annualized_return = (1 + total_return) ** (trading_days / days) - 1
        annualized_volatility = returns.std() * (trading_days ** 0.5)

        if annualized_volatility != 0:
            sharpe_ratio = (annualized_return - risk_free_rate) / annualized_volatility
        else:
            sharpe_ratio = 0.0

        max_drawdown = calculate_max_drawdown_from_returns(returns)

        attribution_rows.append(
            {
                "market_regime": regime,
                "days": days,
                "average_daily_return": average_daily_return,
                "total_return": total_return,
                "annualized_return": annualized_return,
                "annualized_volatility": annualized_volatility,
                "sharpe_ratio": sharpe_ratio,
                "max_drawdown": max_drawdown,
            }
        )

    regime_attribution = pd.DataFrame(attribution_rows)

    if regime_attribution.empty:
        return regime_attribution

    return regime_attribution.sort_values(
        by="sharpe_ratio",
        ascending=False
    ).reset_index(drop=True)


def identify_best_regime(regime_attribution):
    """
    Identify the best-performing regime by Sharpe ratio.
    """

    if regime_attribution is None or regime_attribution.empty:
        return None

    best_row = regime_attribution.sort_values(
        by="sharpe_ratio",
        ascending=False
    ).iloc[0]

    return best_row.to_dict()


def identify_worst_regime(regime_attribution):
    """
    Identify the worst-performing regime by Sharpe ratio.
    """

    if regime_attribution is None or regime_attribution.empty:
        return None

    worst_row = regime_attribution.sort_values(
        by="sharpe_ratio",
        ascending=True
    ).iloc[0]

    return worst_row.to_dict()