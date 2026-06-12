import pandas as pd

from src.returns import calculate_daily_returns
from src.risk_metrics import calculate_mean_returns, calculate_covariance_matrix
from src.optimizer import optimize_max_sharpe
from src.backtester import run_portfolio_backtest


def run_walk_forward_test(
    prices,
    tickers,
    risk_free_rate,
    train_window_days,
    test_window_days,
    min_weight,
    max_weight,
    initial_value,
    rolling_window,
    rebalance_frequency,
    transaction_cost_rate
):
    results = []

    start_index = 0

    while start_index + train_window_days + test_window_days <= len(prices):
        train_start = start_index
        train_end = start_index + train_window_days
        test_start = train_end
        test_end = test_start + test_window_days

        train_prices = prices.iloc[train_start:train_end]
        test_prices = prices.iloc[test_start:test_end]

        train_returns = calculate_daily_returns(train_prices)
        train_mean_returns = calculate_mean_returns(train_returns)
        train_covariance_matrix = calculate_covariance_matrix(train_returns)

        optimized_portfolio = optimize_max_sharpe(
            train_mean_returns,
            train_covariance_matrix,
            tickers,
            risk_free_rate=risk_free_rate,
            min_weight=min_weight,
            max_weight=max_weight
        )

        test_backtest = run_portfolio_backtest(
            prices=test_prices,
            weights=optimized_portfolio["weights"],
            risk_free_rate=risk_free_rate,
            initial_value=initial_value,
            rolling_window=rolling_window,
            rebalance_frequency=rebalance_frequency,
            transaction_cost_rate=transaction_cost_rate
        )

        row = {
            "train_start_date": train_prices.index[0],
            "train_end_date": train_prices.index[-1],
            "test_start_date": test_prices.index[0],
            "test_end_date": test_prices.index[-1],
            "test_total_return": test_backtest["total_return"],
            "test_annualized_return": test_backtest["annualized_return"],
            "test_annualized_volatility": test_backtest["annualized_volatility"],
            "test_sharpe_ratio": test_backtest["sharpe_ratio"],
            "test_max_drawdown": test_backtest["max_drawdown"],
            "test_final_value": test_backtest["growth_curve"].iloc[-1]
        }

        for ticker, weight in optimized_portfolio["weights"].items():
            row[f"{ticker}_weight"] = weight

        results.append(row)

        start_index += test_window_days

    return pd.DataFrame(results)


def summarize_walk_forward_results(walk_forward_results):
    if walk_forward_results.empty:
        return {
            "number_of_windows": 0,
            "average_test_return": 0,
            "average_test_volatility": 0,
            "average_test_sharpe": 0,
            "average_test_drawdown": 0,
            "best_window_return": 0,
            "worst_window_return": 0
        }

    return {
        "number_of_windows": len(walk_forward_results),
        "average_test_return": walk_forward_results["test_annualized_return"].mean(),
        "average_test_volatility": walk_forward_results["test_annualized_volatility"].mean(),
        "average_test_sharpe": walk_forward_results["test_sharpe_ratio"].mean(),
        "average_test_drawdown": walk_forward_results["test_max_drawdown"].mean(),
        "best_window_return": walk_forward_results["test_total_return"].max(),
        "worst_window_return": walk_forward_results["test_total_return"].min()
    }