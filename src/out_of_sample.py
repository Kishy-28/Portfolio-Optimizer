import pandas as pd

from src.returns import calculate_daily_returns
from src.risk_metrics import calculate_mean_returns, calculate_covariance_matrix
from src.optimizer import optimize_max_sharpe
from src.backtester import run_portfolio_backtest


def run_out_of_sample_test(
    prices,
    tickers,
    risk_free_rate,
    train_fraction,
    min_weight,
    max_weight,
    initial_value,
    rolling_window,
    rebalance_frequency,
    transaction_cost_rate
):
    split_index = int(len(prices) * train_fraction)

    train_prices = prices.iloc[:split_index]
    test_prices = prices.iloc[split_index:]

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

    result = {
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
        result[f"{ticker}_weight"] = weight

    return pd.DataFrame([result])


def summarize_out_of_sample_results(out_of_sample_results):
    if out_of_sample_results.empty:
        return {
            "test_total_return": 0,
            "test_annualized_return": 0,
            "test_annualized_volatility": 0,
            "test_sharpe_ratio": 0,
            "test_max_drawdown": 0,
            "test_final_value": 0
        }

    row = out_of_sample_results.iloc[0]

    return {
        "test_total_return": row["test_total_return"],
        "test_annualized_return": row["test_annualized_return"],
        "test_annualized_volatility": row["test_annualized_volatility"],
        "test_sharpe_ratio": row["test_sharpe_ratio"],
        "test_max_drawdown": row["test_max_drawdown"],
        "test_final_value": row["test_final_value"]
    }