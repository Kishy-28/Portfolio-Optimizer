"""
research_database_exporter.py

Export utilities for the centralized Portfolio Research Database.
"""

import os
import pandas as pd


def export_research_database_summary(
    research_database: dict,
    export_path: str,
) -> None:
    """
    Export the research database summary to CSV.
    """

    summary = research_database.get("summary", pd.DataFrame())

    os.makedirs(os.path.dirname(export_path), exist_ok=True)
    summary.to_csv(export_path, index=False)


def export_full_research_database(
    research_database: dict,
    export_folder: str,
) -> None:
    """
    Export every stored study in the research database as individual CSV files.
    """

    os.makedirs(export_folder, exist_ok=True)

    for section_name, section_data in research_database.items():
        if section_name in ["metadata", "summary"]:
            continue

        section_folder = os.path.join(export_folder, section_name)
        os.makedirs(section_folder, exist_ok=True)

        for study_name, study_record in section_data.items():
            data = study_record.get("data", pd.DataFrame())

            if isinstance(data, pd.DataFrame):
                clean_study_name = (
                    study_name.lower()
                    .replace(" ", "_")
                    .replace("/", "_")
                    .replace("\\", "_")
                )

                file_path = os.path.join(
                    section_folder,
                    f"{clean_study_name}.csv"
                )

                data.to_csv(file_path, index=False)


def export_research_database_metadata(
    research_database: dict,
    export_path: str,
) -> None:
    """
    Export research database metadata to CSV.
    """

    metadata = research_database.get("metadata", {})
    metadata_df = pd.DataFrame([metadata])

    os.makedirs(os.path.dirname(export_path), exist_ok=True)
    metadata_df.to_csv(export_path, index=False)