import numpy as np
import pandas as pd


TRADING_DAYS_PER_YEAR = 252


def align_factor_model_data(portfolio_returns, factor_returns):
    combined_data = pd.concat(
        [portfolio_returns, factor_returns],
        axis=1
    ).dropna()

    portfolio_column = combined_data.columns[0]
    factor_columns = combined_data.columns[1:]

    y = combined_data[portfolio_column]
    x = combined_data[factor_columns]

    return y, x


def add_intercept(factor_returns):
    factor_returns_with_intercept = factor_returns.copy()
    factor_returns_with_intercept.insert(0, "intercept", 1.0)

    return factor_returns_with_intercept


def run_factor_regression(portfolio_returns, factor_returns):
    y, x = align_factor_model_data(
        portfolio_returns,
        factor_returns
    )

    x_with_intercept = add_intercept(x)

    coefficients = np.linalg.lstsq(
        x_with_intercept.values,
        y.values,
        rcond=None
    )[0]

    coefficient_series = pd.Series(
        coefficients,
        index=x_with_intercept.columns
    )

    predicted_returns = pd.Series(
        x_with_intercept.values @ coefficients,
        index=y.index,
        name="predicted_return"
    )

    residual_returns = y - predicted_returns

    return {
        "coefficients": coefficient_series,
        "predicted_returns": predicted_returns,
        "residual_returns": residual_returns
    }


def calculate_regression_r_squared(portfolio_returns, factor_returns):
    y, _ = align_factor_model_data(
        portfolio_returns,
        factor_returns
    )

    regression_results = run_factor_regression(
        portfolio_returns,
        factor_returns
    )

    predicted_returns = regression_results["predicted_returns"]

    total_sum_of_squares = ((y - y.mean()) ** 2).sum()
    residual_sum_of_squares = (
        (y - predicted_returns) ** 2
    ).sum()

    if total_sum_of_squares == 0:
        return np.nan

    return 1 - (residual_sum_of_squares / total_sum_of_squares)


def calculate_factor_alpha(portfolio_returns, factor_returns):
    regression_results = run_factor_regression(
        portfolio_returns,
        factor_returns
    )

    daily_alpha = regression_results["coefficients"]["intercept"]

    return daily_alpha * TRADING_DAYS_PER_YEAR


def calculate_factor_exposures(portfolio_returns, factor_returns):
    regression_results = run_factor_regression(
        portfolio_returns,
        factor_returns
    )

    coefficients = regression_results["coefficients"]

    return coefficients.drop("intercept")


def calculate_residual_volatility(portfolio_returns, factor_returns):
    regression_results = run_factor_regression(
        portfolio_returns,
        factor_returns
    )

    residual_returns = regression_results["residual_returns"]

    return residual_returns.std() * np.sqrt(TRADING_DAYS_PER_YEAR)


def calculate_factor_model_summary(portfolio_returns, factor_returns):
    factor_exposures = calculate_factor_exposures(
        portfolio_returns,
        factor_returns
    )

    summary = {
        "factor_alpha": calculate_factor_alpha(
            portfolio_returns,
            factor_returns
        ),
        "r_squared": calculate_regression_r_squared(
            portfolio_returns,
            factor_returns
        ),
        "residual_volatility": calculate_residual_volatility(
            portfolio_returns,
            factor_returns
        )
    }

    for factor_name, exposure in factor_exposures.items():
        summary[f"{factor_name}_exposure"] = exposure

    return summary