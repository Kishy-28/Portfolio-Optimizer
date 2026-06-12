import numpy as np

from src.risk_contribution import calculate_percentage_risk_contribution


def create_max_weight_constraint(asset_index, max_weight):
    return {
        "type": "ineq",
        "fun": lambda weights: max_weight - weights[asset_index]
    }


def create_min_weight_constraint(asset_index, min_weight):
    return {
        "type": "ineq",
        "fun": lambda weights: weights[asset_index] - min_weight
    }


def create_group_max_weight_constraint(asset_indices, max_group_weight):
    return {
        "type": "ineq",
        "fun": lambda weights: max_group_weight - np.sum(weights[asset_indices])
    }


def create_group_min_weight_constraint(asset_indices, min_group_weight):
    return {
        "type": "ineq",
        "fun": lambda weights: np.sum(weights[asset_indices]) - min_group_weight
    }


def create_max_risk_contribution_constraint(
    asset_index,
    covariance_matrix,
    max_risk_contribution
):
    return {
        "type": "ineq",
        "fun": lambda weights: (
            max_risk_contribution
            - calculate_percentage_risk_contribution(
                weights=weights,
                covariance_matrix=covariance_matrix
            ).iloc[asset_index]
        )
    }


def create_turnover_constraint(current_weights, max_turnover):
    current_weights = np.array(current_weights)

    return {
        "type": "ineq",
        "fun": lambda target_weights: (
            max_turnover - np.sum(np.abs(target_weights - current_weights))
        )
    }


def create_custom_constraint_list():
    return []