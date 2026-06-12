import numpy as np
import pandas as pd


def convert_weights_to_series(weights, tickers):
    if isinstance(weights, dict):
        weight_series = pd.Series(weights)
    else:
        weight_series = pd.Series(weights, index=tickers)

    return weight_series.reindex(tickers).fillna(0.0).astype(float)


def classify_trade(weight_change, tolerance=1e-8):
    if weight_change > tolerance:
        return "BUY"

    if weight_change < -tolerance:
        return "SELL"

    return "HOLD"


def calculate_trade_list(
    current_weights,
    target_weights,
    tickers,
    portfolio_value=1.0,
    tolerance=1e-8
):
    current_weight_series = convert_weights_to_series(
        weights=current_weights,
        tickers=tickers
    )

    target_weight_series = convert_weights_to_series(
        weights=target_weights,
        tickers=tickers
    )

    weight_change = target_weight_series - current_weight_series
    dollar_trade = weight_change * portfolio_value

    trade_list = pd.DataFrame({
        "current_weight": current_weight_series,
        "target_weight": target_weight_series,
        "weight_change": weight_change,
        "trade_action": [
            classify_trade(change, tolerance)
            for change in weight_change
        ],
        "dollar_trade": dollar_trade,
        "absolute_weight_change": np.abs(weight_change)
    })

    trade_list.index.name = "ticker"

    return trade_list


def calculate_total_turnover_from_trade_list(trade_list):
    return trade_list["absolute_weight_change"].sum()


def calculate_buy_value(trade_list):
    buy_trades = trade_list[trade_list["trade_action"] == "BUY"]
    return buy_trades["dollar_trade"].sum()


def calculate_sell_value(trade_list):
    sell_trades = trade_list[trade_list["trade_action"] == "SELL"]
    return abs(sell_trades["dollar_trade"].sum())


def calculate_trade_summary(trade_list):
    return {
        "total_turnover": calculate_total_turnover_from_trade_list(trade_list),
        "total_buy_value": calculate_buy_value(trade_list),
        "total_sell_value": calculate_sell_value(trade_list),
        "number_of_buys": (trade_list["trade_action"] == "BUY").sum(),
        "number_of_sells": (trade_list["trade_action"] == "SELL").sum(),
        "number_of_holds": (trade_list["trade_action"] == "HOLD").sum()
    }