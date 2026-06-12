"""
research_database.py

Centralized research database layer for the Portfolio Optimizer project.

This module consolidates outputs from portfolio, strategy, regime, forecast,
risk, and dashboard research into a single structured research database.

The goal is to create a final institutional research platform layer that can
store, organize, export, and later summarize the full project output.
"""

from datetime import datetime
from typing import Any, Dict, Optional

import pandas as pd


def _safe_to_dataframe(data: Any) -> pd.DataFrame:
    """
    Convert supported research objects into a DataFrame.
    """
    if data is None:
        return pd.DataFrame()

    if isinstance(data, pd.DataFrame):
        return data.copy()

    if isinstance(data, pd.Series):
        return data.to_frame().T

    if isinstance(data, dict):
        return pd.DataFrame([data])

    if isinstance(data, list):
        return pd.DataFrame(data)

    return pd.DataFrame([{"value": data}])


def create_research_database(
    portfolio_studies: Optional[Dict[str, Any]] = None,
    strategy_studies: Optional[Dict[str, Any]] = None,
    regime_studies: Optional[Dict[str, Any]] = None,
    forecast_studies: Optional[Dict[str, Any]] = None,
    risk_studies: Optional[Dict[str, Any]] = None,
    dashboard_outputs: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Create a centralized research database.

    Parameters
    ----------
    portfolio_studies:
        Portfolio construction, optimization, backtesting, attribution,
        performance, and capacity outputs.

    strategy_studies:
        Strategy engine, strategy comparison, walk-forward, out-of-sample,
        sensitivity, robustness, and robustness dashboard outputs.

    regime_studies:
        Regime detection, attribution, strategy-by-regime, and regime dashboard
        outputs.

    forecast_studies:
        Forecast model, forecast evaluation, adaptive forecast, and
        regime-aware forecast outputs.

    risk_studies:
        VaR, CVaR, drawdown, stress testing, scenario analysis, concentration,
        tail risk, and governance outputs.

    dashboard_outputs:
        Final dashboard outputs generated across the project.

    Returns
    -------
    dict
        Centralized institutional research database.
    """

    database = {
        "metadata": {
            "database_name": "Portfolio Research Database",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "platform": "Portfolio Optimizer",
            "phase": "Phase 10.1",
            "description": (
                "Centralized database containing portfolio, strategy, regime, "
                "forecast, risk, and dashboard research outputs."
            ),
        },
        "portfolio_studies": {},
        "strategy_studies": {},
        "regime_studies": {},
        "forecast_studies": {},
        "risk_studies": {},
        "dashboard_outputs": {},
        "summary": {},
    }

    research_sections = {
        "portfolio_studies": portfolio_studies or {},
        "strategy_studies": strategy_studies or {},
        "regime_studies": regime_studies or {},
        "forecast_studies": forecast_studies or {},
        "risk_studies": risk_studies or {},
        "dashboard_outputs": dashboard_outputs or {},
    }

    for section_name, section_data in research_sections.items():
        for study_name, study_output in section_data.items():
            database[section_name][study_name] = {
                "study_name": study_name,
                "stored_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "data": _safe_to_dataframe(study_output),
            }

    database["summary"] = create_research_database_summary(database)

    return database


def create_research_database_summary(
    research_database: Dict[str, Any]
) -> pd.DataFrame:
    """
    Create a summary of all studies stored in the research database.
    """

    records = []

    for section_name, section_data in research_database.items():
        if section_name in ["metadata", "summary"]:
            continue

        for study_name, study_record in section_data.items():
            study_data = study_record.get("data", pd.DataFrame())

            records.append(
                {
                    "research_section": section_name,
                    "study_name": study_name,
                    "stored_at": study_record.get("stored_at"),
                    "rows": len(study_data),
                    "columns": len(study_data.columns)
                    if isinstance(study_data, pd.DataFrame)
                    else 0,
                    "is_empty": study_data.empty
                    if isinstance(study_data, pd.DataFrame)
                    else True,
                }
            )

    return pd.DataFrame(records)


def get_research_section(
    research_database: Dict[str, Any],
    section_name: str,
) -> Dict[str, Any]:
    """
    Retrieve one section from the research database.
    """
    return research_database.get(section_name, {})


def get_research_study(
    research_database: Dict[str, Any],
    section_name: str,
    study_name: str,
) -> pd.DataFrame:
    """
    Retrieve one specific study as a DataFrame.
    """
    section = research_database.get(section_name, {})
    study = section.get(study_name, {})

    return study.get("data", pd.DataFrame())


def list_research_sections(
    research_database: Dict[str, Any]
) -> list:
    """
    List available research sections.
    """
    return [
        key
        for key in research_database.keys()
        if key not in ["metadata", "summary"]
    ]


def list_research_studies(
    research_database: Dict[str, Any],
    section_name: str,
) -> list:
    """
    List available studies inside a research section.
    """
    section = research_database.get(section_name, {})
    return list(section.keys())


def validate_research_database(
    research_database: Dict[str, Any]
) -> bool:
    """
    Validate that the research database has the expected institutional structure.
    """

    required_sections = [
        "metadata",
        "portfolio_studies",
        "strategy_studies",
        "regime_studies",
        "forecast_studies",
        "risk_studies",
        "dashboard_outputs",
        "summary",
    ]

    for section in required_sections:
        if section not in research_database:
            return False

    return True