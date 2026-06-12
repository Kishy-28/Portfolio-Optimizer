import numpy as np
import pandas as pd


def calculate_mean_returns(daily_returns):
    """
    Calculates the average daily return for each asset.
    """
    return daily_returns.mean()


def calculate_variance(daily_returns):
    """
    Calculates daily return variance for each asset.
    """
    return daily_returns.var()


def calculate_volatility(daily_returns):
    """
    Calculates daily volatility for each asset.
    """
    return daily_returns.std()


def calculate_annualized_volatility(daily_returns, trading_days=252):
    """
    Converts daily volatility into annualized volatility.
    """
    daily_volatility = calculate_volatility(daily_returns)
    return daily_volatility * np.sqrt(trading_days)


def calculate_covariance_matrix(daily_returns):
    """
    Calculates the daily covariance matrix of asset returns.
    """
    return daily_returns.cov()


def calculate_annualized_covariance_matrix(daily_returns, trading_days=252):
    """
    Converts the daily covariance matrix into an annualized covariance matrix.
    """
    covariance_matrix = calculate_covariance_matrix(daily_returns)
    return covariance_matrix * trading_days


def calculate_correlation_matrix(daily_returns):
    """
    Calculates the correlation matrix of asset returns.
    """
    return daily_returns.corr()


def calculate_beta(asset_returns, market_returns):
    """
    Calculates beta for each asset relative to a market benchmark.
    """
    combined_returns = pd.concat([asset_returns, market_returns], axis=1).dropna()

    asset_columns = asset_returns.columns
    market_column = market_returns.columns[0]

    market_variance = combined_returns[market_column].var()

    betas = {}

    for asset in asset_columns:
        covariance_with_market = combined_returns[asset].cov(
            combined_returns[market_column]
        )
        beta = covariance_with_market / market_variance
        betas[asset] = beta

    return pd.Series(betas)


def calculate_sharpe_ratio(
    annualized_returns,
    annualized_volatility,
    risk_free_rate=0.04
):
    """
    Calculates Sharpe ratio from annualized return and annualized volatility.
    """
    return (annualized_returns - risk_free_rate) / annualized_volatility