import pandas as pd

from src.returns import calculate_daily_returns
from src.risk_metrics import calculate_mean_returns, calculate_covariance_matrix
from src.optimizer import optimize_max_sharpe
from src.backtester import run_portfolio_backtest


def run_sensitivity_analysis(
    prices,
    tickers,
    risk_free_rate_values,
    min_weight_values,
    max_weight_values,
    initial_value,
    rolling_window,
    rebalance_frequency,
    transaction_cost_rate
):
    results = []

    daily_returns = calculate_daily_returns(prices)
    mean_returns = calculate_mean_returns(daily_returns)
    covariance_matrix = calculate_covariance_matrix(daily_returns)

    for risk_free_rate in risk_free_rate_values:
        for min_weight in min_weight_values:
            for max_weight in max_weight_values:
                if min_weight > max_weight:
                    continue

                optimized_portfolio = optimize_max_sharpe(
                    mean_returns,
                    covariance_matrix,
                    tickers,
                    risk_free_rate=risk_free_rate,
                    min_weight=min_weight,
                    max_weight=max_weight
                )

                backtest = run_portfolio_backtest(
                    prices=prices,
                    weights=optimized_portfolio["weights"],
                    risk_free_rate=risk_free_rate,
                    initial_value=initial_value,
                    rolling_window=rolling_window,
                    rebalance_frequency=rebalance_frequency,
                    transaction_cost_rate=transaction_cost_rate
                )

                row = {
                    "risk_free_rate": risk_free_rate,
                    "min_weight": min_weight,
                    "max_weight": max_weight,
                    "expected_return": optimized_portfolio["return"],
                    "expected_volatility": optimized_portfolio["volatility"],
                    "expected_sharpe_ratio": optimized_portfolio["sharpe_ratio"],
                    "backtest_total_return": backtest["total_return"],
                    "backtest_annualized_return": backtest["annualized_return"],
                    "backtest_annualized_volatility": backtest["annualized_volatility"],
                    "backtest_sharpe_ratio": backtest["sharpe_ratio"],
                    "backtest_max_drawdown": backtest["max_drawdown"],
                    "backtest_final_value": backtest["growth_curve"].iloc[-1]
                }

                for ticker, weight in optimized_portfolio["weights"].items():
                    row[f"{ticker}_weight"] = weight

                results.append(row)

    return pd.DataFrame(results)


def summarize_sensitivity_analysis(sensitivity_results):
    if sensitivity_results.empty:
        return {
            "number_of_tests": 0,
            "average_sharpe_ratio": 0,
            "minimum_sharpe_ratio": 0,
            "maximum_sharpe_ratio": 0,
            "average_total_return": 0,
            "minimum_total_return": 0,
            "maximum_total_return": 0,
            "average_max_drawdown": 0
        }

    return {
        "number_of_tests": len(sensitivity_results),
        "average_sharpe_ratio": sensitivity_results["backtest_sharpe_ratio"].mean(),
        "minimum_sharpe_ratio": sensitivity_results["backtest_sharpe_ratio"].min(),
        "maximum_sharpe_ratio": sensitivity_results["backtest_sharpe_ratio"].max(),
        "average_total_return": sensitivity_results["backtest_total_return"].mean(),
        "minimum_total_return": sensitivity_results["backtest_total_return"].min(),
        "maximum_total_return": sensitivity_results["backtest_total_return"].max(),
        "average_max_drawdown": sensitivity_results["backtest_max_drawdown"].mean()
    }