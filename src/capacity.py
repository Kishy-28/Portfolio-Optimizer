import pandas as pd


def calculate_asset_capacity(
    average_daily_dollar_volume,
    max_percent_of_daily_volume
):
    return average_daily_dollar_volume * max_percent_of_daily_volume


def create_capacity_diagnostics(
    liquidity_diagnostics,
    max_percent_of_daily_volume
):
    diagnostics = liquidity_diagnostics.copy()

    diagnostics["asset_capacity"] = calculate_asset_capacity(
        diagnostics["average_daily_dollar_volume"],
        max_percent_of_daily_volume
    )

    diagnostics["capacity_multiple"] = (
        diagnostics["asset_capacity"]
        / diagnostics["absolute_dollar_trade"]
    )

    return diagnostics


def create_capacity_summary(
    capacity_diagnostics
):
    bottleneck_asset = capacity_diagnostics[
        "asset_capacity"
    ].idxmin()

    bottleneck_capacity = capacity_diagnostics.loc[
        bottleneck_asset,
        "asset_capacity"
    ]

    return {
        "bottleneck_asset": bottleneck_asset,
        "strategy_capacity": bottleneck_capacity,
        "average_asset_capacity":
            capacity_diagnostics["asset_capacity"].mean(),
        "maximum_asset_capacity":
            capacity_diagnostics["asset_capacity"].max(),
        "minimum_asset_capacity":
            capacity_diagnostics["asset_capacity"].min()
    }