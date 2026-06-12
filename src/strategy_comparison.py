import pandas as pd

from src.backtester import run_portfolio_backtest
from src.performance import calculate_performance_summary
from src.drawdown import create_drawdown_summary
from src.value_at_risk import create_value_at_risk_summary
from src.advanced_risk import create_tail_risk_summary


def compare_strategies(
    prices,
    strategy_summary,
    tickers,
    benchmark_returns,
    risk_free_rate,
    initial_value,
    rolling_window,
    rebalance_frequency,
    transaction_cost_rate,
    value_at_risk_confidence_levels
):
    comparison_rows = []
    strategy_backtests = {}

    for _, strategy in strategy_summary.iterrows():
        strategy_name = strategy["strategy_name"]
        weights = strategy[tickers].values.tolist()

        backtest = run_portfolio_backtest(
            prices=prices,
            weights=weights,
            risk_free_rate=risk_free_rate,
            initial_value=initial_value,
            rolling_window=rolling_window,
            rebalance_frequency=rebalance_frequency,
            transaction_cost_rate=transaction_cost_rate
        )

        strategy_backtests[strategy_name] = backtest

        performance = calculate_performance_summary(
            portfolio_returns=backtest["daily_returns"],
            benchmark_returns=benchmark_returns,
            risk_free_rate=risk_free_rate
        )

        drawdown = create_drawdown_summary(
            backtest["growth_curve"]
        )

        value_at_risk = create_value_at_risk_summary(
            portfolio_returns=backtest["daily_returns"],
            confidence_levels=value_at_risk_confidence_levels
        )

        tail_risk = create_tail_risk_summary(
            portfolio_returns=backtest["daily_returns"],
            risk_free_rate=risk_free_rate
        )

        row = {
            "strategy_name": strategy_name,
            "strategy_type": strategy["strategy_type"],
            "annualized_return": backtest["annualized_return"],
            "annualized_volatility": backtest["annualized_volatility"],
            "sharpe_ratio": backtest["sharpe_ratio"],
            "alpha": performance["alpha"],
            "beta": performance["beta"],
            "tracking_error": performance["tracking_error"],
            "information_ratio": performance["information_ratio"],
            "active_return": performance["active_return"],
            "up_capture_ratio": performance["up_capture_ratio"],
            "down_capture_ratio": performance["down_capture_ratio"],
            "batting_average": performance["batting_average"],
            "sortino_ratio": tail_risk["sortino_ratio"],
            "max_drawdown": drawdown["max_drawdown"],
            "average_drawdown": drawdown["average_drawdown"],
            "historical_var_95": value_at_risk.loc[
                value_at_risk["confidence_level"] == 0.95,
                "historical_var"
            ].iloc[0],
            "historical_cvar_95": value_at_risk.loc[
                value_at_risk["confidence_level"] == 0.95,
                "historical_cvar"
            ].iloc[0],
            "final_portfolio_value": backtest["growth_curve"].iloc[-1]
        }

        comparison_rows.append(row)

    comparison_table = pd.DataFrame(comparison_rows)
    comparison_table.attrs["strategy_backtests"] = strategy_backtests

    return comparison_table


def rank_strategies(strategy_comparison):
    ranked = strategy_comparison.copy()

    ranked["return_rank"] = ranked["annualized_return"].rank(
        ascending=False
    )

    ranked["volatility_rank"] = ranked["annualized_volatility"].rank(
        ascending=True
    )

    ranked["sharpe_rank"] = ranked["sharpe_ratio"].rank(
        ascending=False
    )

    ranked["sortino_rank"] = ranked["sortino_ratio"].rank(
        ascending=False
    )

    ranked["drawdown_rank"] = ranked["max_drawdown"].rank(
        ascending=False
    )

    ranked["overall_rank_score"] = (
        ranked["return_rank"]
        + ranked["volatility_rank"]
        + ranked["sharpe_rank"]
        + ranked["sortino_rank"]
        + ranked["drawdown_rank"]
    )

    ranked["overall_rank"] = ranked["overall_rank_score"].rank(
        ascending=True
    )

    ranked.attrs["strategy_backtests"] = strategy_comparison.attrs.get(
        "strategy_backtests",
        {}
    )

    return ranked.sort_values("overall_rank")