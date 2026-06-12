import numpy as np
import pandas as pd


TRADING_DAYS_PER_YEAR = 252


def align_return_series(portfolio_returns, benchmark_returns):
    combined_returns = pd.concat(
        [portfolio_returns, benchmark_returns],
        axis=1
    ).dropna()

    combined_returns.columns = ["portfolio", "benchmark"]

    return combined_returns["portfolio"], combined_returns["benchmark"]


def calculate_active_returns(portfolio_returns, benchmark_returns):
    portfolio_returns, benchmark_returns = align_return_series(
        portfolio_returns,
        benchmark_returns
    )

    return portfolio_returns - benchmark_returns


def calculate_beta(portfolio_returns, benchmark_returns):
    portfolio_returns, benchmark_returns = align_return_series(
        portfolio_returns,
        benchmark_returns
    )

    benchmark_variance = benchmark_returns.var()

    if benchmark_variance == 0:
        return np.nan

    covariance = portfolio_returns.cov(benchmark_returns)
    return covariance / benchmark_variance


def calculate_alpha(
    portfolio_returns,
    benchmark_returns,
    risk_free_rate=0.02
):
    portfolio_returns, benchmark_returns = align_return_series(
        portfolio_returns,
        benchmark_returns
    )

    beta = calculate_beta(portfolio_returns, benchmark_returns)

    portfolio_annual_return = portfolio_returns.mean() * TRADING_DAYS_PER_YEAR
    benchmark_annual_return = benchmark_returns.mean() * TRADING_DAYS_PER_YEAR

    alpha = (
        portfolio_annual_return
        - risk_free_rate
        - beta * (benchmark_annual_return - risk_free_rate)
    )

    return alpha


def calculate_tracking_error(portfolio_returns, benchmark_returns):
    active_returns = calculate_active_returns(
        portfolio_returns,
        benchmark_returns
    )

    return active_returns.std() * np.sqrt(TRADING_DAYS_PER_YEAR)


def calculate_information_ratio(portfolio_returns, benchmark_returns):
    active_returns = calculate_active_returns(
        portfolio_returns,
        benchmark_returns
    )

    annualized_active_return = active_returns.mean() * TRADING_DAYS_PER_YEAR
    tracking_error = calculate_tracking_error(
        portfolio_returns,
        benchmark_returns
    )

    if tracking_error == 0:
        return np.nan

    return annualized_active_return / tracking_error


def calculate_up_capture_ratio(portfolio_returns, benchmark_returns):
    portfolio_returns, benchmark_returns = align_return_series(
        portfolio_returns,
        benchmark_returns
    )

    up_market_days = benchmark_returns > 0

    if up_market_days.sum() == 0:
        return np.nan

    portfolio_up_return = portfolio_returns[up_market_days].mean()
    benchmark_up_return = benchmark_returns[up_market_days].mean()

    if benchmark_up_return == 0:
        return np.nan

    return portfolio_up_return / benchmark_up_return


def calculate_down_capture_ratio(portfolio_returns, benchmark_returns):
    portfolio_returns, benchmark_returns = align_return_series(
        portfolio_returns,
        benchmark_returns
    )

    down_market_days = benchmark_returns < 0

    if down_market_days.sum() == 0:
        return np.nan

    portfolio_down_return = portfolio_returns[down_market_days].mean()
    benchmark_down_return = benchmark_returns[down_market_days].mean()

    if benchmark_down_return == 0:
        return np.nan

    return portfolio_down_return / benchmark_down_return


def calculate_batting_average(portfolio_returns, benchmark_returns):
    active_returns = calculate_active_returns(
        portfolio_returns,
        benchmark_returns
    )

    if len(active_returns) == 0:
        return np.nan

    return (active_returns > 0).mean()


def calculate_average_active_return(portfolio_returns, benchmark_returns):
    active_returns = calculate_active_returns(
        portfolio_returns,
        benchmark_returns
    )

    return active_returns.mean() * TRADING_DAYS_PER_YEAR


def calculate_performance_summary(
    portfolio_returns,
    benchmark_returns,
    risk_free_rate=0.02
):
    return {
        "alpha": calculate_alpha(
            portfolio_returns,
            benchmark_returns,
            risk_free_rate
        ),
        "beta": calculate_beta(
            portfolio_returns,
            benchmark_returns
        ),
        "tracking_error": calculate_tracking_error(
            portfolio_returns,
            benchmark_returns
        ),
        "information_ratio": calculate_information_ratio(
            portfolio_returns,
            benchmark_returns
        ),
        "active_return": calculate_average_active_return(
            portfolio_returns,
            benchmark_returns
        ),
        "up_capture_ratio": calculate_up_capture_ratio(
            portfolio_returns,
            benchmark_returns
        ),
        "down_capture_ratio": calculate_down_capture_ratio(
            portfolio_returns,
            benchmark_returns
        ),
        "batting_average": calculate_batting_average(
            portfolio_returns,
            benchmark_returns
        )
    }