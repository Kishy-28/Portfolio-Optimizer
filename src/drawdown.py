import pandas as pd


def calculate_drawdown_series(portfolio_values):
    """
    Calculate the drawdown series from a portfolio value series.

    Drawdown measures the percentage decline from the previous peak.
    """
    running_peak = portfolio_values.cummax()
    drawdown = (portfolio_values / running_peak) - 1
    return drawdown


def calculate_max_drawdown(drawdown_series):
    """
    Calculate the maximum drawdown.
    """
    return drawdown_series.min()


def calculate_average_drawdown(drawdown_series):
    """
    Calculate the average drawdown during periods when drawdown is negative.
    """
    negative_drawdowns = drawdown_series[drawdown_series < 0]

    if negative_drawdowns.empty:
        return 0.0

    return negative_drawdowns.mean()


def calculate_drawdown_duration(drawdown_series):
    """
    Calculate the longest drawdown duration in trading days.
    """
    max_duration = 0
    current_duration = 0

    for drawdown in drawdown_series:
        if drawdown < 0:
            current_duration += 1
            max_duration = max(max_duration, current_duration)
        else:
            current_duration = 0

    return max_duration


def create_drawdown_summary(portfolio_values):
    """
    Create a drawdown risk summary for a portfolio.
    """
    drawdown_series = calculate_drawdown_series(portfolio_values)

    max_drawdown = calculate_max_drawdown(drawdown_series)
    average_drawdown = calculate_average_drawdown(drawdown_series)
    max_drawdown_duration = calculate_drawdown_duration(drawdown_series)

    summary = {
        "max_drawdown": max_drawdown,
        "average_drawdown": average_drawdown,
        "max_drawdown_duration_days": max_drawdown_duration
    }

    return summary