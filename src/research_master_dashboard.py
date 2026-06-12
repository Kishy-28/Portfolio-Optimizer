"""
research_master_dashboard.py

Creates a high-level master dashboard for the Portfolio Research Platform.
"""

import pandas as pd


def create_research_master_dashboard(research_database: dict) -> pd.DataFrame:
    """
    Create a master dashboard summarizing the full research database.
    """

    summary = research_database.get("summary", pd.DataFrame())

    if summary.empty:
        return pd.DataFrame()

    dashboard = (
        summary.groupby("research_section")
        .agg(
            number_of_studies=("study_name", "count"),
            total_rows=("rows", "sum"),
            total_columns=("columns", "sum"),
            empty_studies=("is_empty", "sum"),
        )
        .reset_index()
    )

    dashboard["non_empty_studies"] = (
        dashboard["number_of_studies"] - dashboard["empty_studies"]
    )

    dashboard["completion_rate"] = (
        dashboard["non_empty_studies"] / dashboard["number_of_studies"]
    )

    return dashboard