import pandas as pd


TRADING_DAYS_PER_YEAR = 252


def calculate_contribution_to_return(weights, asset_returns):
    weight_series = pd.Series(weights).reindex(asset_returns.columns)

    contribution_to_return = (
        asset_returns.mean()
        * TRADING_DAYS_PER_YEAR
        * weight_series
    )

    return contribution_to_return


def calculate_return_attribution(weights, asset_returns):
    contributions = calculate_contribution_to_return(
        weights=weights,
        asset_returns=asset_returns
    )

    total_contribution = contributions.sum()

    if total_contribution == 0:
        percentage_of_total = contributions * 0
    else:
        percentage_of_total = contributions / total_contribution

    attribution = pd.DataFrame({
        "contribution_to_return": contributions,
        "percentage_of_total_return": percentage_of_total
    })

    return attribution.sort_values(
        by="contribution_to_return",
        ascending=False
    )


def calculate_attribution_summary(weights, asset_returns):
    return calculate_return_attribution(
        weights=weights,
        asset_returns=asset_returns
    )