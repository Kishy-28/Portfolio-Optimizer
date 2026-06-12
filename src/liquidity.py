import numpy as np
import pandas as pd


def align_price_and_volume_data(prices, volumes):
    combined_prices = prices.copy()
    combined_volumes = volumes.copy()

    combined_prices, combined_volumes = combined_prices.align(
        combined_volumes,
        join="inner",
        axis=0
    )

    combined_prices, combined_volumes = combined_prices.align(
        combined_volumes,
        join="inner",
        axis=1
    )

    return combined_prices, combined_volumes


def calculate_average_daily_dollar_volume(prices, volumes):
    prices, volumes = align_price_and_volume_data(
        prices=prices,
        volumes=volumes
    )

    daily_dollar_volume = prices * volumes
    average_daily_dollar_volume = daily_dollar_volume.mean()

    return average_daily_dollar_volume


def calculate_trade_percent_of_daily_volume(
    trade_list,
    average_daily_dollar_volume
):
    diagnostics = trade_list.copy()

    diagnostics["average_daily_dollar_volume"] = average_daily_dollar_volume.reindex(
        diagnostics.index
    )

    diagnostics["absolute_dollar_trade"] = diagnostics["dollar_trade"].abs()

    diagnostics["trade_percent_of_daily_volume"] = np.where(
        diagnostics["average_daily_dollar_volume"] > 0,
        diagnostics["absolute_dollar_trade"] / diagnostics["average_daily_dollar_volume"],
        np.nan
    )

    return diagnostics


def create_liquidity_diagnostics(
    trade_list,
    prices,
    volumes,
    max_percent_of_daily_volume
):
    average_daily_dollar_volume = calculate_average_daily_dollar_volume(
        prices=prices,
        volumes=volumes
    )

    diagnostics = calculate_trade_percent_of_daily_volume(
        trade_list=trade_list,
        average_daily_dollar_volume=average_daily_dollar_volume
    )

    diagnostics["max_percent_of_daily_volume"] = max_percent_of_daily_volume

    diagnostics["passes_liquidity_constraint"] = (
        diagnostics["trade_percent_of_daily_volume"]
        <= diagnostics["max_percent_of_daily_volume"]
    )

    diagnostics["passes_liquidity_constraint"] = diagnostics[
        "passes_liquidity_constraint"
    ].fillna(False)

    return diagnostics


def summarize_liquidity_diagnostics(liquidity_diagnostics):
    return {
        "max_trade_percent_of_daily_volume": liquidity_diagnostics[
            "trade_percent_of_daily_volume"
        ].max(),
        "average_trade_percent_of_daily_volume": liquidity_diagnostics[
            "trade_percent_of_daily_volume"
        ].mean(),
        "number_of_trades_checked": len(liquidity_diagnostics),
        "number_of_liquidity_violations": (
            liquidity_diagnostics["passes_liquidity_constraint"] == False
        ).sum(),
        "passes_all_liquidity_constraints": liquidity_diagnostics[
            "passes_liquidity_constraint"
        ].all()
    }