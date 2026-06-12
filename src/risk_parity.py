import numpy as np
from scipy.optimize import minimize

from src.optimizer import (
    create_initial_weights,
    create_weight_bounds,
    create_full_investment_constraint,
    calculate_portfolio_performance
)
from src.risk_contribution import calculate_percentage_risk_contribution


def calculate_equal_risk_budget(num_assets):
    return np.array([1 / num_assets] * num_assets)


def calculate_risk_parity_objective(weights, covariance_matrix):
    num_assets = len(weights)
    target_risk_budget = calculate_equal_risk_budget(num_assets)

    percentage_risk_contribution = calculate_percentage_risk_contribution(
        weights=weights,
        covariance_matrix=covariance_matrix
    )

    if percentage_risk_contribution.isnull().any():
        return 1e10

    risk_contribution_difference = (
        percentage_risk_contribution.values - target_risk_budget
    )

    return np.sum(risk_contribution_difference ** 2)


def optimize_risk_parity(
    mean_returns,
    covariance_matrix,
    tickers,
    risk_free_rate=0.02,
    min_weight=0.0,
    max_weight=1.0
):
    num_assets = len(tickers)

    starting_points = [
        create_initial_weights(num_assets),
        np.array([max_weight if i == 0 else (1 - max_weight) / (num_assets - 1) for i in range(num_assets)]),
        np.array([min_weight if i == 0 else (1 - min_weight) / (num_assets - 1) for i in range(num_assets)])
    ]

    best_result = None
    best_objective_value = np.inf

    for starting_weights in starting_points:
        result = minimize(
            calculate_risk_parity_objective,
            starting_weights,
            args=(covariance_matrix,),
            method="SLSQP",
            bounds=create_weight_bounds(num_assets, min_weight, max_weight),
            constraints=(create_full_investment_constraint(),),
            options={
                "maxiter": 1000,
                "ftol": 1e-12,
                "disp": False
            }
        )

        objective_value = calculate_risk_parity_objective(
            result.x,
            covariance_matrix
        )

        if objective_value < best_objective_value:
            best_result = result
            best_objective_value = objective_value

    if best_result is None:
        raise ValueError("Risk parity optimization failed.")

    portfolio_return, portfolio_volatility, sharpe_ratio = calculate_portfolio_performance(
        mean_returns=mean_returns,
        covariance_matrix=covariance_matrix,
        weights=best_result.x,
        risk_free_rate=risk_free_rate
    )

    return {
        "return": portfolio_return,
        "volatility": portfolio_volatility,
        "sharpe_ratio": sharpe_ratio,
        "weights": dict(zip(tickers, best_result.x))
    }