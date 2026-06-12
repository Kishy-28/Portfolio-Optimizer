import numpy as np
import pandas as pd

from src.returns import calculate_daily_returns


TRADING_DAYS_PER_YEAR = 252


def convert_weights_to_series(weights, tickers):
    return pd.Series(weights).reindex(tickers)


def should_rebalance(current_date, previous_date, frequency):
    if frequency is None or frequency == "none":
        return False

    if previous_date is None:
        return True

    if frequency == "monthly":
        return current_date.month != previous_date.month

    if frequency == "quarterly":
        current_quarter = (current_date.month - 1) // 3
        previous_quarter = (previous_date.month - 1) // 3
        return current_quarter != previous_quarter

    if frequency == "annually":
        return current_date.year != previous_date.year

    raise ValueError(
        "Rebalance frequency must be 'monthly', 'quarterly', 'annually', or 'none'."
    )


def calculate_transaction_cost(current_weights, target_weights, transaction_cost_rate):
    turnover = np.sum(np.abs(target_weights - current_weights))
    transaction_cost = turnover * transaction_cost_rate
    return transaction_cost


def calculate_portfolio_daily_returns(daily_returns, weights):
    weight_series = convert_weights_to_series(
        weights,
        daily_returns.columns
    )

    return daily_returns.dot(weight_series)


def calculate_rebalanced_portfolio_daily_returns(
    daily_returns,
    target_weights,
    rebalance_frequency="monthly",
    transaction_cost_rate=0.0
):
    target_weight_series = convert_weights_to_series(
        target_weights,
        daily_returns.columns
    )

    current_weights = target_weight_series.copy()
    portfolio_returns = []
    transaction_costs = []

    previous_date = None

    for current_date, asset_returns in daily_returns.iterrows():
        transaction_cost = 0.0

        if should_rebalance(current_date, previous_date, rebalance_frequency):
            transaction_cost = calculate_transaction_cost(
                current_weights=current_weights,
                target_weights=target_weight_series,
                transaction_cost_rate=transaction_cost_rate
            )

            current_weights = target_weight_series.copy()

        gross_portfolio_return = np.sum(current_weights * asset_returns)
        net_portfolio_return = gross_portfolio_return - transaction_cost

        portfolio_returns.append(net_portfolio_return)
        transaction_costs.append(transaction_cost)

        if gross_portfolio_return != -1:
            current_weights = (
                current_weights * (1 + asset_returns)
            ) / (1 + gross_portfolio_return)

        previous_date = current_date

    portfolio_returns = pd.Series(
        portfolio_returns,
        index=daily_returns.index,
        name="portfolio_return"
    )

    transaction_costs = pd.Series(
        transaction_costs,
        index=daily_returns.index,
        name="transaction_cost"
    )

    return portfolio_returns, transaction_costs


def calculate_growth_curve(daily_returns, initial_value=1.0):
    return initial_value * (1 + daily_returns).cumprod()


def calculate_drawdown(growth_curve):
    running_peak = growth_curve.cummax()
    drawdown = (growth_curve / running_peak) - 1
    return drawdown


def calculate_annualized_return(growth_curve):
    total_return = growth_curve.iloc[-1] / growth_curve.iloc[0] - 1
    num_days = len(growth_curve)

    return (1 + total_return) ** (TRADING_DAYS_PER_YEAR / num_days) - 1


def calculate_annualized_volatility(daily_returns):
    return daily_returns.std() * np.sqrt(TRADING_DAYS_PER_YEAR)


def calculate_backtest_sharpe_ratio(
    annualized_return,
    annualized_volatility,
    risk_free_rate=0.02
):
    if annualized_volatility == 0:
        return np.nan

    return (annualized_return - risk_free_rate) / annualized_volatility


def calculate_rolling_return(daily_returns, window=252):
    return (1 + daily_returns).rolling(window=window).apply(
        np.prod,
        raw=True
    ) - 1


def calculate_rolling_volatility(daily_returns, window=252):
    return daily_returns.rolling(window=window).std() * np.sqrt(TRADING_DAYS_PER_YEAR)


def calculate_rolling_sharpe_ratio(
    daily_returns,
    window=252,
    risk_free_rate=0.02
):
    rolling_return = calculate_rolling_return(daily_returns, window)
    rolling_volatility = calculate_rolling_volatility(daily_returns, window)

    return (rolling_return - risk_free_rate) / rolling_volatility


def run_portfolio_backtest(
    prices,
    weights,
    risk_free_rate=0.02,
    initial_value=1.0,
    rolling_window=252,
    rebalance_frequency="monthly",
    transaction_cost_rate=0.0
):
    daily_returns = calculate_daily_returns(prices)

    portfolio_daily_returns, transaction_costs = calculate_rebalanced_portfolio_daily_returns(
        daily_returns=daily_returns,
        target_weights=weights,
        rebalance_frequency=rebalance_frequency,
        transaction_cost_rate=transaction_cost_rate
    )

    growth_curve = calculate_growth_curve(
        portfolio_daily_returns,
        initial_value
    )

    drawdown = calculate_drawdown(growth_curve)

    total_return = growth_curve.iloc[-1] / growth_curve.iloc[0] - 1
    annualized_return = calculate_annualized_return(growth_curve)
    annualized_volatility = calculate_annualized_volatility(
        portfolio_daily_returns
    )

    sharpe_ratio = calculate_backtest_sharpe_ratio(
        annualized_return,
        annualized_volatility,
        risk_free_rate
    )

    max_drawdown = drawdown.min()
    total_transaction_cost = transaction_costs.sum()

    rolling_return = calculate_rolling_return(
        portfolio_daily_returns,
        rolling_window
    )

    rolling_volatility = calculate_rolling_volatility(
        portfolio_daily_returns,
        rolling_window
    )

    rolling_sharpe = calculate_rolling_sharpe_ratio(
        portfolio_daily_returns,
        rolling_window,
        risk_free_rate
    )

    return {
        "daily_returns": portfolio_daily_returns,
        "growth_curve": growth_curve,
        "drawdown": drawdown,
        "total_return": total_return,
        "annualized_return": annualized_return,
        "annualized_volatility": annualized_volatility,
        "sharpe_ratio": sharpe_ratio,
        "max_drawdown": max_drawdown,
        "transaction_costs": transaction_costs,
        "total_transaction_cost": total_transaction_cost,
        "rolling_return": rolling_return,
        "rolling_volatility": rolling_volatility,
        "rolling_sharpe": rolling_sharpe
    }


def run_benchmark_backtest(
    benchmark_prices,
    risk_free_rate=0.02,
    initial_value=1.0,
    rolling_window=252
):
    benchmark_daily_returns = calculate_daily_returns(benchmark_prices)

    if isinstance(benchmark_daily_returns, pd.DataFrame):
        benchmark_daily_returns = benchmark_daily_returns.iloc[:, 0]

    growth_curve = calculate_growth_curve(
        benchmark_daily_returns,
        initial_value
    )

    drawdown = calculate_drawdown(growth_curve)

    total_return = growth_curve.iloc[-1] / growth_curve.iloc[0] - 1
    annualized_return = calculate_annualized_return(growth_curve)
    annualized_volatility = calculate_annualized_volatility(
        benchmark_daily_returns
    )

    sharpe_ratio = calculate_backtest_sharpe_ratio(
        annualized_return,
        annualized_volatility,
        risk_free_rate
    )

    max_drawdown = drawdown.min()

    rolling_return = calculate_rolling_return(
        benchmark_daily_returns,
        rolling_window
    )

    rolling_volatility = calculate_rolling_volatility(
        benchmark_daily_returns,
        rolling_window
    )

    rolling_sharpe = calculate_rolling_sharpe_ratio(
        benchmark_daily_returns,
        rolling_window,
        risk_free_rate
    )

    return {
        "daily_returns": benchmark_daily_returns,
        "growth_curve": growth_curve,
        "drawdown": drawdown,
        "total_return": total_return,
        "annualized_return": annualized_return,
        "annualized_volatility": annualized_volatility,
        "sharpe_ratio": sharpe_ratio,
        "max_drawdown": max_drawdown,
        "rolling_return": rolling_return,
        "rolling_volatility": rolling_volatility,
        "rolling_sharpe": rolling_sharpe
    }