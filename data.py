import os

import pandas as pd


EXPORTS_FOLDER = "exports"

CSV_FILES = {
    "Final Research Report": "final_research_report.csv",
    "Research Master Dashboard": "research_master_dashboard.csv",
    "Portfolio Results": "portfolio_results.csv",
    "Backtest Results": "backtest_results.csv",
    "Performance Summary": "performance_summary.csv",
    "Risk Dashboard": "risk_dashboard.csv",
    "Risk Governance Report": "risk_governance_report.csv",
    "Strategy Summary": "strategy_summary.csv",
    "Strategy Comparison": "strategy_comparison.csv",
    "Robustness Dashboard": "robustness_dashboard.csv",
    "Market Regime Summary": "market_regime_summary.csv",
    "Regime Attribution": "regime_attribution.csv",
    "Expected Return Forecasts": "expected_return_forecasts.csv",
    "Forecast Evaluation": "forecast_evaluation.csv",
    "Regime Forecast Dashboard": "regime_forecast_dashboard.csv",
    "Regime Strategy Dashboard": "regime_strategy_dashboard.csv",
    "Value-at-Risk Summary": "value_at_risk_summary.csv",
    "Stress Test Results": "stress_test_results.csv",
    "Scenario Analysis": "scenario_analysis.csv",
    "Market Shock Analysis": "market_shock_analysis.csv",
    "Concentration Summary": "concentration_summary.csv",
    "Tail Risk Summary": "tail_risk_summary.csv",
}


def load_csv(file_name):
    file_path = os.path.join(EXPORTS_FOLDER, file_name)

    if not os.path.exists(file_path):
        return pd.DataFrame()

    try:
        return pd.read_csv(file_path)
    except Exception:
        return pd.DataFrame()
