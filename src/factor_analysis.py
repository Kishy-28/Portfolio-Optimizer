import numpy as np
import pandas as pd


TRADING_DAYS_PER_YEAR = 252


def align_factor_data(portfolio_returns, benchmark_returns):
    combined_data = pd.concat(
        [portfolio_returns, benchmark_returns],
        axis=1
    ).dropna()

    combined_data.columns = ["portfolio", "benchmark"]

    return combined_data


def calculate_factor_beta(portfolio_returns, benchmark_returns):
    data = align_factor_data(
        portfolio_returns,
        benchmark_returns
    )

    benchmark_variance = data["benchmark"].var()

    if benchmark_variance == 0:
        return np.nan

    covariance = data["portfolio"].cov(data["benchmark"])

    return covariance / benchmark_variance


def calculate_factor_alpha(
    portfolio_returns,
    benchmark_returns,
    risk_free_rate=0.02
):
    data = align_factor_data(
        portfolio_returns,
        benchmark_returns
    )

    beta = calculate_factor_beta(
        portfolio_returns,
        benchmark_returns
    )

    portfolio_return = data["portfolio"].mean() * TRADING_DAYS_PER_YEAR
    benchmark_return = data["benchmark"].mean() * TRADING_DAYS_PER_YEAR

    alpha = (
        portfolio_return
        - risk_free_rate
        - beta * (benchmark_return - risk_free_rate)
    )

    return alpha


def calculate_r_squared(portfolio_returns, benchmark_returns):
    data = align_factor_data(
        portfolio_returns,
        benchmark_returns
    )

    correlation = data["portfolio"].corr(data["benchmark"])

    return correlation ** 2


def calculate_residual_returns(portfolio_returns, benchmark_returns):
    data = align_factor_data(
        portfolio_returns,
        benchmark_returns
    )

    beta = calculate_factor_beta(
        portfolio_returns,
        benchmark_returns
    )

    predicted_returns = beta * data["benchmark"]

    residual_returns = data["portfolio"] - predicted_returns

    return residual_returns


def calculate_residual_volatility(
    portfolio_returns,
    benchmark_returns
):
    residual_returns = calculate_residual_returns(
        portfolio_returns,
        benchmark_returns
    )

    return residual_returns.std() * np.sqrt(TRADING_DAYS_PER_YEAR)


def calculate_market_capture(
    portfolio_returns,
    benchmark_returns
):
    data = align_factor_data(
        portfolio_returns,
        benchmark_returns
    )

    correlation = data["portfolio"].corr(data["benchmark"])

    beta = calculate_factor_beta(
        portfolio_returns,
        benchmark_returns
    )

    r_squared = correlation ** 2

    return {
        "correlation": correlation,
        "beta": beta,
        "r_squared": r_squared
    }


def calculate_factor_summary(
    portfolio_returns,
    benchmark_returns,
    risk_free_rate=0.02
):
    market_capture = calculate_market_capture(
        portfolio_returns,
        benchmark_returns
    )

    return {
        "factor_alpha": calculate_factor_alpha(
            portfolio_returns,
            benchmark_returns,
            risk_free_rate
        ),
        "factor_beta": market_capture["beta"],
        "correlation": market_capture["correlation"],
        "r_squared": market_capture["r_squared"],
        "residual_volatility": calculate_residual_volatility(
            portfolio_returns,
            benchmark_returns
        )
    }