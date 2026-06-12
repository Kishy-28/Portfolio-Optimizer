import pandas as pd


def calculate_portfolio_scenario_return(
    weights,
    scenario_returns
):
    portfolio_return = 0.0

    for ticker, weight in weights.items():
        portfolio_return += weight * scenario_returns.get(ticker, 0.0)

    return portfolio_return


def create_scenario_analysis(
    weights,
    scenarios
):
    rows = []

    for scenario_name, scenario_returns in scenarios.items():
        portfolio_return = calculate_portfolio_scenario_return(
            weights=weights,
            scenario_returns=scenario_returns
        )

        rows.append(
            {
                "scenario": scenario_name,
                "portfolio_return": portfolio_return
            }
        )

    return pd.DataFrame(rows)


def create_market_shock_analysis(
    weights,
    shock_levels
):
    rows = []

    for shock in shock_levels:
        rows.append(
            {
                "shock_level": shock,
                "portfolio_return": shock
            }
        )

    return pd.DataFrame(rows)


def create_historical_stress_test(
    portfolio_returns,
    stress_periods
):
    rows = []

    for stress_name, dates in stress_periods.items():
        start_date = dates["start_date"]
        end_date = dates["end_date"]

        stress_returns = portfolio_returns.loc[start_date:end_date]

        if stress_returns.empty:
            total_return = None
            worst_day = None
            volatility = None
        else:
            total_return = (1 + stress_returns).prod() - 1
            worst_day = stress_returns.min()
            volatility = stress_returns.std()

        rows.append(
            {
                "stress_period": stress_name,
                "start_date": start_date,
                "end_date": end_date,
                "total_return": total_return,
                "worst_day": worst_day,
                "volatility": volatility
            }
        )

    return pd.DataFrame(rows)