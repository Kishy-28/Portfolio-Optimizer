import pandas as pd


def create_robustness_dashboard(
    sensitivity_summary,
    walk_forward_summary,
    out_of_sample_summary,
    minimum_acceptable_sharpe=0.50,
    maximum_acceptable_drawdown=-0.30
):
    robustness_checks = []

    average_sensitivity_sharpe = sensitivity_summary["average_sharpe_ratio"]
    minimum_sensitivity_sharpe = sensitivity_summary["minimum_sharpe_ratio"]
    average_walk_forward_sharpe = walk_forward_summary["average_test_sharpe"]
    out_of_sample_sharpe = out_of_sample_summary["test_sharpe_ratio"]

    average_sensitivity_drawdown = sensitivity_summary["average_max_drawdown"]
    average_walk_forward_drawdown = walk_forward_summary["average_test_drawdown"]
    out_of_sample_drawdown = out_of_sample_summary["test_max_drawdown"]

    robustness_checks.append(
        {
            "robustness_check": "Average Sensitivity Sharpe",
            "metric_value": average_sensitivity_sharpe,
            "limit": minimum_acceptable_sharpe,
            "passes": average_sensitivity_sharpe >= minimum_acceptable_sharpe
        }
    )

    robustness_checks.append(
        {
            "robustness_check": "Minimum Sensitivity Sharpe",
            "metric_value": minimum_sensitivity_sharpe,
            "limit": minimum_acceptable_sharpe,
            "passes": minimum_sensitivity_sharpe >= minimum_acceptable_sharpe
        }
    )

    robustness_checks.append(
        {
            "robustness_check": "Average Walk-Forward Sharpe",
            "metric_value": average_walk_forward_sharpe,
            "limit": minimum_acceptable_sharpe,
            "passes": average_walk_forward_sharpe >= minimum_acceptable_sharpe
        }
    )

    robustness_checks.append(
        {
            "robustness_check": "Out-of-Sample Sharpe",
            "metric_value": out_of_sample_sharpe,
            "limit": minimum_acceptable_sharpe,
            "passes": out_of_sample_sharpe >= minimum_acceptable_sharpe
        }
    )

    robustness_checks.append(
        {
            "robustness_check": "Average Sensitivity Drawdown",
            "metric_value": average_sensitivity_drawdown,
            "limit": maximum_acceptable_drawdown,
            "passes": average_sensitivity_drawdown >= maximum_acceptable_drawdown
        }
    )

    robustness_checks.append(
        {
            "robustness_check": "Average Walk-Forward Drawdown",
            "metric_value": average_walk_forward_drawdown,
            "limit": maximum_acceptable_drawdown,
            "passes": average_walk_forward_drawdown >= maximum_acceptable_drawdown
        }
    )

    robustness_checks.append(
        {
            "robustness_check": "Out-of-Sample Drawdown",
            "metric_value": out_of_sample_drawdown,
            "limit": maximum_acceptable_drawdown,
            "passes": out_of_sample_drawdown >= maximum_acceptable_drawdown
        }
    )

    robustness_dashboard = pd.DataFrame(robustness_checks)

    passed_checks = robustness_dashboard["passes"].sum()
    total_checks = len(robustness_dashboard)

    robustness_score = passed_checks / total_checks

    robustness_dashboard["robustness_score"] = robustness_score

    return robustness_dashboard


def summarize_robustness_dashboard(robustness_dashboard):
    if robustness_dashboard.empty:
        return {
            "total_checks": 0,
            "passed_checks": 0,
            "failed_checks": 0,
            "robustness_score": 0,
            "overall_status": "No Data"
        }

    total_checks = len(robustness_dashboard)
    passed_checks = robustness_dashboard["passes"].sum()
    failed_checks = total_checks - passed_checks
    robustness_score = passed_checks / total_checks

    if robustness_score >= 0.80:
        overall_status = "Robust"
    elif robustness_score >= 0.50:
        overall_status = "Moderately Robust"
    else:
        overall_status = "Fragile"

    return {
        "total_checks": total_checks,
        "passed_checks": passed_checks,
        "failed_checks": failed_checks,
        "robustness_score": robustness_score,
        "overall_status": overall_status
    }