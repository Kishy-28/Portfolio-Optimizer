from src.trading import (
    calculate_total_turnover_from_trade_list,
    calculate_buy_value,
    calculate_sell_value
)


def calculate_transaction_cost(
    trade_list,
    portfolio_value,
    transaction_cost_rate
):
    turnover = calculate_total_turnover_from_trade_list(
        trade_list
    )

    return turnover * portfolio_value * transaction_cost_rate


def calculate_net_portfolio_value(
    portfolio_value,
    estimated_transaction_cost
):
    return portfolio_value - estimated_transaction_cost


def calculate_rebalance_summary(
    trade_list,
    portfolio_value,
    transaction_cost_rate
):
    turnover = calculate_total_turnover_from_trade_list(
        trade_list
    )

    buy_value = calculate_buy_value(
        trade_list
    )

    sell_value = calculate_sell_value(
        trade_list
    )

    estimated_transaction_cost = calculate_transaction_cost(
        trade_list,
        portfolio_value,
        transaction_cost_rate
    )

    net_portfolio_value = calculate_net_portfolio_value(
        portfolio_value,
        estimated_transaction_cost
    )

    return {
        "portfolio_value": portfolio_value,
        "turnover": turnover,
        "buy_value": buy_value,
        "sell_value": sell_value,
        "transaction_cost_rate": transaction_cost_rate,
        "estimated_transaction_cost": estimated_transaction_cost,
        "net_portfolio_value": net_portfolio_value
    }
