"""
final_research_report.py

Creates a final institutional research report for the Portfolio Optimizer.
"""

import pandas as pd


def create_final_research_report(
    research_database: dict,
    research_master_dashboard: pd.DataFrame,
) -> pd.DataFrame:
    """
    Create a final institutional summary report from the research database
    and master dashboard.
    """

    metadata = research_database.get("metadata", {})

    if research_master_dashboard.empty:
        return pd.DataFrame()

    total_studies = research_master_dashboard["number_of_studies"].sum()
    total_empty = research_master_dashboard["empty_studies"].sum()
    total_non_empty = research_master_dashboard["non_empty_studies"].sum()

    overall_completion_rate = (
        total_non_empty / total_studies if total_studies != 0 else 0
    )

    report = pd.DataFrame(
        [
            {
                "platform": metadata.get("platform", "Portfolio Optimizer"),
                "database_name": metadata.get("database_name", "Portfolio Research Database"),
                "phase": "Phase 10.6",
                "total_research_sections": len(research_master_dashboard),
                "total_research_studies": total_studies,
                "completed_research_studies": total_non_empty,
                "empty_research_studies": total_empty,
                "overall_completion_rate": overall_completion_rate,
                "final_status": (
                    "Complete"
                    if overall_completion_rate == 1
                    else "Review Required"
                ),
            }
        ]
    )

    return report