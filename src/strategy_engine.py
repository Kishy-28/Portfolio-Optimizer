import pandas as pd


def create_strategy_record(
    strategy_name,
    strategy_type,
    weights,
    tickers,
    description=""
):
    strategy_record = {
        "strategy_name": strategy_name,
        "strategy_type": strategy_type,
        "description": description
    }

    if isinstance(weights, dict):
        for ticker in tickers:
            strategy_record[ticker] = float(weights[ticker])
    else:
        for ticker, weight in zip(tickers, weights):
            strategy_record[ticker] = float(weight)

    return strategy_record


def create_equal_weight_strategy(tickers):
    equal_weight = 1 / len(tickers)
    return [equal_weight] * len(tickers)


def create_strategy_summary(
    tickers,
    optimized_max_sharpe_portfolio,
    optimized_min_volatility_portfolio,
    risk_parity_portfolio,
    constrained_max_sharpe_portfolio,
    turnover_constrained_max_sharpe_portfolio
):
    strategies = []

    strategies.append(
        create_strategy_record(
            strategy_name="Optimized Max Sharpe",
            strategy_type="Optimization",
            weights=optimized_max_sharpe_portfolio["weights"],
            tickers=tickers,
            description="Portfolio optimized to maximize Sharpe ratio."
        )
    )

    strategies.append(
        create_strategy_record(
            strategy_name="Optimized Minimum Volatility",
            strategy_type="Optimization",
            weights=optimized_min_volatility_portfolio["weights"],
            tickers=tickers,
            description="Portfolio optimized to minimize volatility."
        )
    )

    strategies.append(
        create_strategy_record(
            strategy_name="Risk Parity",
            strategy_type="Risk-Based",
            weights=risk_parity_portfolio["weights"],
            tickers=tickers,
            description="Portfolio designed to balance risk contribution."
        )
    )

    strategies.append(
        create_strategy_record(
            strategy_name="Constrained Max Sharpe",
            strategy_type="Institutional Constraint",
            weights=constrained_max_sharpe_portfolio["weights"],
            tickers=tickers,
            description="Max Sharpe portfolio with institutional constraints."
        )
    )

    strategies.append(
        create_strategy_record(
            strategy_name="Turnover-Constrained Max Sharpe",
            strategy_type="Implementation-Aware",
            weights=turnover_constrained_max_sharpe_portfolio["weights"],
            tickers=tickers,
            description="Max Sharpe portfolio with turnover constraints."
        )
    )

    strategies.append(
        create_strategy_record(
            strategy_name="Equal Weight",
            strategy_type="Baseline",
            weights=create_equal_weight_strategy(tickers),
            tickers=tickers,
            description="Naive equally weighted benchmark portfolio."
        )
    )

    return pd.DataFrame(strategies)


def get_strategy_weights(strategy_summary, strategy_name, tickers):
    selected_strategy = strategy_summary[
        strategy_summary["strategy_name"] == strategy_name
    ]

    if selected_strategy.empty:
        raise ValueError(f"Strategy not found: {strategy_name}")

    return selected_strategy[tickers].iloc[0].values.tolist()