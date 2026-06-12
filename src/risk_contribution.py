import numpy as np
import pandas as pd


TRADING_DAYS_PER_YEAR = 252


def convert_weights_to_series(weights, tickers):
    if isinstance(weights, dict):
        weight_series = pd.Series(weights)
    else:
        weight_series = pd.Series(weights, index=tickers)

    return weight_series.reindex(tickers).astype(float)


def clean_covariance_matrix(covariance_matrix):
    covariance_matrix = covariance_matrix.copy()
    covariance_matrix = covariance_matrix.astype(float)
    covariance_matrix = covariance_matrix.fillna(0.0)
    return covariance_matrix


def calculate_portfolio_volatility(weights, covariance_matrix):
    covariance_matrix = clean_covariance_matrix(covariance_matrix)

    tickers = covariance_matrix.columns
    weight_series = convert_weights_to_series(weights, tickers)

    annualized_covariance_matrix = covariance_matrix * TRADING_DAYS_PER_YEAR

    portfolio_variance = np.dot(
        weight_series.values.T,
        np.dot(annualized_covariance_matrix.values, weight_series.values)
    )

    if portfolio_variance <= 0:
        return np.nan

    return np.sqrt(portfolio_variance)


def calculate_marginal_risk_contribution(weights, covariance_matrix):
    covariance_matrix = clean_covariance_matrix(covariance_matrix)

    tickers = covariance_matrix.columns
    weight_series = convert_weights_to_series(weights, tickers)

    annualized_covariance_matrix = covariance_matrix * TRADING_DAYS_PER_YEAR

    portfolio_volatility = calculate_portfolio_volatility(
        weights=weight_series,
        covariance_matrix=covariance_matrix
    )

    if pd.isna(portfolio_volatility) or portfolio_volatility == 0:
        return pd.Series(np.nan, index=tickers)

    marginal_risk_contribution = (
        annualized_covariance_matrix.values @ weight_series.values
    ) / portfolio_volatility

    return pd.Series(
        marginal_risk_contribution,
        index=tickers,
        name="marginal_risk_contribution"
    )


def calculate_component_risk_contribution(weights, covariance_matrix):
    covariance_matrix = clean_covariance_matrix(covariance_matrix)

    tickers = covariance_matrix.columns
    weight_series = convert_weights_to_series(weights, tickers)

    marginal_risk_contribution = calculate_marginal_risk_contribution(
        weights=weight_series,
        covariance_matrix=covariance_matrix
    )

    component_risk_contribution = (
        weight_series * marginal_risk_contribution
    )

    return pd.Series(
        component_risk_contribution,
        index=tickers,
        name="component_risk_contribution"
    )


def calculate_percentage_risk_contribution(weights, covariance_matrix):
    component_risk_contribution = calculate_component_risk_contribution(
        weights=weights,
        covariance_matrix=covariance_matrix
    )

    total_risk_contribution = component_risk_contribution.sum()

    if pd.isna(total_risk_contribution) or total_risk_contribution == 0:
        return pd.Series(
            np.nan,
            index=component_risk_contribution.index,
            name="percentage_risk_contribution"
        )

    percentage_risk_contribution = (
        component_risk_contribution / total_risk_contribution
    )

    return pd.Series(
        percentage_risk_contribution,
        index=component_risk_contribution.index,
        name="percentage_risk_contribution"
    )


def calculate_risk_contribution_summary(weights, covariance_matrix):
    covariance_matrix = clean_covariance_matrix(covariance_matrix)

    tickers = covariance_matrix.columns
    weight_series = convert_weights_to_series(weights, tickers)

    marginal_risk_contribution = calculate_marginal_risk_contribution(
        weights=weight_series,
        covariance_matrix=covariance_matrix
    )

    component_risk_contribution = calculate_component_risk_contribution(
        weights=weight_series,
        covariance_matrix=covariance_matrix
    )

    percentage_risk_contribution = calculate_percentage_risk_contribution(
        weights=weight_series,
        covariance_matrix=covariance_matrix
    )

    risk_contribution_summary = pd.DataFrame({
        "weight": weight_series,
        "marginal_risk_contribution": marginal_risk_contribution,
        "component_risk_contribution": component_risk_contribution,
        "percentage_risk_contribution": percentage_risk_contribution
    })

    return risk_contribution_summary.sort_values(
        by="percentage_risk_contribution",
        ascending=False
    )