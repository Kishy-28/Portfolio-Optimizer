import numpy as np
import pandas as pd
from scipy.optimize import minimize


TRADING_DAYS_PER_YEAR = 252


def validate_weight_constraints(num_assets, min_weight, max_weight):
    if min_weight * num_assets > 1:
        raise ValueError("Minimum weight constraint is too high.")

    if max_weight * num_assets < 1:
        raise ValueError("Maximum weight constraint is too low.")


def generate_random_weights(num_assets, min_weight=0.0, max_weight=1.0):
    validate_weight_constraints(num_assets, min_weight, max_weight)

    while True:
        random_weights = np.random.random(num_assets)
        weights = random_weights / np.sum(random_weights)

        if np.all(weights >= min_weight) and np.all(weights <= max_weight):
            return weights


def create_initial_weights(num_assets):
    return np.array([1 / num_assets] * num_assets)


def create_weight_bounds(num_assets, min_weight=0.0, max_weight=1.0):
    validate_weight_constraints(num_assets, min_weight, max_weight)
    return tuple((min_weight, max_weight) for _ in range(num_assets))


def create_full_investment_constraint():
    return {
        "type": "eq",
        "fun": lambda weights: np.sum(weights) - 1
    }


def combine_constraints(*constraint_groups):
    constraints = []

    for group in constraint_groups:
        if group is None:
            continue

        if isinstance(group, (list, tuple)):
            constraints.extend(group)
        else:
            constraints.append(group)

    return tuple(constraints)


def calculate_portfolio_performance(
    mean_returns,
    covariance_matrix,
    weights,
    risk_free_rate=0.02
):
    portfolio_return = np.sum(mean_returns * weights) * TRADING_DAYS_PER_YEAR

    portfolio_volatility = np.sqrt(
        np.dot(weights.T, np.dot(covariance_matrix * TRADING_DAYS_PER_YEAR, weights))
    )

    sharpe_ratio = (portfolio_return - risk_free_rate) / portfolio_volatility

    return portfolio_return, portfolio_volatility, sharpe_ratio


def create_portfolio_summary(
    tickers,
    weights,
    mean_returns,
    covariance_matrix,
    risk_free_rate=0.02
):
    portfolio_return, portfolio_volatility, sharpe_ratio = calculate_portfolio_performance(
        mean_returns,
        covariance_matrix,
        weights,
        risk_free_rate
    )

    return {
        "return": portfolio_return,
        "volatility": portfolio_volatility,
        "sharpe_ratio": sharpe_ratio,
        "weights": dict(zip(tickers, weights))
    }


def generate_random_portfolios(
    mean_returns,
    covariance_matrix,
    tickers,
    num_portfolios=5000,
    risk_free_rate=0.02,
    min_weight=0.0,
    max_weight=1.0
):
    num_assets = len(mean_returns)
    portfolio_results = []

    for _ in range(num_portfolios):
        weights = generate_random_weights(
            num_assets,
            min_weight=min_weight,
            max_weight=max_weight
        )

        portfolio_summary = create_portfolio_summary(
            tickers,
            weights,
            mean_returns,
            covariance_matrix,
            risk_free_rate
        )

        row = {
            "return": portfolio_summary["return"],
            "volatility": portfolio_summary["volatility"],
            "sharpe_ratio": portfolio_summary["sharpe_ratio"]
        }

        for ticker, weight in portfolio_summary["weights"].items():
            row[ticker] = weight

        portfolio_results.append(row)

    return pd.DataFrame(portfolio_results)


def convert_simulated_row_to_portfolio(row, tickers):
    return {
        "return": row["return"],
        "volatility": row["volatility"],
        "sharpe_ratio": row["sharpe_ratio"],
        "weights": {ticker: row[ticker] for ticker in tickers}
    }


def find_max_sharpe_portfolio(portfolio_results, tickers):
    best_row = portfolio_results.loc[portfolio_results["sharpe_ratio"].idxmax()]
    return convert_simulated_row_to_portfolio(best_row, tickers)


def find_min_volatility_portfolio(portfolio_results, tickers):
    best_row = portfolio_results.loc[portfolio_results["volatility"].idxmin()]
    return convert_simulated_row_to_portfolio(best_row, tickers)


def negative_sharpe_ratio(weights, mean_returns, covariance_matrix, risk_free_rate=0.02):
    _, _, sharpe_ratio = calculate_portfolio_performance(
        mean_returns,
        covariance_matrix,
        weights,
        risk_free_rate
    )

    return -sharpe_ratio


def portfolio_volatility_objective(weights, mean_returns, covariance_matrix):
    _, portfolio_volatility, _ = calculate_portfolio_performance(
        mean_returns,
        covariance_matrix,
        weights
    )

    return portfolio_volatility


def optimize_max_sharpe(
    mean_returns,
    covariance_matrix,
    tickers,
    risk_free_rate=0.02,
    min_weight=0.0,
    max_weight=1.0,
    additional_constraints=None
):
    num_assets = len(mean_returns)

    result = minimize(
        negative_sharpe_ratio,
        create_initial_weights(num_assets),
        args=(mean_returns, covariance_matrix, risk_free_rate),
        method="SLSQP",
        bounds=create_weight_bounds(num_assets, min_weight, max_weight),
        constraints=combine_constraints(
            create_full_investment_constraint(),
            additional_constraints
        )
    )

    if not result.success:
        raise ValueError("Max Sharpe optimization failed.")

    return create_portfolio_summary(
        tickers,
        result.x,
        mean_returns,
        covariance_matrix,
        risk_free_rate
    )


def optimize_min_volatility(
    mean_returns,
    covariance_matrix,
    tickers,
    risk_free_rate=0.02,
    min_weight=0.0,
    max_weight=1.0,
    additional_constraints=None
):
    num_assets = len(mean_returns)

    result = minimize(
        portfolio_volatility_objective,
        create_initial_weights(num_assets),
        args=(mean_returns, covariance_matrix),
        method="SLSQP",
        bounds=create_weight_bounds(num_assets, min_weight, max_weight),
        constraints=combine_constraints(
            create_full_investment_constraint(),
            additional_constraints
        )
    )

    if not result.success:
        raise ValueError("Minimum volatility optimization failed.")

    return create_portfolio_summary(
        tickers,
        result.x,
        mean_returns,
        covariance_matrix,
        risk_free_rate
    )


def portfolio_return_constraint(weights, mean_returns, target_return):
    portfolio_return = np.sum(mean_returns * weights) * TRADING_DAYS_PER_YEAR
    return portfolio_return - target_return


def create_target_return_constraint(mean_returns, target_return):
    return {
        "type": "eq",
        "fun": lambda weights: portfolio_return_constraint(
            weights,
            mean_returns,
            target_return
        )
    }


def optimize_for_target_return(
    mean_returns,
    covariance_matrix,
    target_return,
    min_weight=0.0,
    max_weight=1.0,
    additional_constraints=None
):
    num_assets = len(mean_returns)

    constraints = combine_constraints(
        create_full_investment_constraint(),
        create_target_return_constraint(mean_returns, target_return),
        additional_constraints
    )

    result = minimize(
        portfolio_volatility_objective,
        create_initial_weights(num_assets),
        args=(mean_returns, covariance_matrix),
        method="SLSQP",
        bounds=create_weight_bounds(num_assets, min_weight, max_weight),
        constraints=constraints
    )

    return result


def calculate_efficient_frontier(
    mean_returns,
    covariance_matrix,
    tickers,
    num_points=50,
    risk_free_rate=0.02,
    min_weight=0.0,
    max_weight=1.0,
    additional_constraints=None
):
    min_return = min(mean_returns) * TRADING_DAYS_PER_YEAR
    max_return = max(mean_returns) * TRADING_DAYS_PER_YEAR

    target_returns = np.linspace(min_return, max_return, num_points)

    frontier_results = []

    for target_return in target_returns:
        result = optimize_for_target_return(
            mean_returns,
            covariance_matrix,
            target_return,
            min_weight,
            max_weight,
            additional_constraints
        )

        if result.success:
            portfolio_summary = create_portfolio_summary(
                tickers,
                result.x,
                mean_returns,
                covariance_matrix,
                risk_free_rate
            )

            row = {
                "return": portfolio_summary["return"],
                "volatility": portfolio_summary["volatility"],
                "sharpe_ratio": portfolio_summary["sharpe_ratio"]
            }

            for ticker, weight in portfolio_summary["weights"].items():
                row[ticker] = weight

            frontier_results.append(row)

    return pd.DataFrame(frontier_results)