import pandas as pd
from scipy.stats import norm


def calculate_historical_var(
    returns,
    confidence_level
):
    percentile = 1 - confidence_level
    return returns.quantile(percentile)


def calculate_parametric_var(
    returns,
    confidence_level
):
    mean_return = returns.mean()
    volatility = returns.std()
    z_score = norm.ppf(1 - confidence_level)

    return mean_return + (z_score * volatility)


def calculate_historical_cvar(
    returns,
    confidence_level
):
    historical_var = calculate_historical_var(
        returns=returns,
        confidence_level=confidence_level
    )

    tail_losses = returns[returns <= historical_var]

    if tail_losses.empty:
        return historical_var

    return tail_losses.mean()


def calculate_parametric_cvar(
    returns,
    confidence_level
):
    mean_return = returns.mean()
    volatility = returns.std()
    z_score = norm.ppf(1 - confidence_level)

    return mean_return - (
        volatility
        * norm.pdf(z_score)
        / (1 - confidence_level)
    )


def create_value_at_risk_summary(
    portfolio_returns,
    confidence_levels
):
    rows = []

    for confidence_level in confidence_levels:
        historical_var = calculate_historical_var(
            returns=portfolio_returns,
            confidence_level=confidence_level
        )

        parametric_var = calculate_parametric_var(
            returns=portfolio_returns,
            confidence_level=confidence_level
        )

        historical_cvar = calculate_historical_cvar(
            returns=portfolio_returns,
            confidence_level=confidence_level
        )

        parametric_cvar = calculate_parametric_cvar(
            returns=portfolio_returns,
            confidence_level=confidence_level
        )

        rows.append(
            {
                "confidence_level": confidence_level,
                "historical_var": historical_var,
                "parametric_var": parametric_var,
                "historical_cvar": historical_cvar,
                "parametric_cvar": parametric_cvar
            }
        )

    return pd.DataFrame(rows)