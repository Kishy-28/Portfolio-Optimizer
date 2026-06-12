import numpy as np
import pandas as pd


def calculate_hhi(weights):
    return sum(weight ** 2 for weight in weights.values())


def calculate_effective_number_of_positions(weights):
    hhi = calculate_hhi(weights)

    if hhi == 0:
        return 0.0

    return 1 / hhi


def create_concentration_summary(weights):
    hhi = calculate_hhi(weights)
    effective_positions = calculate_effective_number_of_positions(weights)
    max_weight = max(weights.values())

    return {
        "hhi": hhi,
        "effective_number_of_positions": effective_positions,
        "max_position_weight": max_weight
    }


def calculate_downside_deviation(returns, minimum_acceptable_return=0.0):
    downside_returns = returns[returns < minimum_acceptable_return]

    if downside_returns.empty:
        return 0.0

    return np.sqrt(
        ((downside_returns - minimum_acceptable_return) ** 2).mean()
    )


def calculate_sortino_ratio(
    returns,
    risk_free_rate=0.0,
    trading_days=252
):
    daily_risk_free_rate = risk_free_rate / trading_days
    excess_returns = returns - daily_risk_free_rate

    downside_deviation = calculate_downside_deviation(
        returns=returns,
        minimum_acceptable_return=daily_risk_free_rate
    )

    if downside_deviation == 0:
        return 0.0

    return (
        excess_returns.mean()
        / downside_deviation
        * np.sqrt(trading_days)
    )


def calculate_tail_ratio(returns):
    downside_tail = abs(returns.quantile(0.05))
    upside_tail = returns.quantile(0.95)

    if downside_tail == 0:
        return 0.0

    return upside_tail / downside_tail


def calculate_tail_volatility(returns):
    tail_returns = returns[returns <= returns.quantile(0.05)]

    if tail_returns.empty:
        return 0.0

    return tail_returns.std()


def create_tail_risk_summary(
    portfolio_returns,
    risk_free_rate=0.0
):
    downside_deviation = calculate_downside_deviation(
        portfolio_returns
    )

    sortino_ratio = calculate_sortino_ratio(
        returns=portfolio_returns,
        risk_free_rate=risk_free_rate
    )

    tail_ratio = calculate_tail_ratio(
        portfolio_returns
    )

    tail_volatility = calculate_tail_volatility(
        portfolio_returns
    )

    return {
        "downside_deviation": downside_deviation,
        "sortino_ratio": sortino_ratio,
        "tail_ratio": tail_ratio,
        "tail_volatility": tail_volatility
    }