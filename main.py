from src.config import (
    TICKERS,
    START_DATE,
    END_DATE,
    BENCHMARK_TICKER,
    FACTOR_TICKERS,
    SECTOR_MAP,
    MAX_SECTOR_WEIGHT,
    RISK_FREE_RATE,
    NUM_PORTFOLIOS,
    NUM_FRONTIER_POINTS,
    MIN_WEIGHT,
    MAX_WEIGHT,
    MAX_RISK_CONTRIBUTION,
    MAX_TURNOVER,
    MAX_PERCENT_OF_DAILY_VOLUME,
    MARKET_IMPACT_COEFFICIENT,
    VALUE_AT_RISK_CONFIDENCE_LEVELS,
    STRESS_TEST_PERIODS,
    SCENARIO_RETURNS,
    MARKET_SHOCK_LEVELS,
    ROLLING_WINDOW,
    REBALANCE_FREQUENCY,
    TRANSACTION_COST_RATE,
    SAVE_PLOT_PATH,
    SAVE_BACKTEST_PLOT_PATH,
    SAVE_DRAWDOWN_PLOT_PATH,
    SAVE_ROLLING_RETURN_PLOT_PATH,
    SAVE_ROLLING_VOLATILITY_PLOT_PATH,
    SAVE_ROLLING_SHARPE_PLOT_PATH,
    EXPORT_RESULTS_PATH,
    EXPORT_BACKTEST_RESULTS_PATH,
    EXPORT_PERFORMANCE_SUMMARY_PATH,
    EXPORT_FACTOR_SUMMARY_PATH,
    EXPORT_FACTOR_MODEL_SUMMARY_PATH,
    EXPORT_RETURN_ATTRIBUTION_PATH,
    EXPORT_RISK_CONTRIBUTION_PATH,
    EXPORT_CONSTRAINT_DIAGNOSTICS_PATH,
    EXPORT_TRADE_LIST_PATH,
    EXPORT_REBALANCE_SUMMARY_PATH,
    EXPORT_LIQUIDITY_DIAGNOSTICS_PATH,
    EXPORT_MARKET_IMPACT_DIAGNOSTICS_PATH,
    EXPORT_CAPACITY_DIAGNOSTICS_PATH,
    EXPORT_CAPACITY_SUMMARY_PATH,
    EXPORT_DRAWDOWN_SUMMARY_PATH,
    EXPORT_VALUE_AT_RISK_SUMMARY_PATH,
    EXPORT_STRESS_TEST_RESULTS_PATH,
    EXPORT_SCENARIO_ANALYSIS_PATH,
    EXPORT_MARKET_SHOCK_ANALYSIS_PATH,
    EXPORT_CONCENTRATION_SUMMARY_PATH,
    EXPORT_TAIL_RISK_SUMMARY_PATH,
    EXPORT_RISK_DASHBOARD_PATH,
    EXPORT_RISK_GOVERNANCE_REPORT_PATH,
    EXPORT_STRATEGY_SUMMARY_PATH,
    EXPORT_STRATEGY_COMPARISON_PATH,
    WALK_FORWARD_TRAIN_WINDOW_DAYS,
    WALK_FORWARD_TEST_WINDOW_DAYS,
    EXPORT_WALK_FORWARD_RESULTS_PATH,
    EXPORT_WALK_FORWARD_SUMMARY_PATH,
    OUT_OF_SAMPLE_TRAIN_FRACTION,
    EXPORT_OUT_OF_SAMPLE_RESULTS_PATH,
    EXPORT_OUT_OF_SAMPLE_SUMMARY_PATH,
    SENSITIVITY_RISK_FREE_RATE_VALUES,
    SENSITIVITY_MIN_WEIGHT_VALUES,
    SENSITIVITY_MAX_WEIGHT_VALUES,
    MINIMUM_ACCEPTABLE_ROBUSTNESS_SHARPE,
    MAXIMUM_ACCEPTABLE_ROBUSTNESS_DRAWDOWN,
    EXPORT_SENSITIVITY_ANALYSIS_PATH,
    EXPORT_SENSITIVITY_SUMMARY_PATH,
    EXPORT_ROBUSTNESS_DASHBOARD_PATH,
    EXPORT_ROBUSTNESS_SUMMARY_PATH,
    REGIME_DETECTION_WINDOW,
    REGIME_DETECTION_TRADING_DAYS,
    REGIME_RETURN_THRESHOLD,
    REGIME_HIGH_VOLATILITY_THRESHOLD,
    REGIME_SEVERE_DRAWDOWN_THRESHOLD,
    EXPORT_MARKET_REGIME_DATA_PATH,
    EXPORT_MARKET_REGIME_SUMMARY_PATH,
    EXPORT_REGIME_ATTRIBUTION_PATH,
    FORECAST_TRADING_DAYS,
    FORECAST_EXPONENTIAL_SPAN,
    FORECAST_MOMENTUM_LOOKBACK_WINDOW,
    FORECAST_HISTORICAL_WEIGHT,
    FORECAST_EXPONENTIAL_WEIGHT,
    FORECAST_MOMENTUM_WEIGHT,
    EXPORT_EXPECTED_RETURN_FORECASTS_PATH,
    FORECAST_EVALUATION_FORWARD_WINDOW,
    EXPORT_FORECAST_EVALUATION_PATH,
    EXPORT_FORECAST_EVALUATION_SUMMARY_PATH,
    EXPORT_REGIME_FORECAST_ANALYSIS_PATH,
    EXPORT_REGIME_FORECAST_SUMMARY_PATH,
    EXPORT_STRATEGY_REGIME_ANALYSIS_PATH,
    EXPORT_BEST_STRATEGY_BY_REGIME_PATH,
    EXPORT_WORST_STRATEGY_BY_REGIME_PATH,
    EXPORT_FORECAST_MODEL_EVALUATION_PATH,
    EXPORT_ADAPTIVE_FORECAST_RECOMMENDATION_PATH,
    EXPORT_REGIME_FORECAST_DASHBOARD_PATH,
    EXPORT_REGIME_STRATEGY_DASHBOARD_PATH,
    EXPORT_RESEARCH_DATABASE_SUMMARY_PATH,
    EXPORT_RESEARCH_DATABASE_METADATA_PATH,
    EXPORT_FULL_RESEARCH_DATABASE_FOLDER,
    EXPORT_RESEARCH_MASTER_DASHBOARD_PATH,
    EXPORT_FINAL_RESEARCH_REPORT_PATH,
    MAX_ACCEPTABLE_DRAWDOWN,
    MAX_ACCEPTABLE_VAR,
    MAX_ACCEPTABLE_CVAR,
    MAX_ACCEPTABLE_POSITION_WEIGHT,
    MIN_ACCEPTABLE_SORTINO_RATIO,
    INITIAL_PORTFOLIO_VALUE,
    PORTFOLIO_VALUE,
    SHOW_PLOT
)

from src.data_loader import load_price_data, load_volume_data
from src.returns import calculate_daily_returns
from src.risk_metrics import calculate_mean_returns, calculate_covariance_matrix

from src.optimizer import (
    generate_random_portfolios,
    find_max_sharpe_portfolio,
    find_min_volatility_portfolio,
    optimize_max_sharpe,
    optimize_min_volatility,
    calculate_efficient_frontier
)

from src.risk_parity import optimize_risk_parity

from src.constraints import (
    create_max_risk_contribution_constraint,
    create_group_max_weight_constraint,
    create_turnover_constraint
)

from src.backtester import run_portfolio_backtest, run_benchmark_backtest
from src.performance import calculate_performance_summary
from src.factor_analysis import calculate_factor_summary
from src.factor_models import calculate_factor_model_summary
from src.attribution import calculate_attribution_summary
from src.risk_contribution import calculate_risk_contribution_summary
from src.diagnostics import create_constraint_diagnostics
from src.trading import calculate_trade_list
from src.transaction_costs import calculate_rebalance_summary
from src.liquidity import create_liquidity_diagnostics
from src.market_impact import create_market_impact_diagnostics
from src.capacity import create_capacity_diagnostics, create_capacity_summary
from src.drawdown import create_drawdown_summary
from src.value_at_risk import create_value_at_risk_summary

from src.stress_testing import (
    create_historical_stress_test,
    create_scenario_analysis,
    create_market_shock_analysis
)

from src.advanced_risk import (
    create_concentration_summary,
    create_tail_risk_summary
)

from src.risk_dashboard import (
    create_risk_dashboard,
    create_risk_governance_report
)

from src.strategy_engine import create_strategy_summary

from src.strategy_comparison import (
    compare_strategies,
    rank_strategies
)

from src.walk_forward import (
    run_walk_forward_test,
    summarize_walk_forward_results
)

from src.out_of_sample import (
    run_out_of_sample_test,
    summarize_out_of_sample_results
)

from src.sensitivity_analysis import (
    run_sensitivity_analysis,
    summarize_sensitivity_analysis
)

from src.robustness import (
    create_robustness_dashboard,
    summarize_robustness_dashboard
)

from src.regime_detection import (
    detect_market_regimes,
    summarize_market_regimes,
    get_latest_market_regime
)

from src.regime_attribution import (
    calculate_regime_attribution,
    identify_best_regime,
    identify_worst_regime
)

from src.forecast_models import create_expected_return_forecasts

from src.forecast_evaluation import (
    calculate_realized_forward_returns,
    evaluate_forecast_accuracy,
    summarize_forecast_evaluation
)

from src.regime_forecast_analysis import (
    align_forecasts_with_regimes,
    summarize_forecast_accuracy_by_regime,
    identify_best_forecast_regime,
    identify_worst_forecast_regime
)

from src.regime_strategy_analysis import (
    compare_strategies_by_regime,
    identify_best_strategy_by_regime,
    identify_worst_strategy_by_regime
)

from src.adaptive_forecast import (
    create_forecast_model_evaluation,
    identify_best_forecast_model,
    identify_worst_forecast_model,
    create_adaptive_forecast_recommendation
)

from src.regime_forecast_dashboard import (
    create_regime_forecast_dashboard,
    create_regime_strategy_dashboard
)

from src.research_database import create_research_database
from src.research_master_dashboard import create_research_master_dashboard
from src.final_research_report import create_final_research_report

from src.research_database_reporting import (
    print_research_database_summary,
    print_research_database_sections,
)

from src.research_database_exporter import (
    export_research_database_summary,
    export_research_database_metadata,
    export_full_research_database,
)

from src.visualizer import (
    plot_efficient_frontier,
    plot_backtest_growth,
    plot_drawdown,
    plot_rolling_metric
)

from src.reporting import (
    print_section_title,
    print_project_settings,
    print_portfolio_results,
    print_backtest_results,
    print_performance_summary,
    print_factor_summary,
    print_factor_model_summary,
    print_return_attribution,
    print_risk_contribution_summary,
    print_constraint_diagnostics,
    print_trade_list,
    print_rebalance_summary,
    print_liquidity_diagnostics,
    print_market_impact_diagnostics,
    print_capacity_diagnostics,
    print_capacity_summary,
    print_drawdown_summary,
    print_value_at_risk_summary,
    print_historical_stress_test,
    print_scenario_analysis,
    print_market_shock_analysis,
    print_concentration_summary,
    print_tail_risk_summary,
    print_risk_dashboard,
    print_risk_governance_report,
    print_strategy_summary,
    print_strategy_comparison,
    print_walk_forward_results,
    print_out_of_sample_results,
    print_sensitivity_analysis,
    print_robustness_dashboard,
    print_market_regime_summary,
    print_latest_market_regime,
    print_regime_attribution,
    print_best_regime,
    print_worst_regime,
    print_expected_return_forecasts,
    print_forecast_evaluation,
    print_forecast_evaluation_summary,
    print_regime_forecast_analysis,
    print_regime_forecast_summary,
    print_best_forecast_regime,
    print_worst_forecast_regime,
    print_strategy_regime_analysis,
    print_best_strategy_by_regime,
    print_worst_strategy_by_regime,
    print_forecast_model_evaluation,
    print_best_forecast_model,
    print_worst_forecast_model,
    print_adaptive_forecast_recommendation,
    print_regime_forecast_dashboard,
    print_regime_strategy_dashboard,
    print_research_master_dashboard,
    print_final_research_report,
    print_completion_message
)

from src.exporter import (
    export_portfolio_results,
    export_backtest_results,
    export_performance_summary,
    export_factor_summary,
    export_factor_model_summary,
    export_return_attribution,
    export_risk_contribution_summary,
    export_constraint_diagnostics,
    export_trade_list,
    export_rebalance_summary,
    export_liquidity_diagnostics,
    export_market_impact_diagnostics,
    export_capacity_diagnostics,
    export_capacity_summary,
    export_drawdown_summary,
    export_value_at_risk_summary,
    export_stress_test_results,
    export_scenario_analysis,
    export_market_shock_analysis,
    export_concentration_summary,
    export_tail_risk_summary,
    export_risk_dashboard,
    export_risk_governance_report,
    export_strategy_summary,
    export_strategy_comparison,
    export_walk_forward_results,
    export_walk_forward_summary,
    export_out_of_sample_results,
    export_out_of_sample_summary,
    export_sensitivity_analysis,
    export_sensitivity_summary,
    export_robustness_dashboard,
    export_robustness_summary,
    export_market_regime_data,
    export_market_regime_summary,
    export_regime_attribution,
    export_expected_return_forecasts,
    export_forecast_evaluation,
    export_forecast_evaluation_summary,
    export_regime_forecast_analysis,
    export_regime_forecast_summary,
    export_strategy_regime_analysis,
    export_best_strategy_by_regime,
    export_worst_strategy_by_regime,
    export_forecast_model_evaluation,
    export_adaptive_forecast_recommendation,
    export_regime_forecast_dashboard,
    export_regime_strategy_dashboard,
    export_research_master_dashboard,
    export_final_research_report
)


def create_sector_constraints(tickers, sector_map, max_sector_weight):
    sector_constraints = []

    unique_sectors = sorted(set(sector_map.values()))

    for sector in unique_sectors:
        sector_indices = [
            index
            for index, ticker in enumerate(tickers)
            if sector_map.get(ticker) == sector
        ]

        if len(sector_indices) > 1:
            sector_constraints.append(
                create_group_max_weight_constraint(
                    asset_indices=sector_indices,
                    max_group_weight=max_sector_weight
                )
            )

    return sector_constraints


def main():
    try:
        print_project_settings(
            tickers=TICKERS,
            start_date=START_DATE,
            end_date=END_DATE,
            risk_free_rate=RISK_FREE_RATE,
            num_portfolios=NUM_PORTFOLIOS,
            min_weight=MIN_WEIGHT,
            max_weight=MAX_WEIGHT
        )

        print_section_title("Loading Price Data")

        prices = load_price_data(
            tickers=TICKERS,
            start_date=START_DATE,
            end_date=END_DATE
        )

        print_section_title("Loading Volume Data")

        volume_data = load_volume_data(
            tickers=TICKERS,
            start_date=START_DATE,
            end_date=END_DATE
        )

        print_section_title("Calculating Returns and Risk Metrics")

        daily_returns = calculate_daily_returns(prices)
        mean_returns = calculate_mean_returns(daily_returns)
        covariance_matrix = calculate_covariance_matrix(daily_returns)

        print_section_title("Creating Institutional Constraints")

        max_risk_contribution_constraints = [
            create_max_risk_contribution_constraint(
                asset_index=index,
                covariance_matrix=covariance_matrix,
                max_risk_contribution=MAX_RISK_CONTRIBUTION
            )
            for index in range(len(TICKERS))
        ]

        sector_constraints = create_sector_constraints(
            tickers=TICKERS,
            sector_map=SECTOR_MAP,
            max_sector_weight=MAX_SECTOR_WEIGHT
        )

        institutional_constraints = max_risk_contribution_constraints + sector_constraints

        current_portfolio_weights = [1 / len(TICKERS)] * len(TICKERS)

        turnover_constraint = create_turnover_constraint(
            current_weights=current_portfolio_weights,
            max_turnover=MAX_TURNOVER
        )

        turnover_constrained_constraints = institutional_constraints + [turnover_constraint]

        print(f"Maximum Risk Contribution Per Asset: {MAX_RISK_CONTRIBUTION:.2%}")
        print(f"Maximum Sector Weight: {MAX_SECTOR_WEIGHT:.2%}")
        print(f"Maximum Portfolio Turnover: {MAX_TURNOVER:.2%}")
        print(f"Maximum Percent of Daily Volume: {MAX_PERCENT_OF_DAILY_VOLUME:.2%}")
        print(f"Market Impact Coefficient: {MARKET_IMPACT_COEFFICIENT:.2%}")

        print_section_title("Running Monte Carlo Simulation")

        portfolio_results = generate_random_portfolios(
            mean_returns,
            covariance_matrix,
            TICKERS,
            num_portfolios=NUM_PORTFOLIOS,
            risk_free_rate=RISK_FREE_RATE,
            min_weight=MIN_WEIGHT,
            max_weight=MAX_WEIGHT
        )

        best_simulated_portfolio = find_max_sharpe_portfolio(
            portfolio_results,
            TICKERS
        )

        lowest_risk_simulated_portfolio = find_min_volatility_portfolio(
            portfolio_results,
            TICKERS
        )

        optimized_max_sharpe_portfolio = optimize_max_sharpe(
            mean_returns,
            covariance_matrix,
            TICKERS,
            risk_free_rate=RISK_FREE_RATE,
            min_weight=MIN_WEIGHT,
            max_weight=MAX_WEIGHT
        )

        constrained_max_sharpe_portfolio = optimize_max_sharpe(
            mean_returns,
            covariance_matrix,
            TICKERS,
            risk_free_rate=RISK_FREE_RATE,
            min_weight=MIN_WEIGHT,
            max_weight=MAX_WEIGHT,
            additional_constraints=institutional_constraints
        )

        turnover_constrained_max_sharpe_portfolio = optimize_max_sharpe(
            mean_returns,
            covariance_matrix,
            TICKERS,
            risk_free_rate=RISK_FREE_RATE,
            min_weight=MIN_WEIGHT,
            max_weight=MAX_WEIGHT,
            additional_constraints=turnover_constrained_constraints
        )

        optimized_min_volatility_portfolio = optimize_min_volatility(
            mean_returns,
            covariance_matrix,
            TICKERS,
            risk_free_rate=RISK_FREE_RATE,
            min_weight=MIN_WEIGHT,
            max_weight=MAX_WEIGHT
        )

        risk_parity_portfolio = optimize_risk_parity(
            mean_returns=mean_returns,
            covariance_matrix=covariance_matrix,
            tickers=TICKERS,
            risk_free_rate=RISK_FREE_RATE,
            min_weight=MIN_WEIGHT,
            max_weight=MAX_WEIGHT
        )

        print_section_title("Creating Strategy Engine Summary")

        strategy_summary = create_strategy_summary(
            tickers=TICKERS,
            optimized_max_sharpe_portfolio=optimized_max_sharpe_portfolio,
            optimized_min_volatility_portfolio=optimized_min_volatility_portfolio,
            risk_parity_portfolio=risk_parity_portfolio,
            constrained_max_sharpe_portfolio=constrained_max_sharpe_portfolio,
            turnover_constrained_max_sharpe_portfolio=turnover_constrained_max_sharpe_portfolio
        )

        print_strategy_summary(
            "Strategy Engine Summary",
            strategy_summary
        )

        efficient_frontier = calculate_efficient_frontier(
            mean_returns,
            covariance_matrix,
            TICKERS,
            num_points=NUM_FRONTIER_POINTS,
            risk_free_rate=RISK_FREE_RATE,
            min_weight=MIN_WEIGHT,
            max_weight=MAX_WEIGHT
        )

        print_portfolio_results(
            "Best Simulated Portfolio by Sharpe Ratio",
            best_simulated_portfolio
        )

        print_portfolio_results(
            "Mathematically Optimized Max Sharpe Portfolio",
            optimized_max_sharpe_portfolio
        )

        print_portfolio_results(
            "Max Sharpe with Institutional Constraints",
            constrained_max_sharpe_portfolio
        )

        print_portfolio_results(
            "Turnover-Constrained Max Sharpe Portfolio",
            turnover_constrained_max_sharpe_portfolio
        )

        print_portfolio_results(
            "Best Simulated Minimum Volatility Portfolio",
            lowest_risk_simulated_portfolio
        )

        print_portfolio_results(
            "Mathematically Optimized Minimum Volatility Portfolio",
            optimized_min_volatility_portfolio
        )

        print_portfolio_results(
            "Risk Parity Portfolio",
            risk_parity_portfolio
        )

        print_section_title("Running Backtest")

        benchmark_prices = load_price_data(
            tickers=[BENCHMARK_TICKER],
            start_date=START_DATE,
            end_date=END_DATE
        )

        portfolio_backtest = run_portfolio_backtest(
            prices=prices,
            weights=optimized_max_sharpe_portfolio["weights"],
            risk_free_rate=RISK_FREE_RATE,
            initial_value=INITIAL_PORTFOLIO_VALUE,
            rolling_window=ROLLING_WINDOW,
            rebalance_frequency=REBALANCE_FREQUENCY,
            transaction_cost_rate=TRANSACTION_COST_RATE
        )

        benchmark_backtest = run_benchmark_backtest(
            benchmark_prices=benchmark_prices,
            risk_free_rate=RISK_FREE_RATE,
            initial_value=INITIAL_PORTFOLIO_VALUE,
            rolling_window=ROLLING_WINDOW
        )

        print_backtest_results(
            "Backtest: Optimized Max Sharpe Portfolio",
            portfolio_backtest
        )

        print_backtest_results(
            f"Backtest: Benchmark ({BENCHMARK_TICKER})",
            benchmark_backtest
        )

        print_section_title("Running Market Regime Detection Engine")

        market_regime_data = detect_market_regimes(
            portfolio_returns=portfolio_backtest["daily_returns"],
            window=REGIME_DETECTION_WINDOW,
            trading_days=REGIME_DETECTION_TRADING_DAYS,
            return_threshold=REGIME_RETURN_THRESHOLD,
            high_volatility_threshold=REGIME_HIGH_VOLATILITY_THRESHOLD,
            severe_drawdown_threshold=REGIME_SEVERE_DRAWDOWN_THRESHOLD
        )

        market_regime_summary = summarize_market_regimes(
            market_regime_data
        )

        latest_market_regime = get_latest_market_regime(
            market_regime_data
        )

        print_market_regime_summary(
            "Market Regime Summary",
            market_regime_summary
        )

        print_latest_market_regime(
            "Latest Market Regime",
            latest_market_regime
        )

        print_section_title("Running Regime Attribution Engine")

        regime_attribution = calculate_regime_attribution(
            regime_data=market_regime_data,
            risk_free_rate=RISK_FREE_RATE
        )

        best_regime = identify_best_regime(
            regime_attribution
        )

        worst_regime = identify_worst_regime(
            regime_attribution
        )

        print_regime_attribution(
            "Regime Attribution Analysis",
            regime_attribution
        )

        print_best_regime(
            "Best Performing Regime",
            best_regime
        )

        print_worst_regime(
            "Worst Performing Regime",
            worst_regime
        )

        print_section_title("Creating Expected Return Forecast Models")

        expected_return_forecasts = create_expected_return_forecasts(
            prices=prices,
            asset_returns=daily_returns,
            trading_days=FORECAST_TRADING_DAYS,
            exponential_span=FORECAST_EXPONENTIAL_SPAN,
            momentum_lookback_window=FORECAST_MOMENTUM_LOOKBACK_WINDOW,
            historical_weight=FORECAST_HISTORICAL_WEIGHT,
            exponential_weight=FORECAST_EXPONENTIAL_WEIGHT,
            momentum_weight=FORECAST_MOMENTUM_WEIGHT
        )

        print_expected_return_forecasts(
            "Expected Return Forecast Models",
            expected_return_forecasts
        )

        print_section_title("Running Forecast Evaluation Engine")

        realized_forward_returns = calculate_realized_forward_returns(
            prices=prices,
            forward_window=FORECAST_EVALUATION_FORWARD_WINDOW
        )

        forecast_evaluation = evaluate_forecast_accuracy(
            forecast_table=expected_return_forecasts,
            realized_forward_returns=realized_forward_returns
        )

        forecast_evaluation_summary = summarize_forecast_evaluation(
            forecast_evaluation
        )

        print_forecast_evaluation(
            "Forecast Evaluation Results",
            forecast_evaluation
        )

        print_forecast_evaluation_summary(
            "Forecast Evaluation Summary",
            forecast_evaluation_summary
        )

        print_section_title("Running Regime-Aware Forecast Analysis")

        regime_forecast_analysis = align_forecasts_with_regimes(
            forecast_table=expected_return_forecasts,
            realized_forward_returns=realized_forward_returns,
            regime_data=market_regime_data
        )

        regime_forecast_summary = summarize_forecast_accuracy_by_regime(
            regime_forecast_analysis
        )

        best_forecast_regime = identify_best_forecast_regime(
            regime_forecast_summary
        )

        worst_forecast_regime = identify_worst_forecast_regime(
            regime_forecast_summary
        )

        print_regime_forecast_analysis(
            "Regime-Aware Forecast Analysis",
            regime_forecast_analysis
        )

        print_regime_forecast_summary(
            "Forecast Accuracy by Market Regime",
            regime_forecast_summary
        )

        print_best_forecast_regime(
            "Best Forecast Regime",
            best_forecast_regime
        )

        print_worst_forecast_regime(
            "Worst Forecast Regime",
            worst_forecast_regime
        )

        print_section_title("Running Adaptive Forecast Research Engine")

        forecast_model_evaluation = create_forecast_model_evaluation(
            forecast_table=expected_return_forecasts,
            realized_forward_returns=realized_forward_returns
        )

        best_forecast_model = identify_best_forecast_model(
            forecast_model_evaluation
        )

        worst_forecast_model = identify_worst_forecast_model(
            forecast_model_evaluation
        )

        adaptive_forecast_recommendation = create_adaptive_forecast_recommendation(
            latest_market_regime=latest_market_regime,
            regime_forecast_summary=regime_forecast_summary,
            forecast_model_evaluation=forecast_model_evaluation
        )

        print_forecast_model_evaluation(
            "Forecast Model Evaluation",
            forecast_model_evaluation
        )

        print_best_forecast_model(
            "Best Forecast Model",
            best_forecast_model
        )

        print_worst_forecast_model(
            "Worst Forecast Model",
            worst_forecast_model
        )

        print_adaptive_forecast_recommendation(
            "Adaptive Forecast Recommendation",
            adaptive_forecast_recommendation
        )

        print_section_title("Creating Strategy Comparison Framework")

        strategy_comparison = compare_strategies(
            prices=prices,
            strategy_summary=strategy_summary,
            tickers=TICKERS,
            benchmark_returns=benchmark_backtest["daily_returns"],
            risk_free_rate=RISK_FREE_RATE,
            initial_value=INITIAL_PORTFOLIO_VALUE,
            rolling_window=ROLLING_WINDOW,
            rebalance_frequency=REBALANCE_FREQUENCY,
            transaction_cost_rate=TRANSACTION_COST_RATE,
            value_at_risk_confidence_levels=VALUE_AT_RISK_CONFIDENCE_LEVELS
        )

        ranked_strategy_comparison = rank_strategies(
            strategy_comparison
        )

        print_strategy_comparison(
            "Strategy Comparison Framework",
            ranked_strategy_comparison
        )

        print_section_title("Running Advanced Regime Research Engine")

        strategy_returns_by_name = {
            "Optimized Max Sharpe Portfolio":
                portfolio_backtest["daily_returns"],
            f"Benchmark ({BENCHMARK_TICKER})":
                benchmark_backtest["daily_returns"]
        }

        strategy_regime_analysis = compare_strategies_by_regime(
            strategy_returns_dict=strategy_returns_by_name,
            regime_data=market_regime_data,
            risk_free_rate=RISK_FREE_RATE
        )

        best_strategy_by_regime = identify_best_strategy_by_regime(
            strategy_regime_analysis
        )

        worst_strategy_by_regime = identify_worst_strategy_by_regime(
            strategy_regime_analysis
        )

        print_strategy_regime_analysis(
            "Strategy Performance by Market Regime",
            strategy_regime_analysis
        )

        print_best_strategy_by_regime(
            "Best Strategy by Market Regime",
            best_strategy_by_regime
        )

        print_worst_strategy_by_regime(
            "Worst Strategy by Market Regime",
            worst_strategy_by_regime
        )

        print_section_title("Creating Regime & Forecast Research Dashboard")

        regime_forecast_dashboard = create_regime_forecast_dashboard(
            latest_market_regime=latest_market_regime,
            best_regime=best_regime,
            worst_regime=worst_regime,
            best_forecast_regime=best_forecast_regime,
            worst_forecast_regime=worst_forecast_regime,
            best_forecast_model=best_forecast_model,
            worst_forecast_model=worst_forecast_model,
            adaptive_forecast_recommendation=adaptive_forecast_recommendation
        )

        regime_strategy_dashboard = create_regime_strategy_dashboard(
            best_strategy_by_regime=best_strategy_by_regime,
            worst_strategy_by_regime=worst_strategy_by_regime
        )

        print_regime_forecast_dashboard(
            "Regime & Forecast Research Dashboard",
            regime_forecast_dashboard
        )

        print_regime_strategy_dashboard(
            "Regime Strategy Dashboard",
            regime_strategy_dashboard
        )

        print_section_title("Running Walk-Forward Testing Engine")

        walk_forward_results = run_walk_forward_test(
            prices=prices,
            tickers=TICKERS,
            risk_free_rate=RISK_FREE_RATE,
            train_window_days=WALK_FORWARD_TRAIN_WINDOW_DAYS,
            test_window_days=WALK_FORWARD_TEST_WINDOW_DAYS,
            min_weight=MIN_WEIGHT,
            max_weight=MAX_WEIGHT,
            initial_value=INITIAL_PORTFOLIO_VALUE,
            rolling_window=ROLLING_WINDOW,
            rebalance_frequency=REBALANCE_FREQUENCY,
            transaction_cost_rate=TRANSACTION_COST_RATE
        )

        walk_forward_summary = summarize_walk_forward_results(
            walk_forward_results
        )

        print_walk_forward_results(
            "Walk-Forward Testing Results",
            walk_forward_results,
            walk_forward_summary
        )

        print_section_title("Running Out-of-Sample Testing Engine")

        out_of_sample_results = run_out_of_sample_test(
            prices=prices,
            tickers=TICKERS,
            risk_free_rate=RISK_FREE_RATE,
            train_fraction=OUT_OF_SAMPLE_TRAIN_FRACTION,
            min_weight=MIN_WEIGHT,
            max_weight=MAX_WEIGHT,
            initial_value=INITIAL_PORTFOLIO_VALUE,
            rolling_window=ROLLING_WINDOW,
            rebalance_frequency=REBALANCE_FREQUENCY,
            transaction_cost_rate=TRANSACTION_COST_RATE
        )

        out_of_sample_summary = summarize_out_of_sample_results(
            out_of_sample_results
        )

        print_out_of_sample_results(
            "Out-of-Sample Testing Results",
            out_of_sample_results,
            out_of_sample_summary
        )

        print_section_title("Running Sensitivity Analysis")

        sensitivity_results = run_sensitivity_analysis(
            prices=prices,
            tickers=TICKERS,
            risk_free_rate_values=SENSITIVITY_RISK_FREE_RATE_VALUES,
            min_weight_values=SENSITIVITY_MIN_WEIGHT_VALUES,
            max_weight_values=SENSITIVITY_MAX_WEIGHT_VALUES,
            initial_value=INITIAL_PORTFOLIO_VALUE,
            rolling_window=ROLLING_WINDOW,
            rebalance_frequency=REBALANCE_FREQUENCY,
            transaction_cost_rate=TRANSACTION_COST_RATE
        )

        sensitivity_summary = summarize_sensitivity_analysis(
            sensitivity_results
        )

        print_sensitivity_analysis(
            "Sensitivity Analysis Results",
            sensitivity_results,
            sensitivity_summary
        )

        print_section_title("Creating Robustness Dashboard")

        robustness_dashboard = create_robustness_dashboard(
            sensitivity_summary=sensitivity_summary,
            walk_forward_summary=walk_forward_summary,
            out_of_sample_summary=out_of_sample_summary,
            minimum_acceptable_sharpe=MINIMUM_ACCEPTABLE_ROBUSTNESS_SHARPE,
            maximum_acceptable_drawdown=MAXIMUM_ACCEPTABLE_ROBUSTNESS_DRAWDOWN
        )

        robustness_summary = summarize_robustness_dashboard(
            robustness_dashboard
        )

        print_robustness_dashboard(
            "Robustness Dashboard",
            robustness_dashboard,
            robustness_summary
        )

        print_section_title(
            "Calculating Institutional Drawdown Risk Analysis"
        )

        drawdown_summary = create_drawdown_summary(
            portfolio_backtest["growth_curve"]
        )

        print_drawdown_summary(
            "Institutional Drawdown Risk Analysis",
            drawdown_summary
        )

        print_section_title(
            "Calculating Value-at-Risk and Conditional Value-at-Risk"
        )

        value_at_risk_summary = create_value_at_risk_summary(
            portfolio_returns=portfolio_backtest["daily_returns"],
            confidence_levels=VALUE_AT_RISK_CONFIDENCE_LEVELS
        )

        print_value_at_risk_summary(
            "Value-at-Risk and Conditional Value-at-Risk Analysis",
            value_at_risk_summary
        )

        print_section_title("Running Historical Stress Testing")

        stress_test_results = create_historical_stress_test(
            portfolio_returns=portfolio_backtest["daily_returns"],
            stress_periods=STRESS_TEST_PERIODS
        )

        print_historical_stress_test(
            "Historical Stress Testing",
            stress_test_results
        )

        print_section_title("Running Scenario Analysis")

        scenario_analysis = create_scenario_analysis(
            weights=optimized_max_sharpe_portfolio["weights"],
            scenarios=SCENARIO_RETURNS
        )

        print_scenario_analysis(
            "Scenario Analysis",
            scenario_analysis
        )

        print_section_title("Running Market Shock Analysis")

        market_shock_analysis = create_market_shock_analysis(
            weights=optimized_max_sharpe_portfolio["weights"],
            shock_levels=MARKET_SHOCK_LEVELS
        )

        print_market_shock_analysis(
            "Market Shock Analysis",
            market_shock_analysis
        )

        print_section_title("Calculating Concentration Risk Analytics")

        concentration_summary = create_concentration_summary(
            optimized_max_sharpe_portfolio["weights"]
        )

        print_concentration_summary(
            "Concentration Risk Analysis",
            concentration_summary
        )

        print_section_title("Calculating Tail Risk Analytics")

        tail_risk_summary = create_tail_risk_summary(
            portfolio_returns=portfolio_backtest["daily_returns"],
            risk_free_rate=RISK_FREE_RATE
        )

        print_tail_risk_summary(
            "Tail Risk Analytics",
            tail_risk_summary
        )

        print_section_title("Creating Institutional Risk Dashboard")

        risk_dashboard = create_risk_dashboard(
            drawdown_summary=drawdown_summary,
            value_at_risk_summary=value_at_risk_summary,
            stress_test_results=stress_test_results,
            concentration_summary=concentration_summary,
            tail_risk_summary=tail_risk_summary
        )

        print_risk_dashboard(
            "Institutional Risk Dashboard",
            risk_dashboard
        )

        print_section_title("Running Risk Governance Checks")

        risk_governance_report = create_risk_governance_report(
            risk_dashboard=risk_dashboard,
            max_acceptable_drawdown=MAX_ACCEPTABLE_DRAWDOWN,
            max_acceptable_var=MAX_ACCEPTABLE_VAR,
            max_acceptable_cvar=MAX_ACCEPTABLE_CVAR,
            max_acceptable_position_weight=MAX_ACCEPTABLE_POSITION_WEIGHT,
            min_acceptable_sortino_ratio=MIN_ACCEPTABLE_SORTINO_RATIO
        )

        print_risk_governance_report(
            "Risk Governance Report",
            risk_governance_report
        )

        print_section_title(
            "Calculating Institutional Performance Analytics"
        )

        performance_summary = calculate_performance_summary(
            portfolio_returns=portfolio_backtest["daily_returns"],
            benchmark_returns=benchmark_backtest["daily_returns"],
            risk_free_rate=RISK_FREE_RATE
        )

        print_performance_summary(
            f"Institutional Performance Analytics vs {BENCHMARK_TICKER}",
            performance_summary
        )

        print_section_title("Calculating Single-Factor Analysis")

        factor_summary = calculate_factor_summary(
            portfolio_returns=portfolio_backtest["daily_returns"],
            benchmark_returns=benchmark_backtest["daily_returns"],
            risk_free_rate=RISK_FREE_RATE
        )

        print_factor_summary(
            f"Single-Factor Market Analysis vs {BENCHMARK_TICKER}",
            factor_summary
        )

        print_section_title("Loading Multi-Factor Proxy Data")

        factor_prices = load_price_data(
            tickers=list(FACTOR_TICKERS.values()),
            start_date=START_DATE,
            end_date=END_DATE
        )

        factor_returns = calculate_daily_returns(factor_prices)
        factor_returns.columns = list(FACTOR_TICKERS.keys())

        print_section_title("Calculating Multi-Factor Model")

        factor_model_summary = calculate_factor_model_summary(
            portfolio_returns=portfolio_backtest["daily_returns"],
            factor_returns=factor_returns
        )

        print_factor_model_summary(
            "ETF Proxy Multi-Factor Model",
            factor_model_summary
        )

        print_section_title("Calculating Return Attribution")

        return_attribution = calculate_attribution_summary(
            weights=optimized_max_sharpe_portfolio["weights"],
            asset_returns=daily_returns
        )

        print_return_attribution(
            "Asset-Level Return Attribution",
            return_attribution
        )

        print_section_title("Calculating Risk Contribution Analysis")

        risk_contribution_summary = calculate_risk_contribution_summary(
            weights=optimized_max_sharpe_portfolio["weights"],
            covariance_matrix=covariance_matrix
        )

        constrained_risk_contribution_summary = (
            calculate_risk_contribution_summary(
                weights=constrained_max_sharpe_portfolio["weights"],
                covariance_matrix=covariance_matrix
            )
        )

        turnover_constrained_risk_contribution_summary = (
            calculate_risk_contribution_summary(
                weights=turnover_constrained_max_sharpe_portfolio["weights"],
                covariance_matrix=covariance_matrix
            )
        )

        risk_parity_contribution_summary = (
            calculate_risk_contribution_summary(
                weights=risk_parity_portfolio["weights"],
                covariance_matrix=covariance_matrix
            )
        )

        print_risk_contribution_summary(
            "Risk Contribution Analysis: Optimized Max Sharpe Portfolio",
            risk_contribution_summary
        )

        print_risk_contribution_summary(
            "Risk Contribution Analysis: "
            "Max Sharpe with Institutional Constraints",
            constrained_risk_contribution_summary
        )

        print_risk_contribution_summary(
            "Risk Contribution Analysis: "
            "Turnover-Constrained Max Sharpe Portfolio",
            turnover_constrained_risk_contribution_summary
        )

        print_risk_contribution_summary(
            "Risk Contribution Analysis: Risk Parity Portfolio",
            risk_parity_contribution_summary
        )

        print_section_title("Running Constraint Diagnostics")

        constrained_constraint_diagnostics = create_constraint_diagnostics(
            portfolio_name="Max Sharpe with Institutional Constraints",
            weights=constrained_max_sharpe_portfolio["weights"],
            tickers=TICKERS,
            covariance_matrix=covariance_matrix,
            sector_map=SECTOR_MAP,
            max_sector_weight=MAX_SECTOR_WEIGHT,
            max_risk_contribution=MAX_RISK_CONTRIBUTION,
            current_weights=current_portfolio_weights,
            max_turnover=MAX_TURNOVER
        )

        turnover_constrained_constraint_diagnostics = (
            create_constraint_diagnostics(
                portfolio_name="Turnover-Constrained Max Sharpe Portfolio",
                weights=turnover_constrained_max_sharpe_portfolio["weights"],
                tickers=TICKERS,
                covariance_matrix=covariance_matrix,
                sector_map=SECTOR_MAP,
                max_sector_weight=MAX_SECTOR_WEIGHT,
                max_risk_contribution=MAX_RISK_CONTRIBUTION,
                current_weights=current_portfolio_weights,
                max_turnover=MAX_TURNOVER
            )
        )

        print_constraint_diagnostics(
            "Constraint Diagnostics: "
            "Max Sharpe with Institutional Constraints",
            constrained_constraint_diagnostics
        )

        print_constraint_diagnostics(
            "Constraint Diagnostics: "
            "Turnover-Constrained Max Sharpe Portfolio",
            turnover_constrained_constraint_diagnostics
        )

        print_section_title(
            "Generating Portfolio Rebalancing Trade List"
        )

        trade_list = calculate_trade_list(
            tickers=TICKERS,
            current_weights=current_portfolio_weights,
            target_weights=turnover_constrained_max_sharpe_portfolio[
                "weights"
            ],
            portfolio_value=PORTFOLIO_VALUE
        )

        print_trade_list(
            "Portfolio Rebalancing Trade List",
            trade_list
        )

        print_section_title(
            "Calculating Transaction Cost and Rebalance Impact"
        )

        rebalance_summary = calculate_rebalance_summary(
            trade_list=trade_list,
            portfolio_value=PORTFOLIO_VALUE,
            transaction_cost_rate=TRANSACTION_COST_RATE
        )

        print_rebalance_summary(
            "Transaction Cost and Rebalance Impact Summary",
            rebalance_summary
        )

        print_section_title(
            "Calculating Liquidity and Capacity Diagnostics"
        )

        liquidity_diagnostics = create_liquidity_diagnostics(
            trade_list=trade_list,
            prices=prices,
            volumes=volume_data,
            max_percent_of_daily_volume=MAX_PERCENT_OF_DAILY_VOLUME
        )

        print_liquidity_diagnostics(
            "Liquidity and Capacity Diagnostics",
            liquidity_diagnostics
        )

        print_section_title("Calculating Market Impact Diagnostics")

        market_impact_diagnostics = create_market_impact_diagnostics(
            liquidity_diagnostics=liquidity_diagnostics,
            market_impact_coefficient=MARKET_IMPACT_COEFFICIENT
        )

        print_market_impact_diagnostics(
            "Market Impact Diagnostics",
            market_impact_diagnostics
        )

        print_section_title("Calculating Portfolio Capacity Analysis")

        capacity_diagnostics = create_capacity_diagnostics(
            liquidity_diagnostics=liquidity_diagnostics,
            max_percent_of_daily_volume=MAX_PERCENT_OF_DAILY_VOLUME
        )

        capacity_summary = create_capacity_summary(
            capacity_diagnostics
        )

        print_capacity_diagnostics(
            "Portfolio Capacity Diagnostics",
            capacity_diagnostics
        )

        print_capacity_summary(
            "Portfolio Capacity Summary",
            capacity_summary
        )

        plot_efficient_frontier(
            portfolio_results,
            best_simulated_portfolio,
            lowest_risk_simulated_portfolio,
            optimized_max_sharpe_portfolio,
            optimized_min_volatility_portfolio,
            efficient_frontier,
            save_path=SAVE_PLOT_PATH,
            show_plot=SHOW_PLOT
        )

        plot_backtest_growth(
            portfolio_growth=portfolio_backtest["growth_curve"],
            benchmark_growth=benchmark_backtest["growth_curve"],
            save_path=SAVE_BACKTEST_PLOT_PATH,
            show_plot=SHOW_PLOT
        )

        plot_drawdown(
            portfolio_drawdown=portfolio_backtest["drawdown"],
            benchmark_drawdown=benchmark_backtest["drawdown"],
            save_path=SAVE_DRAWDOWN_PLOT_PATH,
            show_plot=SHOW_PLOT
        )

        plot_rolling_metric(
            portfolio_metric=portfolio_backtest["rolling_return"],
            benchmark_metric=benchmark_backtest["rolling_return"],
            title="Rolling 1-Year Return",
            ylabel="Return",
            save_path=SAVE_ROLLING_RETURN_PLOT_PATH,
            show_plot=SHOW_PLOT
        )

        plot_rolling_metric(
            portfolio_metric=portfolio_backtest["rolling_volatility"],
            benchmark_metric=benchmark_backtest["rolling_volatility"],
            title="Rolling 1-Year Volatility",
            ylabel="Volatility",
            save_path=SAVE_ROLLING_VOLATILITY_PLOT_PATH,
            show_plot=SHOW_PLOT
        )

        plot_rolling_metric(
            portfolio_metric=portfolio_backtest["rolling_sharpe"],
            benchmark_metric=benchmark_backtest["rolling_sharpe"],
            title="Rolling 1-Year Sharpe Ratio",
            ylabel="Sharpe Ratio",
            save_path=SAVE_ROLLING_SHARPE_PLOT_PATH,
            show_plot=SHOW_PLOT
        )

        portfolios_to_export = {
            "Best Simulated Sharpe": best_simulated_portfolio,
            "Optimized Max Sharpe": optimized_max_sharpe_portfolio,
            "Constrained Max Sharpe": constrained_max_sharpe_portfolio,
            "Turnover-Constrained Max Sharpe":
                turnover_constrained_max_sharpe_portfolio,
            "Best Simulated Min Volatility":
                lowest_risk_simulated_portfolio,
            "Optimized Min Volatility":
                optimized_min_volatility_portfolio,
            "Risk Parity": risk_parity_portfolio
        }

        backtests_to_export = {
            "Optimized Max Sharpe Portfolio": portfolio_backtest,
            f"Benchmark ({BENCHMARK_TICKER})": benchmark_backtest
        }

        constraint_diagnostics_to_export = [
            constrained_constraint_diagnostics,
            turnover_constrained_constraint_diagnostics
        ]

        export_portfolio_results(
            portfolios_to_export,
            EXPORT_RESULTS_PATH
        )

        export_backtest_results(
            backtests_to_export,
            EXPORT_BACKTEST_RESULTS_PATH
        )

        export_performance_summary(
            performance_summary,
            EXPORT_PERFORMANCE_SUMMARY_PATH
        )

        export_factor_summary(
            factor_summary,
            EXPORT_FACTOR_SUMMARY_PATH
        )

        export_factor_model_summary(
            factor_model_summary,
            EXPORT_FACTOR_MODEL_SUMMARY_PATH
        )

        export_return_attribution(
            return_attribution,
            EXPORT_RETURN_ATTRIBUTION_PATH
        )

        export_risk_contribution_summary(
            turnover_constrained_risk_contribution_summary,
            EXPORT_RISK_CONTRIBUTION_PATH
        )

        export_constraint_diagnostics(
            constraint_diagnostics_to_export,
            EXPORT_CONSTRAINT_DIAGNOSTICS_PATH
        )

        export_trade_list(
            trade_list,
            EXPORT_TRADE_LIST_PATH
        )

        export_rebalance_summary(
            rebalance_summary,
            EXPORT_REBALANCE_SUMMARY_PATH
        )

        export_liquidity_diagnostics(
            liquidity_diagnostics,
            EXPORT_LIQUIDITY_DIAGNOSTICS_PATH
        )

        export_market_impact_diagnostics(
            market_impact_diagnostics,
            EXPORT_MARKET_IMPACT_DIAGNOSTICS_PATH
        )

        export_capacity_diagnostics(
            capacity_diagnostics,
            EXPORT_CAPACITY_DIAGNOSTICS_PATH
        )

        export_capacity_summary(
            capacity_summary,
            EXPORT_CAPACITY_SUMMARY_PATH
        )

        export_drawdown_summary(
            drawdown_summary,
            EXPORT_DRAWDOWN_SUMMARY_PATH
        )

        export_value_at_risk_summary(
            value_at_risk_summary,
            EXPORT_VALUE_AT_RISK_SUMMARY_PATH
        )

        export_stress_test_results(
            stress_test_results,
            EXPORT_STRESS_TEST_RESULTS_PATH
        )

        export_scenario_analysis(
            scenario_analysis,
            EXPORT_SCENARIO_ANALYSIS_PATH
        )

        export_market_shock_analysis(
            market_shock_analysis,
            EXPORT_MARKET_SHOCK_ANALYSIS_PATH
        )

        export_concentration_summary(
            concentration_summary,
            EXPORT_CONCENTRATION_SUMMARY_PATH
        )

        export_tail_risk_summary(
            tail_risk_summary,
            EXPORT_TAIL_RISK_SUMMARY_PATH
        )

        export_risk_dashboard(
            risk_dashboard,
            EXPORT_RISK_DASHBOARD_PATH
        )

        export_risk_governance_report(
            risk_governance_report,
            EXPORT_RISK_GOVERNANCE_REPORT_PATH
        )

        export_strategy_summary(
            strategy_summary,
            EXPORT_STRATEGY_SUMMARY_PATH
        )

        export_strategy_comparison(
            ranked_strategy_comparison,
            EXPORT_STRATEGY_COMPARISON_PATH
        )

        export_walk_forward_results(
            walk_forward_results,
            EXPORT_WALK_FORWARD_RESULTS_PATH
        )

        export_walk_forward_summary(
            walk_forward_summary,
            EXPORT_WALK_FORWARD_SUMMARY_PATH
        )

        export_out_of_sample_results(
            out_of_sample_results,
            EXPORT_OUT_OF_SAMPLE_RESULTS_PATH
        )

        export_out_of_sample_summary(
            out_of_sample_summary,
            EXPORT_OUT_OF_SAMPLE_SUMMARY_PATH
        )

        export_sensitivity_analysis(
            sensitivity_results,
            EXPORT_SENSITIVITY_ANALYSIS_PATH
        )

        export_sensitivity_summary(
            sensitivity_summary,
            EXPORT_SENSITIVITY_SUMMARY_PATH
        )

        export_robustness_dashboard(
            robustness_dashboard,
            EXPORT_ROBUSTNESS_DASHBOARD_PATH
        )

        export_robustness_summary(
            robustness_summary,
            EXPORT_ROBUSTNESS_SUMMARY_PATH
        )

        export_market_regime_data(
            market_regime_data,
            EXPORT_MARKET_REGIME_DATA_PATH
        )

        export_market_regime_summary(
            market_regime_summary,
            EXPORT_MARKET_REGIME_SUMMARY_PATH
        )

        export_regime_attribution(
            regime_attribution,
            EXPORT_REGIME_ATTRIBUTION_PATH
        )

        export_expected_return_forecasts(
            expected_return_forecasts,
            EXPORT_EXPECTED_RETURN_FORECASTS_PATH
        )

        export_forecast_evaluation(
            forecast_evaluation,
            EXPORT_FORECAST_EVALUATION_PATH
        )

        export_forecast_evaluation_summary(
            forecast_evaluation_summary,
            EXPORT_FORECAST_EVALUATION_SUMMARY_PATH
        )

        export_regime_forecast_analysis(
            regime_forecast_analysis,
            EXPORT_REGIME_FORECAST_ANALYSIS_PATH
        )

        export_regime_forecast_summary(
            regime_forecast_summary,
            EXPORT_REGIME_FORECAST_SUMMARY_PATH
        )

        export_strategy_regime_analysis(
            strategy_regime_analysis,
            EXPORT_STRATEGY_REGIME_ANALYSIS_PATH
        )

        export_best_strategy_by_regime(
            best_strategy_by_regime,
            EXPORT_BEST_STRATEGY_BY_REGIME_PATH
        )

        export_worst_strategy_by_regime(
            worst_strategy_by_regime,
            EXPORT_WORST_STRATEGY_BY_REGIME_PATH
        )

        export_forecast_model_evaluation(
            forecast_model_evaluation,
            EXPORT_FORECAST_MODEL_EVALUATION_PATH
        )

        export_adaptive_forecast_recommendation(
            adaptive_forecast_recommendation,
            EXPORT_ADAPTIVE_FORECAST_RECOMMENDATION_PATH
        )

        export_regime_forecast_dashboard(
            regime_forecast_dashboard,
            EXPORT_REGIME_FORECAST_DASHBOARD_PATH
        )

        export_regime_strategy_dashboard(
            regime_strategy_dashboard,
            EXPORT_REGIME_STRATEGY_DASHBOARD_PATH
        )

        print_section_title("Creating Portfolio Research Database")

        research_database = create_research_database(
            portfolio_studies={
                "Optimized Max Sharpe Portfolio":
                    optimized_max_sharpe_portfolio,
                "Optimized Minimum Volatility Portfolio":
                    optimized_min_volatility_portfolio,
                "Constrained Max Sharpe Portfolio":
                    constrained_max_sharpe_portfolio,
                "Turnover-Constrained Max Sharpe Portfolio":
                    turnover_constrained_max_sharpe_portfolio,
                "Portfolio Backtest":
                    portfolio_backtest,
                "Benchmark Backtest":
                    benchmark_backtest,
                "Performance Summary":
                    performance_summary,
                "Attribution Summary":
                    return_attribution,
                "Capacity Summary":
                    capacity_summary,
            },
            strategy_studies={
                "Strategy Summary":
                    strategy_summary,
                "Strategy Comparison":
                    strategy_comparison,
                "Strategy Rankings":
                    ranked_strategy_comparison,
                "Walk-Forward Results":
                    walk_forward_results,
                "Out-of-Sample Results":
                    out_of_sample_results,
                "Sensitivity Analysis":
                    sensitivity_results,
                "Robustness Analysis":
                    robustness_summary,
                "Robustness Dashboard":
                    robustness_dashboard,
            },
            regime_studies={
                "Market Regime Summary":
                    market_regime_summary,
                "Latest Market Regime":
                    latest_market_regime,
                "Regime Attribution":
                    regime_attribution,
                "Best Regime":
                    best_regime,
                "Worst Regime":
                    worst_regime,
                "Regime Strategy Analysis":
                    strategy_regime_analysis,
                "Best Strategy By Regime":
                    best_strategy_by_regime,
                "Worst Strategy By Regime":
                    worst_strategy_by_regime,
            },
            forecast_studies={
                "Expected Return Forecasts":
                    expected_return_forecasts,
                "Forecast Evaluation":
                    forecast_evaluation,
                "Regime Forecast Analysis":
                    regime_forecast_analysis,
                "Best Forecast Regime":
                    best_forecast_regime,
                "Worst Forecast Regime":
                    worst_forecast_regime,
                "Adaptive Forecast Comparison":
                    forecast_model_evaluation,
                "Best Forecast Model":
                    best_forecast_model,
                "Worst Forecast Model":
                    worst_forecast_model,
                "Adaptive Forecast Recommendation":
                    adaptive_forecast_recommendation,
            },
            risk_studies={
                "Drawdown Summary":
                    drawdown_summary,
                "Value-at-Risk Summary":
                    value_at_risk_summary,
                "Historical Stress Test":
                    stress_test_results,
                "Scenario Analysis":
                    scenario_analysis,
                "Market Shock Analysis":
                    market_shock_analysis,
                "Concentration Summary":
                    concentration_summary,
                "Tail Risk Summary":
                    tail_risk_summary,
                "Risk Dashboard":
                    risk_dashboard,
                "Risk Governance Report":
                    risk_governance_report,
            },
            dashboard_outputs={
                "Regime Forecast Dashboard":
                    regime_forecast_dashboard,
                "Regime Strategy Dashboard":
                    regime_strategy_dashboard,
            },
        )

        print_research_database_summary(
            "Portfolio Research Database Summary",
            research_database,
        )

        print_research_database_sections(
            research_database
        )

        export_research_database_summary(
            research_database,
            EXPORT_RESEARCH_DATABASE_SUMMARY_PATH,
        )

        export_research_database_metadata(
            research_database,
            EXPORT_RESEARCH_DATABASE_METADATA_PATH,
        )

        export_full_research_database(
            research_database,
            EXPORT_FULL_RESEARCH_DATABASE_FOLDER,
        )

        print_section_title("Creating Research Master Dashboard")

        research_master_dashboard = create_research_master_dashboard(
            research_database=research_database
        )

        print_research_master_dashboard(
            "Research Master Dashboard",
            research_master_dashboard,
        )

        export_research_master_dashboard(
            research_master_dashboard,
            EXPORT_RESEARCH_MASTER_DASHBOARD_PATH,
        )

        print_section_title("Creating Final Institutional Research Report")

        final_research_report = create_final_research_report(
            research_database=research_database,
            research_master_dashboard=research_master_dashboard,
        )

        print_final_research_report(
            "Final Institutional Research Report",
            final_research_report,
        )

        export_final_research_report(
            final_research_report,
            EXPORT_FINAL_RESEARCH_REPORT_PATH,
        )

        print_completion_message(
            save_plot_path=SAVE_PLOT_PATH,
            export_results_path=EXPORT_RESULTS_PATH
        )

        print(f"Backtest chart saved to: {SAVE_BACKTEST_PLOT_PATH}")
        print(f"Drawdown chart saved to: {SAVE_DRAWDOWN_PLOT_PATH}")
        print(f"Rolling return chart saved to: {SAVE_ROLLING_RETURN_PLOT_PATH}")
        print(
            f"Rolling volatility chart saved to: "
            f"{SAVE_ROLLING_VOLATILITY_PLOT_PATH}"
        )
        print(f"Rolling Sharpe chart saved to: {SAVE_ROLLING_SHARPE_PLOT_PATH}")
        print(f"Backtest results saved to: {EXPORT_BACKTEST_RESULTS_PATH}")
        print(f"Performance summary saved to: {EXPORT_PERFORMANCE_SUMMARY_PATH}")
        print(f"Factor summary saved to: {EXPORT_FACTOR_SUMMARY_PATH}")
        print(f"Factor model summary saved to: {EXPORT_FACTOR_MODEL_SUMMARY_PATH}")
        print(f"Return attribution saved to: {EXPORT_RETURN_ATTRIBUTION_PATH}")
        print(f"Risk contribution saved to: {EXPORT_RISK_CONTRIBUTION_PATH}")
        print(
            f"Constraint diagnostics saved to: "
            f"{EXPORT_CONSTRAINT_DIAGNOSTICS_PATH}"
        )
        print(f"Trade list saved to: {EXPORT_TRADE_LIST_PATH}")
        print(f"Rebalance summary saved to: {EXPORT_REBALANCE_SUMMARY_PATH}")
        print(
            f"Liquidity diagnostics saved to: "
            f"{EXPORT_LIQUIDITY_DIAGNOSTICS_PATH}"
        )
        print(
            f"Market impact diagnostics saved to: "
            f"{EXPORT_MARKET_IMPACT_DIAGNOSTICS_PATH}"
        )
        print(
            f"Capacity diagnostics saved to: "
            f"{EXPORT_CAPACITY_DIAGNOSTICS_PATH}"
        )
        print(f"Capacity summary saved to: {EXPORT_CAPACITY_SUMMARY_PATH}")
        print(f"Drawdown summary saved to: {EXPORT_DRAWDOWN_SUMMARY_PATH}")
        print(
            f"Value-at-Risk summary saved to: "
            f"{EXPORT_VALUE_AT_RISK_SUMMARY_PATH}"
        )
        print(
            f"Historical stress test results saved to: "
            f"{EXPORT_STRESS_TEST_RESULTS_PATH}"
        )
        print(f"Scenario analysis saved to: {EXPORT_SCENARIO_ANALYSIS_PATH}")
        print(
            f"Market shock analysis saved to: "
            f"{EXPORT_MARKET_SHOCK_ANALYSIS_PATH}"
        )
        print(
            f"Concentration summary saved to: "
            f"{EXPORT_CONCENTRATION_SUMMARY_PATH}"
        )
        print(
            f"Tail risk summary saved to: "
            f"{EXPORT_TAIL_RISK_SUMMARY_PATH}"
        )
        print(f"Risk dashboard saved to: {EXPORT_RISK_DASHBOARD_PATH}")
        print(
            f"Risk governance report saved to: "
            f"{EXPORT_RISK_GOVERNANCE_REPORT_PATH}"
        )
        print(f"Strategy summary saved to: {EXPORT_STRATEGY_SUMMARY_PATH}")
        print(
            f"Strategy comparison saved to: "
            f"{EXPORT_STRATEGY_COMPARISON_PATH}"
        )
        print(
            f"Walk-forward results saved to: "
            f"{EXPORT_WALK_FORWARD_RESULTS_PATH}"
        )
        print(
            f"Walk-forward summary saved to: "
            f"{EXPORT_WALK_FORWARD_SUMMARY_PATH}"
        )
        print(
            f"Out-of-sample results saved to: "
            f"{EXPORT_OUT_OF_SAMPLE_RESULTS_PATH}"
        )
        print(
            f"Out-of-sample summary saved to: "
            f"{EXPORT_OUT_OF_SAMPLE_SUMMARY_PATH}"
        )
        print(
            f"Sensitivity analysis saved to: "
            f"{EXPORT_SENSITIVITY_ANALYSIS_PATH}"
        )
        print(
            f"Sensitivity summary saved to: "
            f"{EXPORT_SENSITIVITY_SUMMARY_PATH}"
        )
        print(
            f"Robustness dashboard saved to: "
            f"{EXPORT_ROBUSTNESS_DASHBOARD_PATH}"
        )
        print(
            f"Robustness summary saved to: "
            f"{EXPORT_ROBUSTNESS_SUMMARY_PATH}"
        )
        print(
            f"Market regime data saved to: "
            f"{EXPORT_MARKET_REGIME_DATA_PATH}"
        )
        print(
            f"Market regime summary saved to: "
            f"{EXPORT_MARKET_REGIME_SUMMARY_PATH}"
        )
        print(
            f"Regime attribution saved to: "
            f"{EXPORT_REGIME_ATTRIBUTION_PATH}"
        )
        print(
            f"Expected return forecasts saved to: "
            f"{EXPORT_EXPECTED_RETURN_FORECASTS_PATH}"
        )
        print(
            f"Forecast evaluation saved to: "
            f"{EXPORT_FORECAST_EVALUATION_PATH}"
        )
        print(
            f"Forecast evaluation summary saved to: "
            f"{EXPORT_FORECAST_EVALUATION_SUMMARY_PATH}"
        )
        print(
            f"Regime forecast analysis saved to: "
            f"{EXPORT_REGIME_FORECAST_ANALYSIS_PATH}"
        )
        print(
            f"Regime forecast summary saved to: "
            f"{EXPORT_REGIME_FORECAST_SUMMARY_PATH}"
        )
        print(
            f"Strategy regime analysis saved to: "
            f"{EXPORT_STRATEGY_REGIME_ANALYSIS_PATH}"
        )
        print(
            f"Best strategy by regime saved to: "
            f"{EXPORT_BEST_STRATEGY_BY_REGIME_PATH}"
        )
        print(
            f"Worst strategy by regime saved to: "
            f"{EXPORT_WORST_STRATEGY_BY_REGIME_PATH}"
        )
        print(
            f"Forecast model evaluation saved to: "
            f"{EXPORT_FORECAST_MODEL_EVALUATION_PATH}"
        )
        print(
            f"Adaptive forecast recommendation saved to: "
            f"{EXPORT_ADAPTIVE_FORECAST_RECOMMENDATION_PATH}"
        )
        print(
            f"Regime forecast dashboard saved to: "
            f"{EXPORT_REGIME_FORECAST_DASHBOARD_PATH}"
        )
        print(
            f"Regime strategy dashboard saved to: "
            f"{EXPORT_REGIME_STRATEGY_DASHBOARD_PATH}"
        )
        print(
            f"Research database summary saved to: "
            f"{EXPORT_RESEARCH_DATABASE_SUMMARY_PATH}"
        )
        print(
            f"Research database metadata saved to: "
            f"{EXPORT_RESEARCH_DATABASE_METADATA_PATH}"
        )
        print(
            f"Full research database saved to: "
            f"{EXPORT_FULL_RESEARCH_DATABASE_FOLDER}"
        )
        print(
            f"Final research report saved to: "
            f"{EXPORT_FINAL_RESEARCH_REPORT_PATH}"
        )
        print(
            f"Research database summary saved to: "
            f"{EXPORT_RESEARCH_DATABASE_SUMMARY_PATH}"
        )
        print(
            f"Research database metadata saved to: "
            f"{EXPORT_RESEARCH_DATABASE_METADATA_PATH}"
        )
        print(
            f"Full research database saved to folder: "
            f"{EXPORT_FULL_RESEARCH_DATABASE_FOLDER}"
        )
        print(
            f"Research master dashboard saved to: "
            f"{EXPORT_RESEARCH_MASTER_DASHBOARD_PATH}"
        )
        print(
            f"Final research report saved to: "
            f"{EXPORT_FINAL_RESEARCH_REPORT_PATH}"
        )

    except Exception as error:
        print_section_title("Program Error")
        print(f"Something went wrong: {error}")


if __name__ == "__main__":
    main()