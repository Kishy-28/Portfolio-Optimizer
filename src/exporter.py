import os
import pandas as pd


def ensure_directory_exists(file_path):
    directory = os.path.dirname(file_path)

    if directory:
        os.makedirs(directory, exist_ok=True)


def export_portfolio_results(portfolios, file_path):
    ensure_directory_exists(file_path)

    rows = []

    for portfolio_name, portfolio in portfolios.items():
        row = {
            "portfolio": portfolio_name,
            "return": portfolio["return"],
            "volatility": portfolio["volatility"],
            "sharpe_ratio": portfolio["sharpe_ratio"]
        }

        for ticker, weight in portfolio["weights"].items():
            row[ticker] = weight

        rows.append(row)

    pd.DataFrame(rows).to_csv(file_path, index=False)


def export_backtest_results(backtests, file_path):
    ensure_directory_exists(file_path)

    rows = []

    for name, results in backtests.items():
        row = {
            "strategy": name,
            "total_return": results["total_return"],
            "annualized_return": results["annualized_return"],
            "annualized_volatility": results["annualized_volatility"],
            "sharpe_ratio": results["sharpe_ratio"],
            "max_drawdown": results["max_drawdown"]
        }

        row["total_transaction_cost"] = results.get(
            "total_transaction_cost",
            0.0
        )

        rows.append(row)

    pd.DataFrame(rows).to_csv(file_path, index=False)


def export_performance_summary(performance_summary, file_path):
    ensure_directory_exists(file_path)
    pd.DataFrame([performance_summary]).to_csv(file_path, index=False)


def export_factor_summary(factor_summary, file_path):
    ensure_directory_exists(file_path)
    pd.DataFrame([factor_summary]).to_csv(file_path, index=False)


def export_factor_model_summary(factor_model_summary, file_path):
    ensure_directory_exists(file_path)
    pd.DataFrame([factor_model_summary]).to_csv(file_path, index=False)


def export_return_attribution(attribution, file_path):
    ensure_directory_exists(file_path)
    attribution.to_csv(file_path, index=True)


def export_risk_contribution_summary(
    risk_contribution_summary,
    file_path
):
    ensure_directory_exists(file_path)
    risk_contribution_summary.to_csv(file_path, index=True)


def export_constraint_diagnostics(
    constraint_diagnostics,
    file_path
):
    ensure_directory_exists(file_path)
    pd.DataFrame(constraint_diagnostics).to_csv(
        file_path,
        index=False
    )


def export_trade_list(trade_list, file_path):
    ensure_directory_exists(file_path)
    trade_list.to_csv(file_path, index=True)


def export_rebalance_summary(
    rebalance_summary,
    file_path
):
    ensure_directory_exists(file_path)
    pd.DataFrame([rebalance_summary]).to_csv(
        file_path,
        index=False
    )


def export_liquidity_diagnostics(
    liquidity_diagnostics,
    file_path
):
    ensure_directory_exists(file_path)
    liquidity_diagnostics.to_csv(file_path, index=True)


def export_market_impact_diagnostics(
    market_impact_diagnostics,
    file_path
):
    ensure_directory_exists(file_path)
    market_impact_diagnostics.to_csv(file_path, index=True)


def export_capacity_diagnostics(
    capacity_diagnostics,
    file_path
):
    ensure_directory_exists(file_path)
    capacity_diagnostics.to_csv(file_path, index=True)


def export_capacity_summary(
    capacity_summary,
    file_path
):
    ensure_directory_exists(file_path)
    pd.DataFrame([capacity_summary]).to_csv(
        file_path,
        index=False
    )


def export_drawdown_summary(
    drawdown_summary,
    file_path
):
    ensure_directory_exists(file_path)
    pd.DataFrame([drawdown_summary]).to_csv(
        file_path,
        index=False
    )


def export_value_at_risk_summary(
    value_at_risk_summary,
    file_path
):
    ensure_directory_exists(file_path)
    value_at_risk_summary.to_csv(
        file_path,
        index=False
    )


def export_stress_test_results(
    stress_test_results,
    file_path
):
    ensure_directory_exists(file_path)
    stress_test_results.to_csv(
        file_path,
        index=False
    )


def export_scenario_analysis(
    scenario_analysis,
    file_path
):
    ensure_directory_exists(file_path)
    scenario_analysis.to_csv(
        file_path,
        index=False
    )


def export_market_shock_analysis(
    market_shock_analysis,
    file_path
):
    ensure_directory_exists(file_path)
    market_shock_analysis.to_csv(
        file_path,
        index=False
    )


def export_concentration_summary(
    concentration_summary,
    file_path
):
    ensure_directory_exists(file_path)
    pd.DataFrame([concentration_summary]).to_csv(
        file_path,
        index=False
    )


def export_tail_risk_summary(
    tail_risk_summary,
    file_path
):
    ensure_directory_exists(file_path)
    pd.DataFrame([tail_risk_summary]).to_csv(
        file_path,
        index=False
    )


def export_risk_dashboard(
    risk_dashboard,
    file_path
):
    ensure_directory_exists(file_path)
    pd.DataFrame([risk_dashboard]).to_csv(
        file_path,
        index=False
    )


def export_risk_governance_report(
    risk_governance_report,
    file_path
):
    ensure_directory_exists(file_path)
    risk_governance_report.to_csv(
        file_path,
        index=False
    )


def export_strategy_summary(
    strategy_summary,
    export_path
):
    ensure_directory_exists(export_path)
    strategy_summary.to_csv(export_path, index=False)


def export_strategy_comparison(
    strategy_comparison,
    export_path
):
    ensure_directory_exists(export_path)
    strategy_comparison.to_csv(export_path, index=False)


def export_walk_forward_results(
    walk_forward_results,
    export_path
):
    ensure_directory_exists(export_path)
    walk_forward_results.to_csv(export_path, index=False)


def export_walk_forward_summary(
    walk_forward_summary,
    export_path
):
    ensure_directory_exists(export_path)
    pd.DataFrame([walk_forward_summary]).to_csv(
        export_path,
        index=False
    )


def export_out_of_sample_results(
    out_of_sample_results,
    export_path
):
    ensure_directory_exists(export_path)
    out_of_sample_results.to_csv(
        export_path,
        index=False
    )


def export_out_of_sample_summary(
    out_of_sample_summary,
    export_path
):
    ensure_directory_exists(export_path)
    pd.DataFrame([out_of_sample_summary]).to_csv(
        export_path,
        index=False
    )


def export_sensitivity_analysis(
    sensitivity_results,
    export_path
):
    ensure_directory_exists(export_path)
    sensitivity_results.to_csv(
        export_path,
        index=False
    )


def export_sensitivity_summary(
    sensitivity_summary,
    export_path
):
    ensure_directory_exists(export_path)
    pd.DataFrame([sensitivity_summary]).to_csv(
        export_path,
        index=False
    )


def export_robustness_dashboard(
    robustness_dashboard,
    export_path
):
    ensure_directory_exists(export_path)
    robustness_dashboard.to_csv(
        export_path,
        index=False
    )


def export_robustness_summary(
    robustness_summary,
    export_path
):
    ensure_directory_exists(export_path)
    pd.DataFrame([robustness_summary]).to_csv(
        export_path,
        index=False
    )


def export_market_regime_data(
    regime_data,
    file_path
):
    ensure_directory_exists(file_path)
    regime_data.to_csv(file_path)


def export_market_regime_summary(
    regime_summary,
    file_path
):
    ensure_directory_exists(file_path)
    regime_summary.to_csv(
        file_path,
        index=False
    )

def export_regime_attribution(regime_attribution, file_path):
    regime_attribution.to_csv(file_path, index=False)

def export_expected_return_forecasts(forecast_table, file_path):
    forecast_table.to_csv(file_path, index=False)

def export_forecast_evaluation(forecast_evaluation, file_path):
    forecast_evaluation.to_csv(file_path, index=False)


def export_forecast_evaluation_summary(forecast_evaluation_summary, file_path):
    forecast_evaluation_summary.to_csv(file_path, index=False)

def export_regime_forecast_analysis(regime_forecast_analysis, file_path):
    regime_forecast_analysis.to_csv(file_path, index=False)


def export_regime_forecast_summary(regime_forecast_summary, file_path):
    regime_forecast_summary.to_csv(file_path, index=False)

def export_strategy_regime_analysis(strategy_regime_analysis, file_path):
    strategy_regime_analysis.to_csv(file_path, index=False)


def export_best_strategy_by_regime(best_strategy_by_regime, file_path):
    best_strategy_by_regime.to_csv(file_path, index=False)


def export_worst_strategy_by_regime(worst_strategy_by_regime, file_path):
    worst_strategy_by_regime.to_csv(file_path, index=False)

def export_forecast_model_evaluation(forecast_model_evaluation, file_path):
    forecast_model_evaluation.to_csv(file_path, index=False)


def export_adaptive_forecast_recommendation(adaptive_forecast_recommendation, file_path):
    adaptive_forecast_recommendation.to_csv(file_path, index=False)

def export_regime_forecast_dashboard(regime_forecast_dashboard, file_path):
    regime_forecast_dashboard.to_csv(file_path, index=False)


def export_regime_strategy_dashboard(regime_strategy_dashboard, file_path):
    regime_strategy_dashboard.to_csv(file_path, index=False)

def export_research_master_dashboard(dashboard, export_path):
    dashboard.to_csv(export_path, index=False)

def export_final_research_report(report, export_path):
    report.to_csv(export_path, index=False)