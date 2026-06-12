TICKERS = ["AAPL", "MSFT", "GOOGL", "AMZN"]

START_DATE = "2020-01-01"
END_DATE = "2024-01-01"

BENCHMARK_TICKER = "SPY"

FACTOR_TICKERS = {
    "market": "SPY",
    "size": "IWM",
    "value": "VLUE",
    "momentum": "MTUM",
    "quality": "QUAL"
}

SECTOR_MAP = {
    "AAPL": "Technology",
    "MSFT": "Technology",
    "GOOGL": "Communication Services",
    "AMZN": "Consumer Discretionary"
}

MAX_SECTOR_WEIGHT = 0.70

RISK_FREE_RATE = 0.02

NUM_PORTFOLIOS = 5000
NUM_FRONTIER_POINTS = 50

MIN_WEIGHT = 0.0
MAX_WEIGHT = 0.60

MAX_RISK_CONTRIBUTION = 0.35
MAX_TURNOVER = 0.50
MAX_PERCENT_OF_DAILY_VOLUME = 0.05

ROLLING_WINDOW = 252
REBALANCE_FREQUENCY = "monthly"

TRANSACTION_COST_RATE = 0.001

SAVE_PLOT_PATH = "efficient_frontier.png"
SAVE_BACKTEST_PLOT_PATH = "backtest_growth.png"
SAVE_DRAWDOWN_PLOT_PATH = "drawdown_chart.png"
SAVE_ROLLING_RETURN_PLOT_PATH = "rolling_return.png"
SAVE_ROLLING_VOLATILITY_PLOT_PATH = "rolling_volatility.png"
SAVE_ROLLING_SHARPE_PLOT_PATH = "rolling_sharpe.png"

EXPORT_RESULTS_PATH = "exports/portfolio_results.csv"
EXPORT_BACKTEST_RESULTS_PATH = "exports/backtest_results.csv"
EXPORT_PERFORMANCE_SUMMARY_PATH = "exports/performance_summary.csv"
EXPORT_FACTOR_SUMMARY_PATH = "exports/factor_summary.csv"
EXPORT_FACTOR_MODEL_SUMMARY_PATH = "exports/factor_model_summary.csv"
EXPORT_RETURN_ATTRIBUTION_PATH = "exports/return_attribution.csv"
EXPORT_RISK_CONTRIBUTION_PATH = "exports/risk_contribution.csv"
EXPORT_CONSTRAINT_DIAGNOSTICS_PATH = "exports/constraint_diagnostics.csv"
EXPORT_TRADE_LIST_PATH = "exports/trade_list.csv"
EXPORT_REBALANCE_SUMMARY_PATH = "exports/rebalance_summary.csv"
EXPORT_LIQUIDITY_DIAGNOSTICS_PATH = "exports/liquidity_diagnostics.csv"

INITIAL_PORTFOLIO_VALUE = 1.0

PORTFOLIO_VALUE = 1000000

SHOW_PLOT = True

MARKET_IMPACT_COEFFICIENT = 0.10
EXPORT_MARKET_IMPACT_DIAGNOSTICS_PATH = "exports/market_impact_diagnostics.csv"

EXPORT_CAPACITY_DIAGNOSTICS_PATH = "exports/capacity_diagnostics.csv"

EXPORT_CAPACITY_SUMMARY_PATH = "exports/capacity_summary.csv"

EXPORT_DRAWDOWN_SUMMARY_PATH = "exports/drawdown_summary.csv"

VALUE_AT_RISK_CONFIDENCE_LEVELS = [0.95, 0.99]

EXPORT_VALUE_AT_RISK_SUMMARY_PATH = "exports/value_at_risk_summary.csv"

STRESS_TEST_PERIODS = {
    "COVID Crash": {
        "start_date": "2020-02-19",
        "end_date": "2020-03-23"
    },
    "2022 Inflation Shock": {
        "start_date": "2022-01-01",
        "end_date": "2022-10-14"
    }
}

SCENARIO_RETURNS = {
    "Technology Selloff": {
        "AAPL": -0.20,
        "MSFT": -0.20,
        "GOOGL": -0.15,
        "AMZN": -0.15
    },
    "Broad Market Crash": {
        "AAPL": -0.30,
        "MSFT": -0.30,
        "GOOGL": -0.30,
        "AMZN": -0.30
    },
    "Mega-Cap Resilience": {
        "AAPL": -0.05,
        "MSFT": -0.03,
        "GOOGL": -0.08,
        "AMZN": -0.10
    }
}

MARKET_SHOCK_LEVELS = [
    -0.05,
    -0.10,
    -0.20,
    -0.30,
    -0.40,
    -0.50
]

EXPORT_STRESS_TEST_RESULTS_PATH = "exports/stress_test_results.csv"
EXPORT_SCENARIO_ANALYSIS_PATH = "exports/scenario_analysis.csv"
EXPORT_MARKET_SHOCK_ANALYSIS_PATH = "exports/market_shock_analysis.csv"

EXPORT_CONCENTRATION_SUMMARY_PATH = "exports/concentration_summary.csv"
EXPORT_TAIL_RISK_SUMMARY_PATH = "exports/tail_risk_summary.csv"

EXPORT_RISK_DASHBOARD_PATH = "exports/risk_dashboard.csv"
EXPORT_RISK_GOVERNANCE_REPORT_PATH = "exports/risk_governance_report.csv"

MAX_ACCEPTABLE_DRAWDOWN = 0.25
MAX_ACCEPTABLE_VAR = 0.05
MAX_ACCEPTABLE_CVAR = 0.08
MAX_ACCEPTABLE_POSITION_WEIGHT = 0.60
MIN_ACCEPTABLE_SORTINO_RATIO = 1.00

EXPORT_STRATEGY_SUMMARY_PATH = "exports/strategy_summary.csv"
EXPORT_STRATEGY_COMPARISON_PATH = "exports/strategy_comparison.csv"

WALK_FORWARD_TRAIN_WINDOW_DAYS = 504
WALK_FORWARD_TEST_WINDOW_DAYS = 252

EXPORT_WALK_FORWARD_RESULTS_PATH = "exports/walk_forward_results.csv"
EXPORT_WALK_FORWARD_SUMMARY_PATH = "exports/walk_forward_summary.csv"

OUT_OF_SAMPLE_TRAIN_FRACTION = 0.70

EXPORT_OUT_OF_SAMPLE_RESULTS_PATH = "exports/out_of_sample_results.csv"
EXPORT_OUT_OF_SAMPLE_SUMMARY_PATH = "exports/out_of_sample_summary.csv"

SENSITIVITY_RISK_FREE_RATE_VALUES = [0.00, 0.02, 0.04]
SENSITIVITY_MIN_WEIGHT_VALUES = [0.00, 0.05]
SENSITIVITY_MAX_WEIGHT_VALUES = [0.40, 0.60]

MINIMUM_ACCEPTABLE_ROBUSTNESS_SHARPE = 0.50
MAXIMUM_ACCEPTABLE_ROBUSTNESS_DRAWDOWN = -0.30

EXPORT_SENSITIVITY_ANALYSIS_PATH = "exports/sensitivity_analysis.csv"
EXPORT_SENSITIVITY_SUMMARY_PATH = "exports/sensitivity_summary.csv"
EXPORT_ROBUSTNESS_DASHBOARD_PATH = "exports/robustness_dashboard.csv"
EXPORT_ROBUSTNESS_SUMMARY_PATH = "exports/robustness_summary.csv"

# ============================================================
# Phase 9.1 — Market Regime Detection Engine
# ============================================================

REGIME_DETECTION_WINDOW = 63
REGIME_DETECTION_TRADING_DAYS = 252

REGIME_RETURN_THRESHOLD = 0.00
REGIME_HIGH_VOLATILITY_THRESHOLD = 0.25
REGIME_SEVERE_DRAWDOWN_THRESHOLD = -0.15

EXPORT_MARKET_REGIME_DATA_PATH = "exports/market_regime_data.csv"
EXPORT_MARKET_REGIME_SUMMARY_PATH = "exports/market_regime_summary.csv"

# ============================================================
# Phase 9.2 — Regime Attribution Engine
# ============================================================

EXPORT_REGIME_ATTRIBUTION_PATH = "exports/regime_attribution.csv"

# ============================================================
# Phase 9.3 — Expected Return Forecast Models
# ============================================================

FORECAST_TRADING_DAYS = 252
FORECAST_EXPONENTIAL_SPAN = 63
FORECAST_MOMENTUM_LOOKBACK_WINDOW = 126

FORECAST_HISTORICAL_WEIGHT = 0.40
FORECAST_EXPONENTIAL_WEIGHT = 0.40
FORECAST_MOMENTUM_WEIGHT = 0.20

EXPORT_EXPECTED_RETURN_FORECASTS_PATH = "exports/expected_return_forecasts.csv"

# ============================================================
# Phase 9.4 — Forecast Evaluation Engine
# ============================================================

FORECAST_EVALUATION_FORWARD_WINDOW = 63

EXPORT_FORECAST_EVALUATION_PATH = "exports/forecast_evaluation.csv"
EXPORT_FORECAST_EVALUATION_SUMMARY_PATH = "exports/forecast_evaluation_summary.csv"

# ============================================================
# Phase 9.5 — Regime-Aware Forecast Analysis
# ============================================================

EXPORT_REGIME_FORECAST_ANALYSIS_PATH = "exports/regime_forecast_analysis.csv"
EXPORT_REGIME_FORECAST_SUMMARY_PATH = "exports/regime_forecast_summary.csv"

# ============================================================
# Phase 9.6 — Advanced Regime Research Engine
# ============================================================

EXPORT_STRATEGY_REGIME_ANALYSIS_PATH = "exports/strategy_regime_analysis.csv"
EXPORT_BEST_STRATEGY_BY_REGIME_PATH = "exports/best_strategy_by_regime.csv"
EXPORT_WORST_STRATEGY_BY_REGIME_PATH = "exports/worst_strategy_by_regime.csv"

# ============================================================
# Phase 9.7 — Adaptive Forecast Research Engine
# ============================================================

EXPORT_FORECAST_MODEL_EVALUATION_PATH = "exports/forecast_model_evaluation.csv"
EXPORT_ADAPTIVE_FORECAST_RECOMMENDATION_PATH = "exports/adaptive_forecast_recommendation.csv"

# ============================================================
# Phase 9.8 — Regime & Forecast Research Dashboard
# ============================================================

EXPORT_REGIME_FORECAST_DASHBOARD_PATH = "exports/regime_forecast_dashboard.csv"
EXPORT_REGIME_STRATEGY_DASHBOARD_PATH = "exports/regime_strategy_dashboard.csv"

EXPORT_RESEARCH_DATABASE_SUMMARY_PATH = "exports/research_database_summary.csv"
EXPORT_RESEARCH_DATABASE_METADATA_PATH = "exports/research_database_metadata.csv"
EXPORT_FULL_RESEARCH_DATABASE_FOLDER = "exports/research_database"

EXPORT_RESEARCH_MASTER_DASHBOARD_PATH = "exports/research_master_dashboard.csv"

EXPORT_FINAL_RESEARCH_REPORT_PATH = "exports/final_research_report.csv"