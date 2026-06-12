import pandas as pd


def print_section_title(title):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def print_project_settings(
    tickers,
    start_date,
    end_date,
    risk_free_rate,
    num_portfolios,
    min_weight,
    max_weight
):
    print_section_title("Portfolio Optimizer Settings")
    print(f"Tickers: {', '.join(tickers)}")
    print(f"Date Range: {start_date} to {end_date}")
    print(f"Risk-Free Rate: {risk_free_rate:.2%}")
    print(f"Monte Carlo Portfolios: {num_portfolios:,}")
    print(f"Minimum Asset Weight: {min_weight:.2%}")
    print(f"Maximum Asset Weight: {max_weight:.2%}")

def print_dataframe(title, data):
    print_section_title(title)

    if data is None:
        print("No data available.")
        return

    if hasattr(data, "empty") and data.empty:
        print("No data available.")
        return

    print(data.to_string(index=False))


def print_object(title, data):
    print_section_title(title)

    if data is None:
        print("No data available.")
        return

    if isinstance(data, pd.DataFrame):
        if data.empty:
            print("No data available.")
        else:
            print(data.to_string(index=False))
        return

    if isinstance(data, pd.Series):
        if data.empty:
            print("No data available.")
        else:
            print(data.to_string())
        return

    if isinstance(data, dict):
        if not data:
            print("No data available.")
        else:
            for key, value in data.items():
                if isinstance(value, float):
                    print(f"{key}: {value:.4f}")
                else:
                    print(f"{key}: {value}")
        return

    if isinstance(data, list):
        if not data:
            print("No data available.")
        else:
            print(pd.DataFrame(data).to_string(index=False))
        return

    print(data)


def print_portfolio_results(title, portfolio):
    print_section_title(title)

    if portfolio is None:
        print("No portfolio results available.")
        return

    print(f"Expected Annual Return: {portfolio.get('return', 0):.2%}")
    print(f"Annual Volatility: {portfolio.get('volatility', 0):.2%}")
    print(f"Sharpe Ratio: {portfolio.get('sharpe_ratio', 0):.4f}")

    weights = portfolio.get("weights")

    if weights is None:
        return

    print("\nWeights:")

    if isinstance(weights, dict):
        for ticker, weight in weights.items():
            print(f"{ticker}: {weight:.2%}")
    else:
        tickers = portfolio.get("tickers")

        if tickers is not None:
            for ticker, weight in zip(tickers, weights):
                print(f"{ticker}: {weight:.2%}")
        else:
            for index, weight in enumerate(weights):
                print(f"Asset {index + 1}: {weight:.2%}")


def print_backtest_results(title, backtest_results):
    print_section_title(title)

    if backtest_results is None:
        print("No backtest results available.")
        return

    print(f"Total Return: {backtest_results.get('total_return', 0):.2%}")
    print(f"Annualized Return: {backtest_results.get('annualized_return', 0):.2%}")
    print(f"Annualized Volatility: {backtest_results.get('annualized_volatility', 0):.2%}")
    print(f"Sharpe Ratio: {backtest_results.get('sharpe_ratio', 0):.4f}")
    print(f"Maximum Drawdown: {backtest_results.get('max_drawdown', 0):.2%}")

    if "total_transaction_cost" in backtest_results:
        print(f"Total Transaction Cost Drag: {backtest_results['total_transaction_cost']:.2%}")


def print_performance_summary(title, performance_summary):
    print_object(title, performance_summary)


def print_factor_summary(title, factor_summary):
    print_object(title, factor_summary)


def print_factor_model_summary(title, factor_model_summary):
    print_object(title, factor_model_summary)


def print_return_attribution(title, return_attribution):
    print_object(title, return_attribution)


def print_risk_contribution_summary(title, risk_contribution_summary):
    print_object(title, risk_contribution_summary)


def print_constraint_diagnostics(title, diagnostics):
    print_object(title, diagnostics)


def print_trade_list(title, trade_list):
    print_object(title, trade_list)


def print_rebalance_summary(title, rebalance_summary):
    print_object(title, rebalance_summary)


def print_liquidity_diagnostics(title, liquidity_diagnostics):
    print_object(title, liquidity_diagnostics)


def print_market_impact_diagnostics(title, market_impact_diagnostics):
    print_object(title, market_impact_diagnostics)


def print_capacity_diagnostics(title, capacity_diagnostics):
    print_object(title, capacity_diagnostics)


def print_capacity_summary(title, capacity_summary):
    print_object(title, capacity_summary)


def print_drawdown_summary(title, drawdown_summary):
    print_object(title, drawdown_summary)


def print_value_at_risk_summary(title, value_at_risk_summary):
    print_object(title, value_at_risk_summary)


def print_historical_stress_test(title, stress_test_results):
    print_object(title, stress_test_results)


def print_scenario_analysis(title, scenario_analysis):
    print_object(title, scenario_analysis)


def print_market_shock_analysis(title, market_shock_analysis):
    print_object(title, market_shock_analysis)


def print_concentration_summary(title, concentration_summary):
    print_object(title, concentration_summary)


def print_tail_risk_summary(title, tail_risk_summary):
    print_object(title, tail_risk_summary)


def print_risk_dashboard(title, risk_dashboard):
    print_object(title, risk_dashboard)


def print_risk_governance_report(title, risk_governance_report):
    print_object(title, risk_governance_report)


def print_strategy_summary(title, strategy_summary):
    print_object(title, strategy_summary)


def print_strategy_comparison(title, strategy_comparison):
    print_object(title, strategy_comparison)


def print_walk_forward_results(title, walk_forward_results, walk_forward_summary):
    print_section_title(title)

    print("\nWalk-Forward Results:")
    print_object("Walk-Forward Results Table", walk_forward_results)

    print("\nWalk-Forward Summary:")
    print_object("Walk-Forward Summary Table", walk_forward_summary)


def print_out_of_sample_results(title, out_of_sample_results, out_of_sample_summary):
    print_section_title(title)

    print("\nOut-of-Sample Results:")
    print_object("Out-of-Sample Results Table", out_of_sample_results)

    print("\nOut-of-Sample Summary:")
    print_object("Out-of-Sample Summary Table", out_of_sample_summary)


def print_sensitivity_analysis(title, sensitivity_results, sensitivity_summary):
    print_section_title(title)

    print("\nSensitivity Results:")
    print_object("Sensitivity Results Table", sensitivity_results)

    print("\nSensitivity Summary:")
    print_object("Sensitivity Summary Table", sensitivity_summary)


def print_robustness_dashboard(title, robustness_dashboard, robustness_summary):
    print_section_title(title)

    print("\nRobustness Dashboard:")
    print_object("Robustness Dashboard Table", robustness_dashboard)

    print("\nRobustness Summary:")
    print_object("Robustness Summary Table", robustness_summary)


def print_market_regime_summary(title, regime_summary):
    print_object(title, regime_summary)


def print_latest_market_regime(title, latest_regime):
    print_section_title(title)

    if latest_regime is None:
        print("No latest market regime available.")
        return

    print(f"Date: {latest_regime['date']}")
    print(f"Market Regime: {latest_regime['market_regime']}")
    print(f"Daily Return: {latest_regime['daily_return']:.2%}")
    print(f"Cumulative Value: {latest_regime['cumulative_value']:.4f}")
    print(f"Drawdown: {latest_regime['drawdown']:.2%}")
    print(f"Rolling Return: {latest_regime['rolling_return']:.2%}")
    print(f"Rolling Volatility: {latest_regime['rolling_volatility']:.2%}")


def print_completion_message(save_plot_path, export_results_path):
    print_section_title("Program Completed Successfully")

    if save_plot_path is not None:
        print(f"Efficient frontier chart saved to: {save_plot_path}")

    if export_results_path is not None:
        print(f"Portfolio results saved to: {export_results_path}")

def print_regime_attribution(title, regime_attribution):
    print_dataframe(title, regime_attribution)


def print_best_regime(title, best_regime):
    print_section_title(title)

    if best_regime is None:
        print("No best regime available.")
        return

    print(f"Market Regime: {best_regime['market_regime']}")
    print(f"Days: {best_regime['days']}")
    print(f"Average Daily Return: {best_regime['average_daily_return']:.4%}")
    print(f"Total Return: {best_regime['total_return']:.2%}")
    print(f"Annualized Return: {best_regime['annualized_return']:.2%}")
    print(f"Annualized Volatility: {best_regime['annualized_volatility']:.2%}")
    print(f"Sharpe Ratio: {best_regime['sharpe_ratio']:.4f}")
    print(f"Max Drawdown: {best_regime['max_drawdown']:.2%}")


def print_worst_regime(title, worst_regime):
    print_section_title(title)

    if worst_regime is None:
        print("No worst regime available.")
        return

    print(f"Market Regime: {worst_regime['market_regime']}")
    print(f"Days: {worst_regime['days']}")
    print(f"Average Daily Return: {worst_regime['average_daily_return']:.4%}")
    print(f"Total Return: {worst_regime['total_return']:.2%}")
    print(f"Annualized Return: {worst_regime['annualized_return']:.2%}")
    print(f"Annualized Volatility: {worst_regime['annualized_volatility']:.2%}")
    print(f"Sharpe Ratio: {worst_regime['sharpe_ratio']:.4f}")
    print(f"Max Drawdown: {worst_regime['max_drawdown']:.2%}")

def print_expected_return_forecasts(title, forecast_table):
    print_dataframe(title, forecast_table)

def print_forecast_evaluation(title, forecast_evaluation):
    print_dataframe(title, forecast_evaluation)


def print_forecast_evaluation_summary(title, forecast_evaluation_summary):
    print_dataframe(title, forecast_evaluation_summary)

def print_regime_forecast_analysis(title, regime_forecast_analysis):
    print_dataframe(title, regime_forecast_analysis)


def print_regime_forecast_summary(title, regime_forecast_summary):
    print_dataframe(title, regime_forecast_summary)


def print_best_forecast_regime(title, best_forecast_regime):
    print_section_title(title)

    if best_forecast_regime is None:
        print("No best forecast regime available.")
        return

    print(f"Market Regime: {best_forecast_regime['market_regime']}")
    print(f"Observations: {best_forecast_regime['observations']}")
    print(f"Mean Absolute Error: {best_forecast_regime['mean_absolute_error']:.4%}")
    print(f"Root Mean Squared Error: {best_forecast_regime['root_mean_squared_error']:.4%}")
    print(f"Directional Accuracy: {best_forecast_regime['directional_accuracy']:.2%}")


def print_worst_forecast_regime(title, worst_forecast_regime):
    print_section_title(title)

    if worst_forecast_regime is None:
        print("No worst forecast regime available.")
        return

    print(f"Market Regime: {worst_forecast_regime['market_regime']}")
    print(f"Observations: {worst_forecast_regime['observations']}")
    print(f"Mean Absolute Error: {worst_forecast_regime['mean_absolute_error']:.4%}")
    print(f"Root Mean Squared Error: {worst_forecast_regime['root_mean_squared_error']:.4%}")
    print(f"Directional Accuracy: {worst_forecast_regime['directional_accuracy']:.2%}")

def print_strategy_regime_analysis(title, strategy_regime_analysis):
    print_dataframe(title, strategy_regime_analysis)


def print_best_strategy_by_regime(title, best_strategy_by_regime):
    print_dataframe(title, best_strategy_by_regime)


def print_worst_strategy_by_regime(title, worst_strategy_by_regime):
    print_dataframe(title, worst_strategy_by_regime)

def print_forecast_model_evaluation(title, forecast_model_evaluation):
    print_dataframe(title, forecast_model_evaluation)


def print_best_forecast_model(title, best_forecast_model):
    print_section_title(title)

    if best_forecast_model is None:
        print("No best forecast model available.")
        return

    print(f"Forecast Model: {best_forecast_model['forecast_model']}")
    print(f"Observations: {best_forecast_model['observations']}")
    print(f"Mean Absolute Error: {best_forecast_model['mean_absolute_error']:.4%}")
    print(f"Root Mean Squared Error: {best_forecast_model['root_mean_squared_error']:.4%}")
    print(f"Directional Accuracy: {best_forecast_model['directional_accuracy']:.2%}")


def print_worst_forecast_model(title, worst_forecast_model):
    print_section_title(title)

    if worst_forecast_model is None:
        print("No worst forecast model available.")
        return

    print(f"Forecast Model: {worst_forecast_model['forecast_model']}")
    print(f"Observations: {worst_forecast_model['observations']}")
    print(f"Mean Absolute Error: {worst_forecast_model['mean_absolute_error']:.4%}")
    print(f"Root Mean Squared Error: {worst_forecast_model['root_mean_squared_error']:.4%}")
    print(f"Directional Accuracy: {worst_forecast_model['directional_accuracy']:.2%}")


def print_adaptive_forecast_recommendation(title, adaptive_forecast_recommendation):
    print_dataframe(title, adaptive_forecast_recommendation)

def print_regime_forecast_dashboard(title, regime_forecast_dashboard):
    print_dataframe(title, regime_forecast_dashboard)


def print_regime_strategy_dashboard(title, regime_strategy_dashboard):
    print_dataframe(title, regime_strategy_dashboard)

def print_research_master_dashboard(title, dashboard):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)

    if dashboard.empty:
        print("No research master dashboard available.")
    else:
        print(dashboard.to_string(index=False))

def print_final_research_report(title, report):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)

    if report.empty:
        print("No final research report available.")
    else:
        print(report.to_string(index=False))