"""
Market Regime Detection Engine

Phase 9.1 — Regime & Forecast Research

This module detects market regimes using rolling return, volatility,
drawdown, and trend conditions.
"""

import pandas as pd


def classify_market_regime(
    rolling_return: float,
    rolling_volatility: float,
    drawdown: float,
    return_threshold: float = 0.00,
    high_volatility_threshold: float = 0.25,
    severe_drawdown_threshold: float = -0.15,
) -> str:
    """
    Classify a single market regime based on return, volatility, and drawdown.
    """

    if drawdown <= severe_drawdown_threshold and rolling_volatility >= high_volatility_threshold:
        return "Crisis"

    if rolling_return < return_threshold and rolling_volatility >= high_volatility_threshold:
        return "Bear / High Volatility"

    if rolling_return < return_threshold:
        return "Bear / Low Volatility"

    if rolling_return >= return_threshold and rolling_volatility >= high_volatility_threshold:
        return "Bull / High Volatility"

    return "Bull / Low Volatility"


def detect_market_regimes(
    portfolio_returns: pd.Series,
    window: int = 63,
    trading_days: int = 252,
    return_threshold: float = 0.00,
    high_volatility_threshold: float = 0.25,
    severe_drawdown_threshold: float = -0.15,
) -> pd.DataFrame:
    """
    Detect market regimes from portfolio returns.

    Parameters
    ----------
    portfolio_returns:
        Daily portfolio returns.

    window:
        Rolling window used for regime statistics.

    trading_days:
        Number of trading days used for annualization.

    Returns
    -------
    pd.DataFrame
        Regime detection table with rolling return, volatility,
        cumulative value, drawdown, and classified regime.
    """

    if portfolio_returns is None or portfolio_returns.empty:
        raise ValueError("portfolio_returns cannot be empty.")

    returns = portfolio_returns.dropna().copy()

    cumulative_value = (1 + returns).cumprod()
    running_max = cumulative_value.cummax()
    drawdown = (cumulative_value / running_max) - 1

    rolling_return = (
        (1 + returns)
        .rolling(window=window)
        .apply(lambda x: x.prod() - 1, raw=False)
    )

    rolling_volatility = returns.rolling(window=window).std() * (trading_days ** 0.5)

    regime_data = pd.DataFrame(
        {
            "daily_return": returns,
            "cumulative_value": cumulative_value,
            "drawdown": drawdown,
            "rolling_return": rolling_return,
            "rolling_volatility": rolling_volatility,
        }
    )

    regime_data["market_regime"] = regime_data.apply(
        lambda row: classify_market_regime(
            rolling_return=row["rolling_return"],
            rolling_volatility=row["rolling_volatility"],
            drawdown=row["drawdown"],
            return_threshold=return_threshold,
            high_volatility_threshold=high_volatility_threshold,
            severe_drawdown_threshold=severe_drawdown_threshold,
        )
        if pd.notna(row["rolling_return"]) and pd.notna(row["rolling_volatility"])
        else "Insufficient Data",
        axis=1,
    )

    return regime_data


def summarize_market_regimes(regime_data: pd.DataFrame) -> pd.DataFrame:
    """
    Summarize market regime frequency and average conditions.
    """

    if regime_data is None or regime_data.empty:
        raise ValueError("regime_data cannot be empty.")

    summary = (
        regime_data.groupby("market_regime")
        .agg(
            days=("market_regime", "count"),
            average_daily_return=("daily_return", "mean"),
            average_rolling_return=("rolling_return", "mean"),
            average_rolling_volatility=("rolling_volatility", "mean"),
            average_drawdown=("drawdown", "mean"),
            worst_drawdown=("drawdown", "min"),
        )
        .reset_index()
    )

    total_days = summary["days"].sum()
    summary["percentage_of_period"] = summary["days"] / total_days

    return summary.sort_values(by="days", ascending=False).reset_index(drop=True)


def get_latest_market_regime(regime_data: pd.DataFrame) -> dict:
    """
    Return the most recent detected market regime.
    """

    if regime_data is None or regime_data.empty:
        raise ValueError("regime_data cannot be empty.")

    latest_row = regime_data.dropna().iloc[-1]

    return {
        "date": latest_row.name,
        "market_regime": latest_row["market_regime"],
        "daily_return": latest_row["daily_return"],
        "cumulative_value": latest_row["cumulative_value"],
        "drawdown": latest_row["drawdown"],
        "rolling_return": latest_row["rolling_return"],
        "rolling_volatility": latest_row["rolling_volatility"],
    }