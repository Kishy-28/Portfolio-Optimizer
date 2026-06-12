import pandas as pd


def prettify_label(value):
    return (
        str(value)
        .replace("_", " ")
        .strip()
        .title()
        .replace("Universe", "Portfolio")
    )


def prettify_value(value):
    if isinstance(value, str):
        had_underscore = "_" in value
        clean_value = value.replace("_", " ").strip()
        clean_value = (
            clean_value
            .replace("Universe", "Portfolio")
            .replace("universe", "portfolio")
        )

        if had_underscore or clean_value.islower():
            return clean_value.title()

        return clean_value

    return value


def prettify_display_text(value):
    if isinstance(value, str):
        clean_value = prettify_value(value)

        if "_" in value or clean_value != value:
            return clean_value

    return value


def format_percent_value(value, default="N/A"):
    if value is None or pd.isna(value):
        return default

    try:
        return f"{float(value):.2%}"
    except (TypeError, ValueError):
        return default


def format_number_value(value, default="N/A"):
    if value is None or pd.isna(value):
        return default

    try:
        return f"{float(value):.2f}"
    except (TypeError, ValueError):
        return default


def prettify_chart_categories(dataframe, columns):
    chart_dataframe = dataframe.copy()

    for column in columns:
        if column in chart_dataframe.columns:
            chart_dataframe[column] = chart_dataframe[column].map(
                prettify_display_text
            )

    return chart_dataframe


def prettify_dataframe(dataframe):
    if dataframe is None or dataframe.empty:
        return pd.DataFrame()

    clean_dataframe = dataframe.copy()
    clean_dataframe.columns = [prettify_label(column) for column in clean_dataframe.columns]

    text_columns = clean_dataframe.select_dtypes(include=["object", "string"]).columns
    for column in text_columns:
        clean_dataframe[column] = clean_dataframe[column].map(prettify_value)

    return clean_dataframe
