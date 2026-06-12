"""
research_database_reporting.py

Reporting utilities for the centralized Portfolio Research Database.
"""

import pandas as pd


def print_research_database_summary(title: str, research_database: dict) -> None:
    """
    Print a clean summary of the research database.
    """

    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)

    metadata = research_database.get("metadata", {})
    summary = research_database.get("summary", pd.DataFrame())

    print(f"Database Name: {metadata.get('database_name', 'N/A')}")
    print(f"Platform: {metadata.get('platform', 'N/A')}")
    print(f"Phase: {metadata.get('phase', 'N/A')}")
    print(f"Created At: {metadata.get('created_at', 'N/A')}")

    print("\nStored Research Studies")
    print("-" * 60)

    if summary.empty:
        print("No research studies stored.")
    else:
        print(summary.to_string(index=False))


def print_research_database_sections(research_database: dict) -> None:
    """
    Print all available research database sections.
    """

    print("\nAvailable Research Database Sections")
    print("=" * 60)

    for section in research_database.keys():
        if section not in ["metadata", "summary"]:
            print(f"- {section}")


def print_research_database_studies(
    research_database: dict,
    section_name: str,
) -> None:
    """
    Print all studies inside a selected research section.
    """

    print(f"\nStudies in Section: {section_name}")
    print("=" * 60)

    section = research_database.get(section_name, {})

    if not section:
        print("No studies found.")
        return

    for study_name in section.keys():
        print(f"- {study_name}")