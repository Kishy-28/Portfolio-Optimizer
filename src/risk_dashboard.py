import pandas as pd


def create_risk_dashboard(
    drawdown_summary,
    value_at_risk_summary,
    stress_test_results,
    concentration_summary,
    tail_risk_summary
):
    dashboard = {
        "max_drawdown": drawdown_summary["max_drawdown"],
        "average_drawdown": drawdown_summary["average_drawdown"],
        "max_drawdown_duration_days": drawdown_summary["max_drawdown_duration_days"],
        "hhi": concentration_summary["hhi"],
        "effective_number_of_positions": concentration_summary["effective_number_of_positions"],
        "max_position_weight": concentration_summary["max_position_weight"],
        "downside_deviation": tail_risk_summary["downside_deviation"],
        "sortino_ratio": tail_risk_summary["sortino_ratio"],
        "tail_ratio": tail_risk_summary["tail_ratio"],
        "tail_volatility": tail_risk_summary["tail_volatility"]
    }

    for _, row in value_at_risk_summary.iterrows():
        confidence_level = int(row["confidence_level"] * 100)

        dashboard[f"historical_var_{confidence_level}"] = row["historical_var"]
        dashboard[f"parametric_var_{confidence_level}"] = row["parametric_var"]
        dashboard[f"historical_cvar_{confidence_level}"] = row["historical_cvar"]
        dashboard[f"parametric_cvar_{confidence_level}"] = row["parametric_cvar"]

    if not stress_test_results.empty:
        dashboard["worst_stress_test_return"] = stress_test_results["total_return"].min()
        dashboard["worst_stress_test_day"] = stress_test_results["worst_day"].min()
    else:
        dashboard["worst_stress_test_return"] = None
        dashboard["worst_stress_test_day"] = None

    return dashboard


def create_risk_governance_report(
    risk_dashboard,
    max_acceptable_drawdown,
    max_acceptable_var,
    max_acceptable_cvar,
    max_acceptable_position_weight,
    min_acceptable_sortino_ratio
):
    checks = []

    checks.append(
        {
            "risk_check": "Maximum Drawdown Limit",
            "metric_value": risk_dashboard["max_drawdown"],
            "limit": max_acceptable_drawdown,
            "passes": abs(risk_dashboard["max_drawdown"]) <= max_acceptable_drawdown
        }
    )

    checks.append(
        {
            "risk_check": "Maximum Position Weight Limit",
            "metric_value": risk_dashboard["max_position_weight"],
            "limit": max_acceptable_position_weight,
            "passes": risk_dashboard["max_position_weight"] <= max_acceptable_position_weight
        }
    )

    checks.append(
        {
            "risk_check": "Minimum Sortino Ratio",
            "metric_value": risk_dashboard["sortino_ratio"],
            "limit": min_acceptable_sortino_ratio,
            "passes": risk_dashboard["sortino_ratio"] >= min_acceptable_sortino_ratio
        }
    )

    for key, value in risk_dashboard.items():
        if key.startswith("historical_var_"):
            checks.append(
                {
                    "risk_check": f"{key} Limit",
                    "metric_value": value,
                    "limit": max_acceptable_var,
                    "passes": abs(value) <= max_acceptable_var
                }
            )

        if key.startswith("historical_cvar_"):
            checks.append(
                {
                    "risk_check": f"{key} Limit",
                    "metric_value": value,
                    "limit": max_acceptable_cvar,
                    "passes": abs(value) <= max_acceptable_cvar
                }
            )

    return pd.DataFrame(checks)