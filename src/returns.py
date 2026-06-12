import numpy as np


def calculate_daily_returns(price_data):
    daily_returns = price_data.pct_change()
    return daily_returns.dropna()


def calculate_log_returns(price_data):
    log_returns = np.log(price_data / price_data.shift(1))
    return log_returns.dropna()


def calculate_cumulative_returns(daily_returns):
    cumulative_returns = (1 + daily_returns).cumprod() - 1
    return cumulative_returns


def calculate_annualized_returns(daily_returns, trading_days=252):
    mean_daily_returns = daily_returns.mean()
    annualized_returns = (1 + mean_daily_returns) ** trading_days - 1
    return annualized_returns