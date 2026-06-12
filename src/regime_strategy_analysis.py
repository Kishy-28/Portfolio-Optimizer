"""
Advanced Regime Research Engine

Phase 9.6

Strategy Performance by Regime
"""

import pandas as pd
import numpy as np


def analyze_strategy_by_regime(
    strategy_returns,
    regime_data,
    risk_free_rate=0.02,
    trading_days=252
):
    """
    Analyze a strategy's performance within each market regime.
    """

    if strategy_returns is None or strategy_returns.empty:
        raise ValueError("strategy_returns cannot be empty.")

    if regime_data is None or regime_data.empty:
        raise ValueError("regime_data cannot be empty.")

    if "market_regime" not in regime_data.columns:
        raise ValueError("regime_data must contain column: market_regime")

    aligned_data = pd.DataFrame(
        {
            "return": strategy_returns
        }
    )

    aligned_data["market_regime"] = regime_data["market_regime"]

    aligned_data = aligned_data.dropna()

    results = []

    for regime, group in aligned_data.groupby("market_regime"):
        returns = group["return"]

        if len(returns) < 2:
            continue

        total_return = (1 + returns).prod() - 1

        annual_return = (
            (1 + total_return)
            ** (trading_days / len(returns))
        ) - 1

        volatility = returns.std() * np.sqrt(trading_days)

        sharpe_ratio = (
            (annual_return - risk_free_rate) / volatility
            if volatility > 0
            else 0
        )

        growth_curve = (1 + returns).cumprod()
        running_max = growth_curve.cummax()
        drawdown = (growth_curve / running_max) - 1

        max_drawdown = drawdown.min()

        results.append(
            {
                "market_regime": regime,
                "days": len(returns),
                "total_return": total_return,
                "annual_return": annual_return,
                "volatility": volatility,
                "sharpe_ratio": sharpe_ratio,
                "max_drawdown": max_drawdown
            }
        )

    return pd.DataFrame(results)


def compare_strategies_by_regime(
    strategy_returns_dict,
    regime_data,
    risk_free_rate=0.02
):
    """
    Compare multiple strategies across regimes.
    """

    if strategy_returns_dict is None or len(strategy_returns_dict) == 0:
        return pd.DataFrame()

    all_results = []

    for strategy_name, strategy_returns in strategy_returns_dict.items():

        if strategy_returns is None or strategy_returns.empty:
            continue

        regime_analysis = analyze_strategy_by_regime(
            strategy_returns=strategy_returns,
            regime_data=regime_data,
            risk_free_rate=risk_free_rate
        )

        if regime_analysis is None or regime_analysis.empty:
            continue

        regime_analysis["strategy"] = strategy_name

        all_results.append(regime_analysis)

    if not all_results:
        return pd.DataFrame()

    return pd.concat(all_results, ignore_index=True)


def identify_best_strategy_by_regime(
    strategy_regime_analysis
):
    """
    Best Sharpe strategy per regime.
    """

    if strategy_regime_analysis is None or strategy_regime_analysis.empty:
        return pd.DataFrame()

    best = (
        strategy_regime_analysis
        .sort_values(
            ["market_regime", "sharpe_ratio"],
            ascending=[True, False]
        )
        .groupby("market_regime")
        .head(1)
        .reset_index(drop=True)
    )

    return best


def identify_worst_strategy_by_regime(
    strategy_regime_analysis
):
    """
    Worst Sharpe strategy per regime.
    """

    if strategy_regime_analysis is None or strategy_regime_analysis.empty:
        return pd.DataFrame()

    worst = (
        strategy_regime_analysis
        .sort_values(
            ["market_regime", "sharpe_ratio"],
            ascending=[True, True]
        )
        .groupby("market_regime")
        .head(1)
        .reset_index(drop=True)
    )

    return worst