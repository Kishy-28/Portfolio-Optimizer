import numpy as np
import pandas as pd

from src.risk_contribution import calculate_percentage_risk_contribution


def calculate_portfolio_turnover(current_weights, target_weights):
    current_weights = np.array(current_weights)
    target_weights = np.array(target_weights)

    return np.sum(np.abs(target_weights - current_weights))


def calculate_sector_exposures(weights, tickers, sector_map):
    weight_series = pd.Series(weights, index=tickers)

    sector_exposures = {}

    for ticker, weight in weight_series.items():
        sector = sector_map.get(ticker, "Unclassified")
        sector_exposures[sector] = sector_exposures.get(sector, 0.0) + weight

    return pd.Series(sector_exposures).sort_values(ascending=False)


def check_max_sector_weight(sector_exposures, max_sector_weight):
    return sector_exposures.max() <= max_sector_weight


def check_max_risk_contribution(weights, covariance_matrix, max_risk_contribution):
    percentage_risk_contribution = calculate_percentage_risk_contribution(
        weights=weights,
        covariance_matrix=covariance_matrix
    )

    return percentage_risk_contribution.max() <= max_risk_contribution


def check_turnover_limit(
    current_weights,
    target_weights,
    max_turnover,
    tolerance=1e-8
):
    turnover = calculate_portfolio_turnover(
        current_weights=current_weights,
        target_weights=target_weights
    )

    return turnover <= max_turnover + tolerance


def create_constraint_diagnostics(
    portfolio_name,
    weights,
    tickers,
    covariance_matrix,
    sector_map,
    max_sector_weight,
    max_risk_contribution,
    current_weights,
    max_turnover
):
    weight_values = np.array([weights[ticker] for ticker in tickers])

    sector_exposures = calculate_sector_exposures(
        weights=weight_values,
        tickers=tickers,
        sector_map=sector_map
    )

    percentage_risk_contribution = calculate_percentage_risk_contribution(
        weights=weight_values,
        covariance_matrix=covariance_matrix
    )

    turnover = calculate_portfolio_turnover(
        current_weights=current_weights,
        target_weights=weight_values
    )

    diagnostics = {
        "portfolio": portfolio_name,
        "max_sector_exposure": sector_exposures.max(),
        "max_sector_limit": max_sector_weight,
        "passes_sector_constraint": check_max_sector_weight(
            sector_exposures,
            max_sector_weight
        ),
        "max_risk_contribution": percentage_risk_contribution.max(),
        "max_risk_contribution_limit": max_risk_contribution,
        "passes_risk_contribution_constraint": check_max_risk_contribution(
            weight_values,
            covariance_matrix,
            max_risk_contribution
        ),
        "turnover": turnover,
        "max_turnover_limit": max_turnover,
        "passes_turnover_constraint": check_turnover_limit(
            current_weights,
            weight_values,
            max_turnover
        )
    }

    diagnostics["passes_all_constraints"] = (
        diagnostics["passes_sector_constraint"]
        and diagnostics["passes_risk_contribution_constraint"]
        and diagnostics["passes_turnover_constraint"]
    )

    return diagnostics