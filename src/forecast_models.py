"""
Expected Return Forecast Models

Phase 9.3 — Regime & Forecast Research

This module estimates forward-looking expected returns using
historical, exponentially weighted, momentum-based, and combined
forecast models.
"""

import pandas as pd


def calculate_historical_mean_forecast(
    asset_returns,
    trading_days=252
):
    """
    Estimate expected returns using historical average returns.
    """

    if asset_returns is None or asset_returns.empty:
        raise ValueError("asset_returns cannot be empty.")

    return asset_returns.mean() * trading_days


def calculate_exponential_weighted_forecast(
    asset_returns,
    span=63,
    trading_days=252
):
    """
    Estimate expected returns using exponentially weighted average returns.
    """

    if asset_returns is None or asset_returns.empty:
        raise ValueError("asset_returns cannot be empty.")

    exponential_returns = asset_returns.ewm(span=span).mean()

    return exponential_returns.iloc[-1] * trading_days


def calculate_momentum_forecast(
    prices,
    lookback_window=126
):
    """
    Estimate expected returns using price momentum over a lookback window.
    """

    if prices is None or prices.empty:
        raise ValueError("prices cannot be empty.")

    if len(prices) < lookback_window:
        raise ValueError("Not enough price data for the momentum lookback window.")

    momentum_returns = prices.iloc[-1] / prices.iloc[-lookback_window] - 1

    return momentum_returns


def calculate_combined_forecast(
    historical_forecast,
    exponential_forecast,
    momentum_forecast,
    historical_weight=0.40,
    exponential_weight=0.40,
    momentum_weight=0.20
):
    """
    Combine multiple expected return forecasts into one blended forecast.
    """

    total_weight = historical_weight + exponential_weight + momentum_weight

    if abs(total_weight - 1.0) > 1e-8:
        raise ValueError("Forecast model weights must sum to 1.0.")

    combined_forecast = (
        historical_forecast * historical_weight
        + exponential_forecast * exponential_weight
        + momentum_forecast * momentum_weight
    )

    return combined_forecast


def create_expected_return_forecasts(
    prices,
    asset_returns,
    trading_days=252,
    exponential_span=63,
    momentum_lookback_window=126,
    historical_weight=0.40,
    exponential_weight=0.40,
    momentum_weight=0.20
):
    """
    Create a full expected return forecast table.
    """

    if prices is None or prices.empty:
        raise ValueError("prices cannot be empty.")

    if asset_returns is None or asset_returns.empty:
        raise ValueError("asset_returns cannot be empty.")

    historical_forecast = calculate_historical_mean_forecast(
        asset_returns=asset_returns,
        trading_days=trading_days
    )

    exponential_forecast = calculate_exponential_weighted_forecast(
        asset_returns=asset_returns,
        span=exponential_span,
        trading_days=trading_days
    )

    momentum_forecast = calculate_momentum_forecast(
        prices=prices,
        lookback_window=momentum_lookback_window
    )

    combined_forecast = calculate_combined_forecast(
        historical_forecast=historical_forecast,
        exponential_forecast=exponential_forecast,
        momentum_forecast=momentum_forecast,
        historical_weight=historical_weight,
        exponential_weight=exponential_weight,
        momentum_weight=momentum_weight
    )

    forecast_table = pd.DataFrame(
        {
            "historical_mean_forecast": historical_forecast,
            "exponential_weighted_forecast": exponential_forecast,
            "momentum_forecast": momentum_forecast,
            "combined_forecast": combined_forecast
        }
    )

    forecast_table.index.name = "ticker"

    return forecast_table.reset_index()