import numpy as np


def calculate_market_impact_cost(
    trade_percent_of_daily_volume,
    market_impact_coefficient
):
    return market_impact_coefficient * np.sqrt(
        trade_percent_of_daily_volume
    )


def create_market_impact_diagnostics(
    liquidity_diagnostics,
    market_impact_coefficient
):
    diagnostics = liquidity_diagnostics.copy()

    diagnostics["estimated_market_impact_cost"] = calculate_market_impact_cost(
        diagnostics["trade_percent_of_daily_volume"],
        market_impact_coefficient
    )

    diagnostics["estimated_market_impact_dollars"] = (
        diagnostics["absolute_dollar_trade"]
        * diagnostics["estimated_market_impact_cost"]
    )

    return diagnostics