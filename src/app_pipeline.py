"""
app_pipeline.py

Interactive Streamlit application pipeline for the Portfolio Optimizer.

This module powers live app runs without modifying or replacing main.py.
It is designed to support flexible user-defined ticker universes while
preserving the export-based research engine as a separate fallback system.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pandas as pd

from src.adaptive_forecast import (
    create_adaptive_forecast_recommendation,
    create_forecast_model_evaluation,
    identify_best_forecast_model,
    identify_worst_forecast_model,
)
from src.advanced_risk import (
    create_concentration_summary,
    create_tail_risk_summary,
)
from src.backtester import run_portfolio_backtest
from src.data_loader import load_price_data
from src.drawdown import create_drawdown_summary
from src.forecast_evaluation import (
    calculate_realized_forward_returns,
    evaluate_forecast_accuracy,
    summarize_forecast_evaluation,
)
from src.forecast_models import create_expected_return_forecasts
from src.optimizer import (
    calculate_efficient_frontier,
    find_max_sharpe_portfolio,
    find_min_volatility_portfolio,
    generate_random_portfolios,
    optimize_max_sharpe,
    optimize_min_volatility,
)
from src.regime_attribution import (
    calculate_regime_attribution,
    identify_best_regime,
    identify_worst_regime,
)
from src.regime_detection import (
    detect_market_regimes,
    get_latest_market_regime,
    summarize_market_regimes,
)
from src.regime_forecast_analysis import (
    align_forecasts_with_regimes,
    identify_best_forecast_regime,
    identify_worst_forecast_regime,
    summarize_forecast_accuracy_by_regime,
)
from src.regime_forecast_dashboard import (
    create_regime_forecast_dashboard,
    create_regime_strategy_dashboard,
)
from src.regime_strategy_analysis import (
    compare_strategies_by_regime,
    identify_best_strategy_by_regime,
    identify_worst_strategy_by_regime,
)
from src.returns import calculate_daily_returns
from src.risk_dashboard import create_risk_dashboard
from src.risk_metrics import (
    calculate_correlation_matrix,
    calculate_covariance_matrix,
    calculate_mean_returns,
)
from src.stress_testing import (
    create_historical_stress_test,
    create_market_shock_analysis,
)
from src.value_at_risk import create_value_at_risk_summary


DEFAULT_RESEARCH_UNIVERSE = ["AAPL", "MSFT", "GOOGL", "AMZN"]

LIVE_VALUE_AT_RISK_CONFIDENCE_LEVELS = [0.95, 0.99]

LIVE_STRESS_TEST_PERIODS = {
    "COVID Crash": {
        "start_date": "2020-02-19",
        "end_date": "2020-03-23",
    },
    "2022 Inflation Shock": {
        "start_date": "2022-01-01",
        "end_date": "2022-10-14",
    },
}

LIVE_MARKET_SHOCK_LEVELS = [
    -0.30,
    -0.20,
    -0.10,
    0.10,
]

LIVE_REGIME_WINDOW = 63
LIVE_FORECAST_FORWARD_WINDOW = 63
LIVE_MOMENTUM_LOOKBACK_WINDOW = 126


@dataclass
class AppPipelineInputs:
    tickers: list[str]
    start_date: str
    end_date: str
    risk_free_rate: float
    min_weight: float
    max_weight: float
    portfolio_value: float = 1_000_000.0
    monte_carlo_portfolios: int = 5_000
    efficient_frontier_points: int = 50


def clean_tickers(tickers: list[str] | str) -> list[str]:
    if isinstance(tickers, str):
        tickers = tickers.split(",")

    cleaned_tickers = [
        ticker.strip().upper()
        for ticker in tickers
        if ticker and ticker.strip()
    ]

    cleaned_tickers = list(dict.fromkeys(cleaned_tickers))

    if not cleaned_tickers:
        raise ValueError("Please enter at least one valid ticker.")

    return cleaned_tickers


def validate_app_inputs(inputs: AppPipelineInputs) -> None:
    if len(inputs.tickers) < 2:
        raise ValueError("Please enter at least two tickers.")

    if inputs.start_date >= inputs.end_date:
        raise ValueError("Start date must be earlier than end date.")

    if inputs.min_weight < 0:
        raise ValueError("Minimum weight cannot be negative.")

    if inputs.max_weight <= 0:
        raise ValueError("Maximum weight must be greater than zero.")

    if inputs.min_weight > inputs.max_weight:
        raise ValueError("Minimum weight cannot exceed maximum weight.")

    if inputs.max_weight > 1:
        raise ValueError("Maximum weight cannot exceed 1.0, or 100%.")

    if inputs.min_weight * len(inputs.tickers) > 1:
        raise ValueError(
            "The minimum weight constraint is too high for this number of assets."
        )

    if inputs.max_weight * len(inputs.tickers) < 1:
        raise ValueError(
            "The maximum weight constraint is too low for this number of assets."
        )

    if inputs.portfolio_value <= 0:
        raise ValueError("Portfolio value must be greater than zero.")

    if inputs.monte_carlo_portfolios <= 0:
        raise ValueError("Monte Carlo portfolio count must be greater than zero.")

    if inputs.efficient_frontier_points <= 0:
        raise ValueError("Efficient frontier point count must be greater than zero.")


def create_universe_metadata(tickers: list[str]) -> dict[str, Any]:
    default_set = set(DEFAULT_RESEARCH_UNIVERSE)
    selected_set = set(tickers)

    uses_default_universe = selected_set == default_set
    added_tickers = sorted(selected_set - default_set)
    removed_tickers = sorted(default_set - selected_set)

    if uses_default_universe:
        universe_type = "Default Research Universe"
        universe_message = (
            "The live optimizer is using the original institutional research "
            "universe. Live analytics and exported research reports are aligned."
        )
    else:
        universe_type = "Custom Live Universe"
        universe_message = (
            "The live optimizer is using a custom ticker universe. Optimization, "
            "allocation, covariance, correlation, backtesting, risk analytics, "
            "regime analysis, forecast research, and return analytics are "
            "generated directly from the selected tickers."
        )

    return {
        "universe_type": universe_type,
        "uses_default_research_universe": uses_default_universe,
        "default_research_universe": DEFAULT_RESEARCH_UNIVERSE,
        "selected_universe": tickers,
        "added_tickers": added_tickers,
        "removed_tickers": removed_tickers,
        "universe_message": universe_message,
    }


def format_weights_table(portfolio: dict[str, Any]) -> pd.DataFrame:
    weights = portfolio.get("weights", {})

    weights_table = pd.DataFrame(
        {
            "ticker": list(weights.keys()),
            "weight": list(weights.values()),
        }
    )

    if not weights_table.empty:
        weights_table["weight_percent"] = weights_table["weight"] * 100

    return weights_table


def portfolio_summary_dict(
    name: str,
    portfolio: dict[str, Any],
) -> dict[str, Any]:
    return {
        "name": name,
        "return": portfolio.get("return"),
        "volatility": portfolio.get("volatility"),
        "sharpe_ratio": portfolio.get("sharpe_ratio"),
        "weights": portfolio.get("weights"),
        "weights_table": format_weights_table(portfolio),
    }


def build_portfolio_results_table(
    portfolios: dict[str, dict[str, Any]],
) -> pd.DataFrame:
    rows = []

    for portfolio_name, portfolio in portfolios.items():
        row = {
            "portfolio": portfolio_name,
            "return": portfolio.get("return"),
            "volatility": portfolio.get("volatility"),
            "sharpe_ratio": portfolio.get("sharpe_ratio"),
        }

        for ticker, weight in portfolio.get("weights", {}).items():
            row[ticker] = weight

        rows.append(row)

    return pd.DataFrame(rows)


def build_live_backtest_table(
    portfolio_backtest: dict[str, Any],
) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "strategy": "Live Optimized Max Sharpe Portfolio",
                "total_return": portfolio_backtest.get("total_return"),
                "annualized_return": portfolio_backtest.get(
                    "annualized_return"
                ),
                "annualized_volatility": portfolio_backtest.get(
                    "annualized_volatility"
                ),
                "sharpe_ratio": portfolio_backtest.get("sharpe_ratio"),
                "max_drawdown": portfolio_backtest.get("max_drawdown"),
                "total_transaction_cost": portfolio_backtest.get(
                    "total_transaction_cost",
                    0.0,
                ),
            }
        ]
    )


def build_live_drawdown_table(
    drawdown_summary: dict[str, Any],
) -> pd.DataFrame:
    return pd.DataFrame([drawdown_summary])


def build_live_concentration_table(
    concentration_summary: dict[str, Any],
) -> pd.DataFrame:
    return pd.DataFrame([concentration_summary])


def build_live_tail_risk_table(
    tail_risk_summary: dict[str, Any],
) -> pd.DataFrame:
    return pd.DataFrame([tail_risk_summary])


def build_live_risk_dashboard_table(
    risk_dashboard: dict[str, Any],
) -> pd.DataFrame:
    return pd.DataFrame([risk_dashboard])


def build_equal_weight_returns(
    daily_returns: pd.DataFrame,
) -> pd.Series:
    if daily_returns is None or daily_returns.empty:
        return pd.Series(dtype=float)

    equal_weights = pd.Series(
        1 / len(daily_returns.columns),
        index=daily_returns.columns,
    )

    return daily_returns.dot(equal_weights)


def build_weighted_returns(
    daily_returns: pd.DataFrame,
    weights: dict[str, float],
) -> pd.Series:
    if daily_returns is None or daily_returns.empty:
        return pd.Series(dtype=float)

    aligned_weights = pd.Series(weights).reindex(daily_returns.columns).fillna(0)

    return daily_returns.dot(aligned_weights)


def safe_dataframe_result(function, *args, **kwargs) -> pd.DataFrame:
    try:
        result = function(*args, **kwargs)

        if result is None:
            return pd.DataFrame()

        if isinstance(result, pd.DataFrame):
            return result

        if isinstance(result, dict):
            return pd.DataFrame([result])

        return pd.DataFrame(result)

    except Exception:
        return pd.DataFrame()


def safe_dict_result(function, *args, **kwargs) -> dict[str, Any] | None:
    try:
        result = function(*args, **kwargs)

        if result is None:
            return None

        if isinstance(result, dict):
            return result

        if isinstance(result, pd.Series):
            return result.to_dict()

        return None

    except Exception:
        return None


def create_live_regime_forecast_research(
    prices: pd.DataFrame,
    daily_returns: pd.DataFrame,
    portfolio_returns: pd.Series,
    optimized_weights: dict[str, float],
    risk_free_rate: float,
) -> dict[str, Any]:
    regime_data = safe_dataframe_result(
        detect_market_regimes,
        portfolio_returns=portfolio_returns,
        window=LIVE_REGIME_WINDOW,
    )

    market_regime_summary = safe_dataframe_result(
        summarize_market_regimes,
        regime_data,
    )

    latest_market_regime = safe_dict_result(
        get_latest_market_regime,
        regime_data,
    )

    regime_attribution = safe_dataframe_result(
        calculate_regime_attribution,
        regime_data=regime_data,
        risk_free_rate=risk_free_rate,
    )

    best_regime = safe_dict_result(
        identify_best_regime,
        regime_attribution,
    )

    worst_regime = safe_dict_result(
        identify_worst_regime,
        regime_attribution,
    )

    expected_return_forecasts = safe_dataframe_result(
        create_expected_return_forecasts,
        prices=prices,
        asset_returns=daily_returns,
        momentum_lookback_window=LIVE_MOMENTUM_LOOKBACK_WINDOW,
    )

    realized_forward_returns = safe_dataframe_result(
        calculate_realized_forward_returns,
        prices=prices,
        forward_window=LIVE_FORECAST_FORWARD_WINDOW,
    )

    forecast_evaluation = safe_dataframe_result(
        evaluate_forecast_accuracy,
        forecast_table=expected_return_forecasts,
        realized_forward_returns=realized_forward_returns,
    )

    forecast_evaluation_summary = safe_dataframe_result(
        summarize_forecast_evaluation,
        forecast_evaluation,
    )

    regime_forecast_analysis = safe_dataframe_result(
        align_forecasts_with_regimes,
        forecast_table=expected_return_forecasts,
        realized_forward_returns=realized_forward_returns,
        regime_data=regime_data,
    )

    regime_forecast_summary = safe_dataframe_result(
        summarize_forecast_accuracy_by_regime,
        regime_forecast_analysis,
    )

    best_forecast_regime = safe_dict_result(
        identify_best_forecast_regime,
        regime_forecast_summary,
    )

    worst_forecast_regime = safe_dict_result(
        identify_worst_forecast_regime,
        regime_forecast_summary,
    )

    forecast_model_evaluation = safe_dataframe_result(
        create_forecast_model_evaluation,
        forecast_table=expected_return_forecasts,
        realized_forward_returns=realized_forward_returns,
    )

    best_forecast_model = safe_dict_result(
        identify_best_forecast_model,
        forecast_model_evaluation,
    )

    worst_forecast_model = safe_dict_result(
        identify_worst_forecast_model,
        forecast_model_evaluation,
    )

    adaptive_forecast_recommendation = safe_dataframe_result(
        create_adaptive_forecast_recommendation,
        latest_market_regime=latest_market_regime,
        regime_forecast_summary=regime_forecast_summary,
        forecast_model_evaluation=forecast_model_evaluation,
    )

    equal_weight_returns = build_equal_weight_returns(daily_returns)
    optimized_strategy_returns = build_weighted_returns(
        daily_returns=daily_returns,
        weights=optimized_weights,
    )

    strategy_returns_dict = {
        "Live Optimized Max Sharpe": optimized_strategy_returns,
        "Live Equal Weight Portfolio": equal_weight_returns,
    }

    strategy_regime_analysis = safe_dataframe_result(
        compare_strategies_by_regime,
        strategy_returns_dict=strategy_returns_dict,
        regime_data=regime_data,
        risk_free_rate=risk_free_rate,
    )

    best_strategy_by_regime = safe_dataframe_result(
        identify_best_strategy_by_regime,
        strategy_regime_analysis,
    )

    worst_strategy_by_regime = safe_dataframe_result(
        identify_worst_strategy_by_regime,
        strategy_regime_analysis,
    )

    regime_forecast_dashboard = safe_dataframe_result(
        create_regime_forecast_dashboard,
        latest_market_regime=latest_market_regime,
        best_regime=best_regime,
        worst_regime=worst_regime,
        best_forecast_regime=best_forecast_regime,
        worst_forecast_regime=worst_forecast_regime,
        best_forecast_model=best_forecast_model,
        worst_forecast_model=worst_forecast_model,
        adaptive_forecast_recommendation=adaptive_forecast_recommendation,
    )

    regime_strategy_dashboard = safe_dataframe_result(
        create_regime_strategy_dashboard,
        best_strategy_by_regime=best_strategy_by_regime,
        worst_strategy_by_regime=worst_strategy_by_regime,
    )

    return {
        "market_regime_data": regime_data,
        "market_regime_summary": market_regime_summary,
        "latest_market_regime": latest_market_regime,
        "regime_attribution": regime_attribution,
        "best_regime": best_regime,
        "worst_regime": worst_regime,
        "expected_return_forecasts": expected_return_forecasts,
        "realized_forward_returns": realized_forward_returns,
        "forecast_evaluation": forecast_evaluation,
        "forecast_evaluation_summary": forecast_evaluation_summary,
        "regime_forecast_analysis": regime_forecast_analysis,
        "regime_forecast_summary": regime_forecast_summary,
        "best_forecast_regime": best_forecast_regime,
        "worst_forecast_regime": worst_forecast_regime,
        "forecast_model_evaluation": forecast_model_evaluation,
        "best_forecast_model": best_forecast_model,
        "worst_forecast_model": worst_forecast_model,
        "adaptive_forecast_recommendation": adaptive_forecast_recommendation,
        "strategy_regime_analysis": strategy_regime_analysis,
        "best_strategy_by_regime": best_strategy_by_regime,
        "worst_strategy_by_regime": worst_strategy_by_regime,
        "regime_forecast_dashboard": regime_forecast_dashboard,
        "regime_strategy_dashboard": regime_strategy_dashboard,
    }


def run_portfolio_optimizer(
    tickers: list[str] | str,
    start_date: str,
    end_date: str,
    risk_free_rate: float = 0.02,
    min_weight: float = 0.0,
    max_weight: float = 0.60,
    portfolio_value: float = 1_000_000.0,
    monte_carlo_portfolios: int = 5_000,
    efficient_frontier_points: int = 50,
) -> dict[str, Any]:
    cleaned_tickers = clean_tickers(tickers)

    inputs = AppPipelineInputs(
        tickers=cleaned_tickers,
        start_date=start_date,
        end_date=end_date,
        risk_free_rate=risk_free_rate,
        min_weight=min_weight,
        max_weight=max_weight,
        portfolio_value=portfolio_value,
        monte_carlo_portfolios=monte_carlo_portfolios,
        efficient_frontier_points=efficient_frontier_points,
    )

    validate_app_inputs(inputs)

    universe_metadata = create_universe_metadata(inputs.tickers)

    prices = load_price_data(
        tickers=inputs.tickers,
        start_date=inputs.start_date,
        end_date=inputs.end_date,
    )

    daily_returns = calculate_daily_returns(prices)
    mean_returns = calculate_mean_returns(daily_returns)
    covariance_matrix = calculate_covariance_matrix(daily_returns)
    correlation_matrix = calculate_correlation_matrix(daily_returns)

    monte_carlo_results = generate_random_portfolios(
        mean_returns=mean_returns,
        covariance_matrix=covariance_matrix,
        tickers=inputs.tickers,
        num_portfolios=inputs.monte_carlo_portfolios,
        risk_free_rate=inputs.risk_free_rate,
        min_weight=inputs.min_weight,
        max_weight=inputs.max_weight,
    )

    best_simulated_portfolio = find_max_sharpe_portfolio(
        portfolio_results=monte_carlo_results,
        tickers=inputs.tickers,
    )

    lowest_risk_simulated_portfolio = find_min_volatility_portfolio(
        portfolio_results=monte_carlo_results,
        tickers=inputs.tickers,
    )

    optimized_max_sharpe_portfolio = optimize_max_sharpe(
        mean_returns=mean_returns,
        covariance_matrix=covariance_matrix,
        tickers=inputs.tickers,
        risk_free_rate=inputs.risk_free_rate,
        min_weight=inputs.min_weight,
        max_weight=inputs.max_weight,
    )

    optimized_min_volatility_portfolio = optimize_min_volatility(
        mean_returns=mean_returns,
        covariance_matrix=covariance_matrix,
        tickers=inputs.tickers,
        risk_free_rate=inputs.risk_free_rate,
        min_weight=inputs.min_weight,
        max_weight=inputs.max_weight,
    )

    portfolio_backtest = run_portfolio_backtest(
        prices=prices,
        weights=optimized_max_sharpe_portfolio["weights"],
        risk_free_rate=inputs.risk_free_rate,
        initial_value=1.0,
        rolling_window=252,
        rebalance_frequency="monthly",
        transaction_cost_rate=0.001,
    )

    portfolio_returns = portfolio_backtest["daily_returns"]
    growth_curve = portfolio_backtest["growth_curve"]
    optimized_weights = optimized_max_sharpe_portfolio["weights"]

    drawdown_summary = create_drawdown_summary(
        growth_curve
    )

    value_at_risk_summary = create_value_at_risk_summary(
        portfolio_returns=portfolio_returns,
        confidence_levels=LIVE_VALUE_AT_RISK_CONFIDENCE_LEVELS,
    )

    stress_test_results = create_historical_stress_test(
        portfolio_returns=portfolio_returns,
        stress_periods=LIVE_STRESS_TEST_PERIODS,
    )

    market_shock_analysis = create_market_shock_analysis(
        weights=optimized_weights,
        shock_levels=LIVE_MARKET_SHOCK_LEVELS,
    )

    concentration_summary = create_concentration_summary(
        optimized_weights
    )

    tail_risk_summary = create_tail_risk_summary(
        portfolio_returns=portfolio_returns,
        risk_free_rate=inputs.risk_free_rate,
    )

    live_risk_dashboard = create_risk_dashboard(
        drawdown_summary=drawdown_summary,
        value_at_risk_summary=value_at_risk_summary,
        stress_test_results=stress_test_results,
        concentration_summary=concentration_summary,
        tail_risk_summary=tail_risk_summary,
    )

    live_backtest_table = build_live_backtest_table(
        portfolio_backtest
    )

    live_drawdown_table = build_live_drawdown_table(
        drawdown_summary
    )

    live_concentration_table = build_live_concentration_table(
        concentration_summary
    )

    live_tail_risk_table = build_live_tail_risk_table(
        tail_risk_summary
    )

    live_risk_dashboard_table = build_live_risk_dashboard_table(
        live_risk_dashboard
    )

    live_regime_forecast_research = create_live_regime_forecast_research(
        prices=prices,
        daily_returns=daily_returns,
        portfolio_returns=portfolio_returns,
        optimized_weights=optimized_weights,
        risk_free_rate=inputs.risk_free_rate,
    )

    efficient_frontier = calculate_efficient_frontier(
        mean_returns=mean_returns,
        covariance_matrix=covariance_matrix,
        tickers=inputs.tickers,
        num_points=inputs.efficient_frontier_points,
        risk_free_rate=inputs.risk_free_rate,
        min_weight=inputs.min_weight,
        max_weight=inputs.max_weight,
    )

    live_portfolios = {
        "Best Simulated Sharpe": best_simulated_portfolio,
        "Optimized Max Sharpe": optimized_max_sharpe_portfolio,
        "Best Simulated Min Volatility": lowest_risk_simulated_portfolio,
        "Optimized Min Volatility": optimized_min_volatility_portfolio,
    }

    portfolio_results_table = build_portfolio_results_table(live_portfolios)

    return {
        "inputs": {
            "tickers": inputs.tickers,
            "start_date": inputs.start_date,
            "end_date": inputs.end_date,
            "risk_free_rate": inputs.risk_free_rate,
            "min_weight": inputs.min_weight,
            "max_weight": inputs.max_weight,
            "portfolio_value": inputs.portfolio_value,
            "monte_carlo_portfolios": inputs.monte_carlo_portfolios,
            "efficient_frontier_points": inputs.efficient_frontier_points,
        },
        "universe_metadata": universe_metadata,
        "prices": prices,
        "daily_returns": daily_returns,
        "mean_returns": mean_returns,
        "covariance_matrix": covariance_matrix,
        "correlation_matrix": correlation_matrix,
        "monte_carlo_results": monte_carlo_results,
        "efficient_frontier": efficient_frontier,
        "best_simulated_portfolio": best_simulated_portfolio,
        "lowest_risk_simulated_portfolio": lowest_risk_simulated_portfolio,
        "optimized_max_sharpe_portfolio": optimized_max_sharpe_portfolio,
        "optimized_min_volatility_portfolio": optimized_min_volatility_portfolio,
        "portfolio_backtest": portfolio_backtest,
        "live_backtest_table": live_backtest_table,
        "drawdown_summary": drawdown_summary,
        "live_drawdown_table": live_drawdown_table,
        "value_at_risk_summary": value_at_risk_summary,
        "stress_test_results": stress_test_results,
        "market_shock_analysis": market_shock_analysis,
        "concentration_summary": concentration_summary,
        "live_concentration_table": live_concentration_table,
        "tail_risk_summary": tail_risk_summary,
        "live_tail_risk_table": live_tail_risk_table,
        "live_risk_dashboard": live_risk_dashboard,
        "live_risk_dashboard_table": live_risk_dashboard_table,
        "portfolio_results_table": portfolio_results_table,
        "max_sharpe_summary": portfolio_summary_dict(
            "Optimized Max Sharpe",
            optimized_max_sharpe_portfolio,
        ),
        "min_volatility_summary": portfolio_summary_dict(
            "Optimized Min Volatility",
            optimized_min_volatility_portfolio,
        ),
        **live_regime_forecast_research,
    }