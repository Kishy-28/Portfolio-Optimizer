import os
from datetime import date

import pandas as pd
import plotly.express as px
import streamlit as st

from src.app_pipeline import run_portfolio_optimizer


EXPORTS_FOLDER = "exports"

CSV_FILES = {
    "Final Research Report": "final_research_report.csv",
    "Research Master Dashboard": "research_master_dashboard.csv",
    "Portfolio Results": "portfolio_results.csv",
    "Backtest Results": "backtest_results.csv",
    "Performance Summary": "performance_summary.csv",
    "Risk Dashboard": "risk_dashboard.csv",
    "Risk Governance Report": "risk_governance_report.csv",
    "Strategy Summary": "strategy_summary.csv",
    "Strategy Comparison": "strategy_comparison.csv",
    "Robustness Dashboard": "robustness_dashboard.csv",
    "Market Regime Summary": "market_regime_summary.csv",
    "Regime Attribution": "regime_attribution.csv",
    "Expected Return Forecasts": "expected_return_forecasts.csv",
    "Forecast Evaluation": "forecast_evaluation.csv",
    "Regime Forecast Dashboard": "regime_forecast_dashboard.csv",
    "Regime Strategy Dashboard": "regime_strategy_dashboard.csv",
    "Value-at-Risk Summary": "value_at_risk_summary.csv",
    "Stress Test Results": "stress_test_results.csv",
    "Scenario Analysis": "scenario_analysis.csv",
    "Market Shock Analysis": "market_shock_analysis.csv",
    "Concentration Summary": "concentration_summary.csv",
    "Tail Risk Summary": "tail_risk_summary.csv",
}


def load_csv(file_name):
    file_path = os.path.join(EXPORTS_FOLDER, file_name)

    if not os.path.exists(file_path):
        return pd.DataFrame()

    try:
        return pd.read_csv(file_path)
    except Exception:
        return pd.DataFrame()


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


def style_dark_dataframe(dataframe):
    return dataframe.style.set_table_styles(
        [
            {
                "selector": "thead th",
                "props": [
                    ("background-color", "#101827"),
                    ("color", "#E5E7EB"),
                    ("border-color", "#243044"),
                    ("font-family", "Geist, Inter, Segoe UI, sans-serif"),
                    ("font-weight", "500"),
                    ("letter-spacing", "0.01em"),
                    ("font-size", "0.82rem"),
                    ("padding", "0.42rem 0.58rem"),
                ],
            },
            {
                "selector": "tbody td",
                "props": [
                    ("background-color", "#0B1220"),
                    ("color", "#D6DEE9"),
                    ("border-color", "#1F2937"),
                    ("font-family", "Geist, Inter, Segoe UI, sans-serif"),
                    ("font-weight", "400"),
                    ("font-size", "0.82rem"),
                    ("padding", "0.38rem 0.58rem"),
                ],
            },
            {
                "selector": "tbody tr:nth-child(even) td",
                "props": [("background-color", "#0F172A")],
            },
        ]
    )


def show_dataframe(title, dataframe):
    with st.container(border=True):
        st.subheader(title)

        if dataframe is None or dataframe.empty:
            st.warning(f"{title} is not available yet.")
        else:
            display_dataframe = prettify_dataframe(dataframe)
            st.dataframe(
                style_dark_dataframe(display_dataframe),
                use_container_width=True,
                hide_index=True,
            )


def show_download_button(title, file_name):
    file_path = os.path.join(EXPORTS_FOLDER, file_name)

    if not os.path.exists(file_path):
        return

    try:
        with open(file_path, "rb") as file:
            st.download_button(
                label=f"Download {title}",
                data=file.read(),
                file_name=file_name,
                mime="text/csv",
                use_container_width=True,
            )
    except OSError:
        st.warning(f"{title} could not be prepared for download.")


def show_status_banner(live_mode):
    mode_text = (
        "Live mode active"
        if live_mode
        else "Export fallback active"
    )

    st.markdown(
        f"""
        <div class="mode-strip">
            <span></span>{mode_text}
        </div>
        """,
        unsafe_allow_html=True,
    )


def show_top_bar():
    portfolio_label = prettify_display_text(input_tickers)
    day_format = "%#d" if os.name == "nt" else "%-d"
    time_period = (
        f"{input_start_date.strftime(f'%b {day_format}, %Y')} - "
        f"{input_end_date.strftime(f'%b {day_format}, %Y')}"
    )

    st.markdown(
        f"""
        <div class="top-shell">
            <div class="top-brand">
                <div class="hamburger-icon"><span></span><span></span><span></span></div>
                <div class="brand-text">
                    <div>Portfolio</div>
                    <div>Optimizer</div>
                </div>
                <div class="live-pill">Live</div>
            </div>
            <div class="top-meta">
                <div class="meta-item">
                    <span>My Portfolio</span>
                    <strong>{portfolio_label}</strong>
                </div>
                <div class="meta-item">
                    <span>Time Period</span>
                    <strong>{time_period}</strong>
                </div>
                <div class="meta-item">
                    <span>Risk Free Rate</span>
                    <strong>{input_risk_free_rate:.2%}</strong>
                </div>
            </div>
            <div class="top-actions">
                <div class="theme-toggle"><span>☼</span><span>●</span></div>
                <div class="help-dot">?</div>
                <div class="export-pill">⇩ Export</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def show_reference_overview(
    expected_return,
    total_return,
    volatility,
    sharpe_ratio,
    max_drawdown,
    regime,
    adaptive_model,
):
    tickers = [
        ticker.strip().upper()
        for ticker in str(input_tickers).split(",")
        if ticker.strip()
    ]
    first_ticker = tickers[0] if tickers else "AAPL"
    second_ticker = tickers[1] if len(tickers) > 1 else "AVGO"
    conclusion = (
        create_live_executive_conclusion(st.session_state["live_results"])
        if st.session_state["live_results"] is not None
        else (
            "Review the selected portfolio through optimization, "
            "risk, backtesting, and research outputs."
        )
    )
    live_results = st.session_state["live_results"]
    risk_source = (
        live_results.get("live_risk_dashboard_table", pd.DataFrame())
        if live_results is not None
        else globals().get("risk_dashboard", pd.DataFrame())
    )
    var_source = (
        live_results.get("value_at_risk_summary", pd.DataFrame())
        if live_results is not None
        else globals().get("value_at_risk_summary", pd.DataFrame())
    )
    concentration_source = (
        live_results.get("live_concentration_table", pd.DataFrame())
        if live_results is not None
        else globals().get("concentration_summary", pd.DataFrame())
    )
    tail_source = (
        live_results.get("live_tail_risk_table", pd.DataFrame())
        if live_results is not None
        else globals().get("tail_risk_summary", pd.DataFrame())
    )
    value_at_risk = get_first_value(
        risk_source,
        "historical_var_95",
        get_first_value(var_source, "historical_var", None),
    )
    cvar_value = get_first_value(
        risk_source,
        "historical_cvar_95",
        get_first_value(var_source, "historical_cvar", None),
    )
    concentration_value = get_first_value(
        risk_source,
        "hhi",
        get_first_value(concentration_source, "hhi", None),
    )
    tail_ratio_value = get_first_value(
        risk_source,
        "tail_ratio",
        get_first_value(tail_source, "tail_ratio", None),
    )
    risk_status = "Moderate"
    if concentration_value is not None and not pd.isna(concentration_value):
        risk_status = "Elevated" if float(concentration_value) >= 0.65 else "Moderate"
    regime_text = prettify_display_text(regime)
    model_text = prettify_display_text(adaptive_model)
    sharpe_note = (
        "Backtest shows positive risk-adjusted performance."
        if sharpe_ratio > 0
        else "Risk-adjusted performance needs review."
    )
    concentration_note = (
        "Portfolio concentration remains moderate."
        if risk_status == "Moderate"
        else "Portfolio concentration is elevated."
    )

    st.markdown(
        f"""
        <div class="reference-grid">
            <div class="dashboard-panel performance-panel">
                <div class="panel-header">
                    <span>Live Portfolio Performance</span>
                </div>
                <svg class="performance-chart" viewBox="0 0 760 250" preserveAspectRatio="none">
                    <defs>
                        <linearGradient id="lineFade" x1="0" y1="0" x2="0" y2="1">
                            <stop offset="0%" stop-color="#1687FF" stop-opacity="0.28"/>
                            <stop offset="100%" stop-color="#1687FF" stop-opacity="0"/>
                        </linearGradient>
                    </defs>
                    <path d="M0,212 L65,172 L120,188 L180,156 L245,142 L315,112 L385,126 L455,88 L525,66 L590,44 L655,78 L720,62 L760,92 L760,250 L0,250 Z" fill="url(#lineFade)"/>
                    <polyline points="0,212 65,172 120,188 180,156 245,142 315,112 385,126 455,88 525,66 590,44 655,78 720,62 760,92" fill="none" stroke="#1687FF" stroke-width="3"/>
                    <circle cx="760" cy="92" r="6" fill="#1687FF"/>
                </svg>
                <div class="performance-stats">
                    <div><span>Total Return</span><strong class="positive">{total_return:.2%}</strong></div>
                    <div><span>Ann. Return</span><strong class="positive">{expected_return:.2%}</strong></div>
                    <div><span>Ann. Volatility</span><strong class="blue">{volatility:.2%}</strong></div>
                    <div><span>Sharpe Ratio</span><strong class="purple">{sharpe_ratio:.3f}</strong></div>
                    <div><span>Max Drawdown</span><strong class="negative">{max_drawdown:.2%}</strong></div>
                </div>
            </div>
            <div class="dashboard-panel allocation-panel">
                <div class="panel-header"><span>Allocation Overview</span></div>
                <div class="allocation-body">
                    <div class="allocation-ring"><span>40.0%</span></div>
                    <div class="allocation-legend">
                        <div><i class="blue-dot"></i>{first_ticker}<strong>40.0%</strong></div>
                        <div><i class="cyan-dot"></i>{second_ticker}<strong>60.0%</strong></div>
                    </div>
                </div>
            </div>
            <div class="dashboard-panel risk-panel">
                <div class="panel-header"><span>Risk Summary</span></div>
                <div class="risk-list">
                    <div><span><i class="risk-dot red-dot"></i>Max Drawdown</span><strong class="negative">{max_drawdown:.2%}</strong></div>
                    <div><span><i class="risk-dot red-dot"></i>Value at Risk</span><strong class="negative">{format_percent_value(value_at_risk)}</strong></div>
                    <div><span><i class="risk-dot red-dot"></i>CVaR</span><strong class="negative">{format_percent_value(cvar_value)}</strong></div>
                    <div><span><i class="risk-dot slate-dot"></i>Concentration Risk</span><strong>{format_number_value(concentration_value)}</strong></div>
                    <div><span><i class="risk-dot slate-dot"></i>Tail Ratio</span><strong>{format_number_value(tail_ratio_value)}</strong></div>
                    <div><span><i class="risk-dot yellow-dot"></i>Risk Status</span><strong class="yellow">{risk_status}</strong></div>
                </div>
            </div>
            <div class="dashboard-panel conclusion-panel">
                <div class="panel-header"><span>Executive Conclusion</span></div>
                <p>{conclusion}</p>
            </div>
            <div class="dashboard-panel key-panel">
                <div class="panel-header"><span>Key Statistics</span></div>
                <div class="risk-list">
                    <div><span>Optimized Max Sharpe Return</span><strong class="positive">{expected_return:.2%}</strong></div>
                    <div><span>Optimized Max Sharpe Volatility</span><strong class="blue">{volatility:.2%}</strong></div>
                    <div><span>Optimized Max Sharpe Ratio</span><strong class="purple">{sharpe_ratio:.3f}</strong></div>
                    <div><span>Current Market Regime</span><strong class="yellow">{regime_text}</strong></div>
                    <div><span>Recommended Forecast Model</span><strong class="cyan">{model_text}</strong></div>
                </div>
            </div>
            <div class="dashboard-panel insight-panel">
                <div class="panel-header"><span>Recent Insights</span></div>
                <ul>
                    <li>Market regime is {regime_text}.</li>
                    <li>{model_text} is the recommended forecast model.</li>
                    <li>{concentration_note}</li>
                    <li>{sharpe_note}</li>
                    <li>Key risk metrics are within review range.</li>
                </ul>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def show_section_intro(label, title, description):
    st.markdown(
        f"""
        <div class="section-card">
            <div class="section-label">{label}</div>
            <div class="section-title">{title}</div>
            <div class="section-description">{description}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def show_metric_card(label, value, caption="", accent="blue"):
    display_label = prettify_label(label)
    display_value = prettify_display_text(value)
    display_caption = prettify_display_text(caption)

    st.markdown(
        f"""
        <div class="metric-card metric-{accent}">
            <div class="metric-label">{display_label}</div>
            <div class="metric-value">{display_value}</div>
            <div class="metric-caption">{display_caption}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def show_footer():
    st.markdown("---")
    st.caption(
        "Portfolio Optimizer | Interactive Research Dashboard | Dark Fintech UI"
    )


def format_percentage_axis(figure, axis_name):
    if axis_name == "x":
        figure.update_xaxes(tickformat=".1%")
    elif axis_name == "y":
        figure.update_yaxes(tickformat=".1%")


def configure_chart(figure, height=470):
    figure.update_layout(
        template="plotly_dark",
        height=height,
        paper_bgcolor="rgba(9, 14, 25, 0)",
        plot_bgcolor="#0B1220",
        colorway=[
            "#38BDF8",
            "#22C55E",
            "#F59E0B",
            "#A78BFA",
            "#F43F5E",
            "#14B8A6",
        ],
        font=dict(
            family="Geist, Inter, Segoe UI, sans-serif",
            color="#D6DEE9",
            size=12,
        ),
        title=dict(
            font=dict(size=17, color="#F8FAFC"),
            x=0.02,
        ),
        margin=dict(l=18, r=18, t=54, b=24),
        legend_title_text="",
        hoverlabel=dict(
            bgcolor="#050A14",
            bordercolor="#263244",
            font_size=12,
            font_family="Geist, Inter, Segoe UI, sans-serif",
        ),
    )

    figure.update_xaxes(
        gridcolor="rgba(148, 163, 184, 0.10)",
        zerolinecolor="rgba(148, 163, 184, 0.16)",
        title_font=dict(color="#AAB6C5"),
        tickfont=dict(color="#AAB6C5"),
        linecolor="rgba(148, 163, 184, 0.18)",
    )

    figure.update_yaxes(
        gridcolor="rgba(148, 163, 184, 0.10)",
        zerolinecolor="rgba(148, 163, 184, 0.16)",
        title_font=dict(color="#AAB6C5"),
        tickfont=dict(color="#AAB6C5"),
        linecolor="rgba(148, 163, 184, 0.18)",
    )

    return figure


def build_live_portfolio_results(live_results):
    max_sharpe = live_results["max_sharpe_summary"]
    min_volatility = live_results["min_volatility_summary"]

    rows = []

    for summary in [max_sharpe, min_volatility]:
        row = {
            "portfolio": summary["name"],
            "return": summary["return"],
            "volatility": summary["volatility"],
            "sharpe_ratio": summary["sharpe_ratio"],
        }

        weights_table = summary["weights_table"]

        for _, weight_row in weights_table.iterrows():
            row[weight_row["ticker"]] = weight_row["weight"]

        rows.append(row)

    return pd.DataFrame(rows)


def create_risk_return_chart(portfolio_data):
    chart_data = portfolio_data.copy()

    chart_data["marker_size"] = (
        chart_data["sharpe_ratio"]
        .abs()
        .fillna(0)
        .clip(lower=0.05)
    )

    chart_data = prettify_chart_categories(chart_data, ["portfolio"])

    figure = px.scatter(
        chart_data,
        x="volatility",
        y="return",
        color="sharpe_ratio",
        size="marker_size",
        size_max=35,
        hover_name="portfolio",
        hover_data={
            "volatility": ":.2%",
            "return": ":.2%",
            "sharpe_ratio": ":.3f",
            "marker_size": False,
        },
        title="Portfolio Risk vs. Expected Return",
        labels={
            "volatility": "Annualized Volatility",
            "return": "Expected Annual Return",
            "sharpe_ratio": "Sharpe Ratio",
        },
    )

    format_percentage_axis(figure, "x")
    format_percentage_axis(figure, "y")

    return configure_chart(figure)


def create_sharpe_chart(portfolio_data):
    chart_data = portfolio_data.sort_values(
        "sharpe_ratio",
        ascending=True,
    )
    chart_data = prettify_chart_categories(chart_data, ["portfolio"])

    figure = px.bar(
        chart_data,
        x="sharpe_ratio",
        y="portfolio",
        orientation="h",
        color="sharpe_ratio",
        title="Portfolio Sharpe Ratio Comparison",
        labels={
            "sharpe_ratio": "Sharpe Ratio",
            "portfolio": "Portfolio",
        },
        text_auto=".3f",
    )

    figure.update_layout(
        coloraxis_showscale=False,
        yaxis_title=None,
    )

    return configure_chart(figure, height=500)


def create_return_volatility_chart(portfolio_data):
    chart_data = portfolio_data[
        ["portfolio", "return", "volatility"]
    ].copy()
    chart_data = prettify_chart_categories(chart_data, ["portfolio"])

    chart_data = chart_data.melt(
        id_vars="portfolio",
        value_vars=["return", "volatility"],
        var_name="metric",
        value_name="value",
    )

    chart_data["metric"] = chart_data["metric"].replace(
        {
            "return": "Expected Return",
            "volatility": "Volatility",
        }
    )

    figure = px.bar(
        chart_data,
        x="portfolio",
        y="value",
        color="metric",
        barmode="group",
        title="Expected Return and Volatility by Portfolio",
        labels={
            "portfolio": "Portfolio",
            "value": "Annualized Value",
            "metric": "Metric",
        },
    )

    format_percentage_axis(figure, "y")
    figure.update_layout(xaxis_tickangle=-25)

    return configure_chart(figure, height=520)


def create_portfolio_allocation_chart(portfolio_data):
    identifier_columns = {
        "portfolio",
        "return",
        "volatility",
        "sharpe_ratio",
    }

    asset_columns = [
        column
        for column in portfolio_data.columns
        if column not in identifier_columns
    ]

    if not asset_columns:
        return None, None

    selected_portfolio = st.selectbox(
        "Select portfolio allocation",
        options=portfolio_data["portfolio"].tolist(),
        format_func=prettify_display_text,
        key="portfolio_allocation_selector",
    )

    selected_row = portfolio_data.loc[
        portfolio_data["portfolio"] == selected_portfolio
    ].iloc[0]

    allocation_data = pd.DataFrame(
        {
            "Asset": asset_columns,
            "Weight": [
                pd.to_numeric(selected_row[column], errors="coerce")
                for column in asset_columns
            ],
        }
    )

    allocation_data = allocation_data.dropna()
    allocation_data = allocation_data[
        allocation_data["Weight"].abs() > 1e-8
    ]

    if allocation_data.empty:
        return selected_portfolio, None

    figure = px.pie(
        allocation_data,
        names="Asset",
        values="Weight",
        hole=0.55,
        title=f"{prettify_display_text(selected_portfolio)} Allocation",
    )

    figure.update_traces(
        textposition="inside",
        textinfo="label+percent",
        hovertemplate=(
            "<b>%{label}</b><br>"
            "Weight: %{value:.2%}"
            "<extra></extra>"
        ),
    )

    return selected_portfolio, configure_chart(figure, height=500)


def create_live_strategy_summary(live_results):
    portfolio_results = live_results.get("portfolio_results_table", pd.DataFrame()).copy()

    if portfolio_results.empty:
        return pd.DataFrame()

    description_map = {
        "Best Simulated Sharpe": "Highest Sharpe portfolio found through Monte Carlo simulation.",
        "Optimized Max Sharpe": "Mathematically optimized portfolio designed to maximize Sharpe ratio.",
        "Best Simulated Min Volatility": "Lowest volatility portfolio found through Monte Carlo simulation.",
        "Optimized Min Volatility": "Mathematically optimized portfolio designed to minimize volatility.",
    }

    strategy_type_map = {
        "Best Simulated Sharpe": "Simulation",
        "Optimized Max Sharpe": "Optimization",
        "Best Simulated Min Volatility": "Simulation",
        "Optimized Min Volatility": "Optimization",
    }

    portfolio_results.insert(
        1,
        "strategy_type",
        portfolio_results["portfolio"].map(strategy_type_map).fillna("Live Strategy"),
    )

    portfolio_results.insert(
        2,
        "description",
        portfolio_results["portfolio"].map(description_map).fillna(
            "Live strategy for the selected portfolio."
        ),
    )

    portfolio_results = portfolio_results.rename(
        columns={
            "portfolio": "strategy_name",
        }
    )

    return portfolio_results


def create_backtest_return_chart(backtest_data):
    chart_data = backtest_data[
        ["strategy", "total_return", "annualized_return"]
    ].copy()
    chart_data = prettify_chart_categories(chart_data, ["strategy"])

    chart_data = chart_data.melt(
        id_vars="strategy",
        value_vars=["total_return", "annualized_return"],
        var_name="metric",
        value_name="value",
    )

    chart_data["metric"] = chart_data["metric"].replace(
        {
            "total_return": "Total Return",
            "annualized_return": "Annualized Return",
        }
    )

    figure = px.bar(
        chart_data,
        x="strategy",
        y="value",
        color="metric",
        barmode="group",
        title="Backtest Return Comparison",
        labels={
            "strategy": "Strategy",
            "value": "Return",
            "metric": "Metric",
        },
        text_auto=".1%",
    )

    format_percentage_axis(figure, "y")

    return configure_chart(figure)


def create_backtest_sharpe_chart(backtest_data):
    chart_data = backtest_data.sort_values(
        "sharpe_ratio",
        ascending=True,
    )
    chart_data = prettify_chart_categories(chart_data, ["strategy"])

    figure = px.bar(
        chart_data,
        x="sharpe_ratio",
        y="strategy",
        orientation="h",
        color="sharpe_ratio",
        title="Backtest Sharpe Ratio Comparison",
        labels={
            "strategy": "Strategy",
            "sharpe_ratio": "Sharpe Ratio",
        },
        text_auto=".3f",
    )

    figure.update_layout(
        coloraxis_showscale=False,
        yaxis_title=None,
    )

    return configure_chart(figure)


def create_backtest_drawdown_chart(backtest_data):
    chart_data = backtest_data.sort_values(
        "max_drawdown",
        ascending=True,
    )
    chart_data = prettify_chart_categories(chart_data, ["strategy"])

    figure = px.bar(
        chart_data,
        x="strategy",
        y="max_drawdown",
        color="strategy",
        title="Maximum Drawdown Comparison",
        labels={
            "strategy": "Strategy",
            "max_drawdown": "Maximum Drawdown",
        },
        text_auto=".1%",
    )

    format_percentage_axis(figure, "y")
    figure.update_layout(showlegend=False)

    return configure_chart(figure)


def create_backtest_risk_return_chart(backtest_data):
    chart_data = prettify_chart_categories(backtest_data, ["strategy"])

    figure = px.scatter(
        chart_data,
        x="annualized_volatility",
        y="annualized_return",
        color="strategy",
        size="sharpe_ratio",
        size_max=35,
        hover_name="strategy",
        hover_data={
            "annualized_volatility": ":.2%",
            "annualized_return": ":.2%",
            "sharpe_ratio": ":.3f",
            "max_drawdown": ":.2%",
        },
        title="Realized Backtest Risk vs. Return",
        labels={
            "annualized_volatility": "Annualized Volatility",
            "annualized_return": "Annualized Return",
            "sharpe_ratio": "Sharpe Ratio",
        },
    )

    format_percentage_axis(figure, "x")
    format_percentage_axis(figure, "y")

    return configure_chart(figure)


def get_first_value(dataframe, column, default=None):
    if dataframe is None or dataframe.empty or column not in dataframe.columns:
        return default

    return dataframe[column].iloc[0]


def create_live_research_summary(live_results):
    max_sharpe = live_results.get("max_sharpe_summary", {})
    inputs = live_results.get("inputs", {})
    latest_regime = live_results.get("latest_market_regime", {})
    adaptive_forecast = live_results.get(
        "adaptive_forecast_recommendation",
        pd.DataFrame(),
    )
    risk_dashboard = live_results.get(
        "live_risk_dashboard_table",
        pd.DataFrame(),
    )
    backtest = live_results.get(
        "live_backtest_table",
        pd.DataFrame(),
    )

    recommended_model = get_first_value(
        adaptive_forecast,
        "recommended_forecast_model",
        "Not Available",
    )

    risk_status = get_first_value(
        risk_dashboard,
        "overall_risk_status",
        "Live risk review completed",
    )

    backtest_return = get_first_value(
        backtest,
        "annualized_return",
        None,
    )

    backtest_sharpe = get_first_value(
        backtest,
        "sharpe_ratio",
        None,
    )

    rows = [
        {
            "section": "Portfolio",
            "finding": "Selected Portfolio",
            "conclusion": ", ".join(inputs.get("tickers", [])),
        },
        {
            "section": "Optimization",
            "finding": "Optimized Max Sharpe Portfolio",
            "conclusion": (
                f"Expected return of {max_sharpe.get('return', 0):.2%}, "
                f"expected volatility of {max_sharpe.get('volatility', 0):.2%}, "
                f"and Sharpe ratio of {max_sharpe.get('sharpe_ratio', 0):.3f}."
            ),
        },
        {
            "section": "Backtesting",
            "finding": "Live Backtest Profile",
            "conclusion": (
                "Backtest results are available for the selected portfolio."
                if backtest_return is None
                else (
                    f"Annualized return of {backtest_return:.2%} with "
                    f"a realized Sharpe ratio of {backtest_sharpe:.3f}."
                )
            ),
        },
        {
            "section": "Risk Management",
            "finding": "Institutional Risk Review",
            "conclusion": str(risk_status),
        },
        {
            "section": "Regime Analysis",
            "finding": "Current Market Regime",
            "conclusion": str(latest_regime.get("market_regime", "Not Available")),
        },
        {
            "section": "Forecast Research",
            "finding": "Adaptive Forecast Model",
            "conclusion": str(recommended_model),
        },
    ]

    return pd.DataFrame(rows)


def create_live_executive_conclusion(live_results):
    max_sharpe = live_results.get("max_sharpe_summary", {})
    latest_regime = live_results.get("latest_market_regime", {})
    inputs = live_results.get("inputs", {})

    tickers = ", ".join(inputs.get("tickers", []))
    regime = prettify_display_text(
        latest_regime.get("market_regime", "the current detected regime")
    )

    return (
        f"Live analysis reviewed {tickers} with the current assumptions. "
        f"The optimized max Sharpe portfolio shows an expected return of "
        f"{max_sharpe.get('return', 0):.2%}, expected volatility of "
        f"{max_sharpe.get('volatility', 0):.2%}, and a Sharpe ratio of "
        f"{max_sharpe.get('sharpe_ratio', 0):.3f}. The current regime is "
        f"{regime}."
    )


st.set_page_config(
    page_title="Portfolio Optimizer",
    page_icon="P",
    layout="wide",
    initial_sidebar_state="expanded",
)

if "live_results" not in st.session_state:
    st.session_state["live_results"] = None

if "live_portfolio_results" not in st.session_state:
    st.session_state["live_portfolio_results"] = pd.DataFrame()

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Geist:wght@300;400;500;600;700;800&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,300..500,0..1,-50..200&display=block');
    @import url('https://fonts.googleapis.com/icon?family=Material+Icons');

    html,
    body,
    body *,
    [class*="css"],
    [class*="st-"],
    [data-testid],
    [data-baseweb] {
        font-family: 'Geist', 'Inter', 'Segoe UI', sans-serif !important;
    }

    .stMarkdown,
    .stMarkdown *,
    .stCaptionContainer,
    .stCaptionContainer *,
    .stAlert,
    .stAlert *,
    .stButton button,
    .stDownloadButton button,
    .stTextInput *,
    .stNumberInput *,
    .stDateInput *,
    .stSelectbox *,
    .stDataFrame *,
    .stTable *,
    .stMetric *,
    .js-plotly-plot,
    .js-plotly-plot * {
        font-family: 'Geist', 'Inter', 'Segoe UI', sans-serif !important;
    }

    .material-icons,
    .material-icons-outlined,
    .material-icons-round,
    .material-icons-sharp,
    .material-symbols-outlined,
    .material-symbols-rounded,
    .material-symbols-sharp,
    [class*="material-icons"],
    [class*="material-symbols"] {
        font-family: 'Material Symbols Rounded', 'Material Symbols Outlined', 'Material Icons' !important;
        font-weight: 400 !important;
        font-style: normal !important;
        font-size: 1rem !important;
        line-height: 1 !important;
        letter-spacing: normal !important;
        text-transform: none !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        white-space: nowrap !important;
        word-wrap: normal !important;
        direction: ltr !important;
        -webkit-font-feature-settings: 'liga' !important;
        -webkit-font-smoothing: antialiased !important;
        font-feature-settings: 'liga' !important;
    }

    .stApp {
        font-family: 'Geist', 'Inter', 'Segoe UI', sans-serif !important;
        background:
            linear-gradient(180deg, #02070D 0%, #07111D 44%, #08131F 100%);
        color: #F9FAFB;
        letter-spacing: 0.005em;
    }

    .block-container {
        padding-top: 0.25rem;
        padding-bottom: 2rem;
        max-width: 1480px;
        border-left: 1px solid rgba(56, 189, 248, 0.12);
        border-right: 1px solid rgba(56, 189, 248, 0.12);
    }

    h1 {
        font-size: 2.18rem !important;
        font-weight: 560 !important;
        letter-spacing: 0.005em !important;
        color: #F9FAFB !important;
        margin-bottom: 0.6rem !important;
    }

    h2 {
        font-size: 1.34rem !important;
        font-weight: 540 !important;
        letter-spacing: 0.006em !important;
        color: #F9FAFB !important;
    }

    h3 {
        font-size: 1.02rem !important;
        font-weight: 520 !important;
        letter-spacing: 0.006em !important;
        color: #F9FAFB !important;
    }

    p, li, span, div {
        color: inherit;
        font-family: 'Geist', 'Inter', 'Segoe UI', sans-serif !important;
        font-weight: 400;
    }

    span.material-icons,
    span.material-icons-outlined,
    span.material-icons-round,
    span.material-icons-sharp,
    span.material-symbols-outlined,
    span.material-symbols-rounded,
    span.material-symbols-sharp,
    span[class*="material-icons"],
    span[class*="material-symbols"],
    i[class*="material-icons"],
    i[class*="material-symbols"],
    [data-testid="stSidebarCollapseButton"] *,
    [data-testid="collapsedControl"] * {
        font-family: 'Material Symbols Rounded', 'Material Symbols Outlined', 'Material Icons' !important;
        font-weight: 400 !important;
        font-size: 1rem !important;
        letter-spacing: normal !important;
        text-transform: none !important;
        font-feature-settings: 'liga' !important;
    }

    button,
    input,
    textarea,
    label,
    [data-testid="stSidebar"],
    [data-testid="stDataFrame"],
    [data-testid="stTable"],
    [data-baseweb="tab"],
    [data-baseweb="input"],
    [data-baseweb="select"] {
        font-family: 'Geist', 'Inter', 'Segoe UI', sans-serif !important;
    }

    [data-testid="stSidebar"] {
        background:
            linear-gradient(180deg, #030A12 0%, #06111D 100%);
        border-right: 1px solid rgba(56, 189, 248, 0.18);
        box-shadow: inset -1px 0 0 rgba(15, 23, 42, 0.8);
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #F9FAFB !important;
    }

    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] span {
        color: #CBD5E1 !important;
    }

    [data-testid="stSidebar"] input {
        background-color: #0B1220 !important;
        color: #F9FAFB !important;
        border: 1px solid rgba(148, 163, 184, 0.20) !important;
        border-radius: 8px !important;
    }

    [data-baseweb="input"],
    [data-baseweb="select"],
    [data-baseweb="popover"],
    [data-baseweb="menu"] {
        background-color: #0B1220 !important;
        color: #F9FAFB !important;
    }

    [data-baseweb="select"] > div,
    [data-baseweb="input"] > div {
        background-color: #0B1220 !important;
        border-color: rgba(148, 163, 184, 0.20) !important;
        border-radius: 8px !important;
    }

    [data-baseweb="menu"] li {
        background-color: #0B1220 !important;
        color: #E5E7EB !important;
    }

    [data-testid="stSidebar"] button {
        border-radius: 8px !important;
        min-height: 2.65rem !important;
        font-weight: 520 !important;
        background: linear-gradient(135deg, #1D4ED8, #0891B2) !important;
        color: white !important;
        border: 1px solid rgba(56, 189, 248, 0.42) !important;
        box-shadow: 0 10px 24px rgba(14, 165, 233, 0.18);
    }

    [data-testid="stSidebar"] [data-testid="stNumberInput"] button {
        width: 1.45rem !important;
        min-width: 1.45rem !important;
        height: 1.45rem !important;
        min-height: 1.45rem !important;
        padding: 0 !important;
        border-radius: 6px !important;
        background: rgba(15, 23, 42, 0.72) !important;
        border: 1px solid rgba(100, 116, 139, 0.18) !important;
        color: #64748B !important;
        box-shadow: none !important;
        font-size: 0.72rem !important;
        font-weight: 400 !important;
        line-height: 1 !important;
    }

    [data-testid="stSidebar"] [data-testid="stNumberInput"] button:hover {
        background: rgba(30, 41, 59, 0.72) !important;
        border-color: rgba(100, 116, 139, 0.28) !important;
        color: #94A3B8 !important;
    }

    [data-testid="stSidebar"] [data-testid="stNumberInput"] button svg,
    [data-testid="stSidebar"] [data-testid="stNumberInput"] button span {
        width: 0.72rem !important;
        height: 0.72rem !important;
        font-size: 0.72rem !important;
        color: #64748B !important;
    }

    [data-testid="stSidebarCollapseButton"],
    [data-testid="collapsedControl"] {
        font-size: 0 !important;
        color: transparent !important;
    }

    [data-testid="stSidebarCollapseButton"] *,
    [data-testid="collapsedControl"] * {
        font-size: 0 !important;
        color: transparent !important;
    }

    [data-testid="stSidebarCollapseButton"]::before,
    [data-testid="collapsedControl"]::before {
        content: "\\2039";
        display: grid;
        place-items: center;
        width: 1.65rem;
        height: 1.65rem;
        border-radius: 7px;
        color: #7B8AA0;
        background: rgba(15, 23, 42, 0.72);
        border: 1px solid rgba(100, 116, 139, 0.18);
        font-size: 1rem;
        line-height: 1;
    }

    [data-testid="stHeader"] button:first-of-type,
    [data-testid="stToolbar"] button:first-of-type {
        width: 1.8rem !important;
        min-width: 1.8rem !important;
        max-width: 1.8rem !important;
        overflow: hidden !important;
        color: transparent !important;
        font-size: 0 !important;
    }

    [data-testid="stHeader"] button:first-of-type *,
    [data-testid="stToolbar"] button:first-of-type * {
        color: transparent !important;
        font-size: 0 !important;
    }

    [data-testid="stHeader"] button:first-of-type::before,
    [data-testid="stToolbar"] button:first-of-type::before {
        content: "\\2039";
        display: grid;
        place-items: center;
        width: 1.45rem;
        height: 1.45rem;
        border-radius: 7px;
        color: #7B8AA0;
        background: rgba(15, 23, 42, 0.72);
        border: 1px solid rgba(100, 116, 139, 0.18);
        font-size: 0.95rem;
        line-height: 1;
    }

    .sidebar-brand {
        padding: 0.2rem 0 0.75rem 0;
        display: grid;
        grid-template-columns: 1fr auto;
        align-items: center;
        gap: 0.72rem;
    }

    .sidebar-kicker {
        color: #AAB6C5;
        font-size: 0.78rem;
        letter-spacing: 0.22em;
        text-transform: uppercase;
        font-weight: 500;
        line-height: 1.05;
    }

    .sidebar-title {
        color: #F8FAFC;
        font-size: 1rem;
        font-weight: 650;
        letter-spacing: 0.08em;
        line-height: 1.05;
        text-transform: uppercase;
        margin-top: 0;
    }

    .nav-group {
        margin: 0.3rem 0 1rem 0;
    }

    .nav-heading {
        color: #93A4B8;
        font-size: 0.68rem;
        letter-spacing: 0.16em;
        text-transform: uppercase;
        font-weight: 500;
        margin: 1rem 0 0.5rem;
    }

    .nav-item {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.58rem 0.65rem;
        margin-bottom: 0.18rem;
        border-radius: 6px;
        color: #CBD5E1;
        background: transparent;
        border: 1px solid transparent;
        font-size: 0.86rem;
        font-weight: 400;
        letter-spacing: 0.01em;
    }

    .nav-item.active {
        background: linear-gradient(90deg, rgba(18, 89, 166, 0.32), rgba(15, 23, 42, 0.20));
        border-color: rgba(56, 189, 248, 0.16);
        box-shadow: inset 3px 0 0 #1687FF;
        color: #F8FAFC;
    }

    .nav-dot {
        width: 1rem;
        height: 1rem;
        border-radius: 999px;
        background: transparent;
        border: 1px solid #7B8AA0;
        flex: 0 0 auto;
    }

    .nav-item.active .nav-dot {
        border-color: #1687FF;
        box-shadow: 0 0 12px rgba(22, 135, 255, 0.35);
    }

    .sidebar-live-card {
        margin-top: 1.2rem;
        padding: 0.9rem;
        border-radius: 8px;
        background: linear-gradient(180deg, rgba(15, 23, 42, 0.86), rgba(5, 12, 22, 0.9));
        border: 1px solid rgba(148, 163, 184, 0.14);
    }

    .sidebar-live-card div {
        display: flex;
        align-items: center;
        gap: 0.45rem;
        color: #4ADE80;
        text-transform: uppercase;
        font-size: 0.72rem;
        font-weight: 600;
    }

    .sidebar-live-card div span {
        width: 0.48rem;
        height: 0.48rem;
        border-radius: 999px;
        background: #22C55E;
        box-shadow: 0 0 14px rgba(34, 197, 94, 0.38);
    }

    .sidebar-live-card p {
        margin: 0.55rem 0 0;
        color: #AAB6C5;
        font-size: 0.76rem;
        line-height: 1.45;
    }

    .top-shell {
        height: 64px;
        margin: -0.25rem -1rem 1.35rem;
        padding: 0 1.2rem;
        display: grid;
        grid-template-columns: minmax(260px, 1fr) auto auto;
        gap: 2.4rem;
        align-items: center;
        background: rgba(2, 8, 15, 0.92);
        border-bottom: 1px solid rgba(148, 163, 184, 0.16);
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.28);
    }

    .top-brand {
        display: flex;
        align-items: center;
        gap: 0.9rem;
        min-width: 0;
    }

    .hamburger-icon {
        display: grid;
        gap: 4px;
        margin-right: 0.3rem;
    }

    .hamburger-icon span {
        width: 16px;
        height: 2px;
        border-radius: 999px;
        background: #E5E7EB;
    }

    .brand-text {
        color: #F8FAFC;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-size: 1rem;
        line-height: 1.08;
        font-weight: 650;
    }

    .brand-text div:nth-child(2) {
        color: #AAB6C5;
        font-size: 0.78rem;
        letter-spacing: 0.22em;
        font-weight: 500;
    }

    .live-pill {
        color: #4ADE80;
        background: rgba(34, 197, 94, 0.16);
        border: 1px solid rgba(34, 197, 94, 0.24);
        border-radius: 5px;
        padding: 0.16rem 0.42rem;
        font-size: 0.68rem;
        font-weight: 600;
        text-transform: uppercase;
    }

    .top-meta {
        display: flex;
        align-items: center;
        gap: 2rem;
    }

    .meta-item {
        min-width: 128px;
        padding-left: 1.2rem;
        border-left: 1px solid rgba(148, 163, 184, 0.22);
    }

    .meta-item span {
        display: block;
        color: #F8FAFC;
        font-size: 0.72rem;
        font-weight: 500;
        margin-bottom: 0.18rem;
    }

    .meta-item strong {
        display: block;
        color: #AAB6C5;
        font-size: 0.72rem;
        font-weight: 400;
    }

    .top-actions {
        display: flex;
        justify-content: flex-end;
        align-items: center;
        gap: 0.78rem;
    }

    .theme-toggle {
        display: flex;
        align-items: center;
        gap: 0.42rem;
        padding: 0.38rem 0.52rem;
        border-radius: 999px;
        background: rgba(15, 23, 42, 0.86);
        border: 1px solid rgba(148, 163, 184, 0.18);
        color: #AAB6C5;
        font-size: 0.78rem;
    }

    .help-dot {
        width: 1.45rem;
        height: 1.45rem;
        border-radius: 999px;
        border: 1px solid rgba(148, 163, 184, 0.38);
        display: grid;
        place-items: center;
        color: #C6D0DD;
        font-size: 0.78rem;
    }

    .export-pill {
        border-radius: 6px;
        padding: 0.52rem 0.85rem;
        background: linear-gradient(180deg, #0B7CFF, #075CCB);
        border: 1px solid rgba(96, 165, 250, 0.35);
        color: white;
        font-size: 0.82rem;
        font-weight: 560;
        box-shadow: 0 10px 22px rgba(37, 99, 235, 0.28);
    }

    .hero-card {
        width: min(100%, 1180px);
        padding: 0.3rem 0 0.72rem;
        border-radius: 0;
        background: transparent;
        border: 0;
        margin: 0 auto 0.85rem;
        box-shadow: none;
        position: relative;
    }

    .hero-card::before {
        content: "";
        position: absolute;
        left: 0;
        right: 0;
        top: 0;
        display: none;
    }

    .hero-title {
        font-size: clamp(2.05rem, 3.2vw, 3rem);
        font-weight: 700;
        color: #F9FAFB;
        margin-bottom: 0.25rem;
        letter-spacing: -0.015em;
        line-height: 1.12;
    }

    .hero-subtitle {
        font-size: 1.05rem;
        color: #C6D0DD;
        max-width: 920px;
        line-height: 1.45;
        font-weight: 380;
        letter-spacing: 0.01em;
    }

    .hero-card .section-label {
        margin-bottom: 0.5rem;
        color: #7DD3FC;
    }

    .mode-strip {
        width: min(100%, 1180px);
        margin: 0 auto 0.9rem;
        display: flex;
        align-items: center;
        gap: 0.45rem;
        color: #AAB6C5;
        font-size: 0.78rem;
    }

    .mode-strip span {
        width: 0.45rem;
        height: 0.45rem;
        border-radius: 999px;
        background: #22C55E;
        box-shadow: 0 0 12px rgba(34, 197, 94, 0.36);
    }

    .section-card {
        padding: 1rem 1.1rem;
        border-radius: 8px;
        background: rgba(12, 18, 31, 0.76);
        border: 1px solid rgba(148, 163, 184, 0.14);
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.22);
        margin-bottom: 0.9rem;
    }

    .section-label {
        font-size: 0.64rem;
        color: #38BDF8;
        text-transform: uppercase;
        letter-spacing: 0.18em;
        margin-bottom: 0.52rem;
        font-weight: 500;
    }

    .section-title {
        font-size: 1.08rem;
        line-height: 1.34;
        color: #F9FAFB;
        font-weight: 520;
        letter-spacing: 0.006em;
        margin-bottom: 0.35rem;
    }

    .section-description {
        font-size: 0.9rem;
        color: #AAB6C5;
        line-height: 1.62;
        font-weight: 380;
    }

    .metric-card {
        min-height: 84px;
        padding: 0.72rem 0.9rem;
        border-radius: 8px;
        background:
            linear-gradient(180deg, rgba(15, 23, 42, 0.92), rgba(8, 13, 24, 0.88));
        border: 1px solid rgba(148, 163, 184, 0.15);
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.27);
        margin-bottom: 0.62rem;
        position: relative;
        overflow: hidden;
    }

    .metric-card::after {
        content: "";
        position: absolute;
        right: 0.9rem;
        bottom: 0.82rem;
        width: 4rem;
        height: 1rem;
        opacity: 0.82;
        background:
            linear-gradient(135deg, transparent 12%, currentColor 13%, currentColor 16%, transparent 17%),
            linear-gradient(45deg, transparent 30%, currentColor 31%, currentColor 34%, transparent 35%);
        clip-path: polygon(0 76%, 16% 56%, 29% 62%, 43% 39%, 58% 50%, 73% 24%, 86% 35%, 100% 5%, 100% 16%, 86% 48%, 73% 36%, 58% 64%, 43% 53%, 30% 77%, 16% 69%, 0 90%);
    }

    .metric-label {
        font-size: 0.6rem;
        text-transform: uppercase;
        letter-spacing: 0.16em;
        color: #94A3B8;
        font-weight: 500;
        margin-bottom: 0.36rem;
    }

    .metric-value {
        font-size: 1.22rem;
        line-height: 1.15;
        font-weight: 540;
        letter-spacing: 0.004em;
        margin-bottom: 0.34rem;
        overflow-wrap: anywhere;
    }

    .metric-caption {
        font-size: 0.72rem;
        color: #AAB6C5;
        font-weight: 380;
        line-height: 1.5;
    }

    .metric-blue .metric-value { color: #3B82F6; }
    .metric-green .metric-value { color: #22C55E; }
    .metric-purple .metric-value { color: #A855F7; }
    .metric-cyan .metric-value { color: #22D3EE; }
    .metric-yellow .metric-value { color: #FACC15; }
    .metric-red .metric-value { color: #EF4444; }
    .metric-blue { color: #1687FF; }
    .metric-green { color: #22C55E; }
    .metric-purple { color: #A855F7; }
    .metric-cyan { color: #22D3EE; }
    .metric-yellow { color: #FACC15; }
    .metric-red { color: #EF4444; }

    .reference-grid {
        width: min(100%, 1180px);
        margin: 0 auto 0.9rem;
        display: grid;
        grid-template-columns: minmax(0, 1.55fr) minmax(280px, 0.9fr);
        gap: 0.85rem;
    }

    .dashboard-panel {
        border-radius: 8px;
        background: linear-gradient(180deg, rgba(8, 18, 31, 0.92), rgba(4, 11, 20, 0.9));
        border: 1px solid rgba(148, 163, 184, 0.18);
        box-shadow: 0 14px 34px rgba(0, 0, 0, 0.24);
        padding: 0.95rem 1rem;
        overflow: hidden;
    }

    .performance-panel {
        grid-row: span 2;
    }

    .panel-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 1rem;
        margin-bottom: 0.75rem;
    }

    .panel-header span {
        color: #F8FAFC;
        text-transform: uppercase;
        font-size: 0.78rem;
        letter-spacing: 0.06em;
        font-weight: 600;
    }

    .performance-chart {
        width: 100%;
        height: 240px;
        border-bottom: 1px solid rgba(148, 163, 184, 0.12);
        background:
            linear-gradient(rgba(148, 163, 184, 0.08) 1px, transparent 1px),
            linear-gradient(90deg, rgba(148, 163, 184, 0.08) 1px, transparent 1px);
        background-size: 100% 25%, 16.66% 100%;
    }

    .performance-stats {
        display: grid;
        grid-template-columns: repeat(5, minmax(88px, 1fr));
        gap: 0;
        padding-top: 0.72rem;
        overflow-x: auto;
    }

    .performance-stats div {
        min-width: 0;
        padding: 0 0.7rem;
        border-left: 1px solid rgba(148, 163, 184, 0.16);
    }

    .performance-stats div:first-child {
        border-left: 0;
    }

    .performance-stats span,
    .risk-list span {
        display: block;
        color: #AAB6C5;
        font-size: clamp(0.58rem, 0.78vw, 0.68rem);
        text-transform: uppercase;
        letter-spacing: 0.07em;
        margin-bottom: 0.3rem;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    .performance-stats strong {
        display: block;
        font-size: clamp(1rem, 1.45vw, 1.18rem);
        font-weight: 600;
        white-space: nowrap;
        line-height: 1.15;
    }

    .positive { color: #22C55E !important; }
    .negative { color: #EF4444 !important; }
    .blue { color: #1687FF !important; }
    .purple { color: #A855F7 !important; }
    .yellow { color: #FACC15 !important; }
    .cyan { color: #22D3EE !important; }

    .allocation-body {
        display: grid;
        grid-template-columns: minmax(112px, 132px) minmax(0, 1fr);
        align-items: center;
        gap: 0.85rem;
    }

    .allocation-ring {
        width: clamp(112px, 11vw, 132px);
        height: clamp(112px, 11vw, 132px);
        border-radius: 999px;
        background: conic-gradient(#1687FF 0 40%, #23C7C9 40% 100%);
        display: grid;
        place-items: center;
        position: relative;
        color: #FFFFFF;
        font-size: 0.8rem;
    }

    .allocation-ring::after {
        content: "";
        width: 58px;
        height: 58px;
        border-radius: 999px;
        background: #06111D;
        position: absolute;
    }

    .allocation-ring span {
        position: relative;
        z-index: 1;
    }

    .allocation-legend {
        display: grid;
        gap: 0.95rem;
        min-width: 0;
    }

    .allocation-legend div,
    .risk-list div {
        display: grid;
        grid-template-columns: auto minmax(0, 1fr) auto;
        gap: 0.48rem;
        align-items: center;
        color: #D6DEE9;
        font-size: clamp(0.76rem, 0.95vw, 0.85rem);
        min-width: 0;
        white-space: nowrap;
    }

    .allocation-legend strong,
    .risk-list strong {
        white-space: nowrap;
        justify-self: end;
    }

    .allocation-legend i {
        width: 0.72rem;
        height: 0.72rem;
        border-radius: 999px;
    }

    .blue-dot { background: #1687FF; }
    .cyan-dot { background: #23C7C9; }

    .risk-list {
        display: grid;
        gap: 0.55rem;
    }

    .risk-list div {
        grid-template-columns: 1fr auto;
        padding-bottom: 0.42rem;
        border-bottom: 1px solid rgba(148, 163, 184, 0.10);
    }

    .risk-list span {
        display: inline-flex;
        align-items: center;
        gap: 0.42rem;
    }

    .risk-dot {
        width: 0.48rem;
        height: 0.48rem;
        border-radius: 999px;
        display: inline-block;
        flex: 0 0 auto;
    }

    .red-dot { background: rgba(239, 68, 68, 0.72); }
    .slate-dot { background: rgba(148, 163, 184, 0.72); }
    .yellow-dot { background: rgba(250, 204, 21, 0.82); }

    .risk-list div:last-child {
        border-bottom: 0;
        padding-bottom: 0;
    }

    .conclusion-panel p,
    .insight-panel li {
        color: #C6D0DD;
        font-size: 0.82rem;
        line-height: 1.55;
    }

    .insight-panel ul {
        display: grid;
        gap: 0.64rem;
        padding-left: 1.1rem;
        margin: 0;
    }

    @media (max-width: 1100px) {
        .top-shell,
        .reference-grid {
            grid-template-columns: 1fr;
        }

        .top-meta,
        .top-actions {
            display: none;
        }

        .performance-stats {
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 0.8rem;
        }
    }

    div[data-testid="stMetric"] {
        border: 1px solid rgba(148, 163, 184, 0.15);
        padding: 0.95rem;
        border-radius: 8px;
        background:
            linear-gradient(180deg, rgba(15, 23, 42, 0.92), rgba(8, 13, 24, 0.88));
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.27);
    }

    div[data-testid="stMetric"] label {
        color: #94A3B8 !important;
        text-transform: uppercase;
        letter-spacing: 0.16em;
        font-weight: 500;
    }

    div[data-testid="stMetricValue"] {
        color: #F9FAFB !important;
        font-weight: 540;
        letter-spacing: 0.004em;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-color: rgba(148, 163, 184, 0.14) !important;
        border-radius: 8px !important;
        background:
            linear-gradient(180deg, rgba(15, 23, 42, 0.84), rgba(8, 13, 24, 0.78));
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.24);
    }

    div[data-testid="stDataFrame"] {
        border-radius: 8px;
        overflow: hidden;
        border: 1px solid rgba(148, 163, 184, 0.16);
        background: #0B1220 !important;
        color: #D6DEE9 !important;
        font-size: 0.82rem !important;
    }

    div[data-testid="stDataFrame"] div {
        background-color: transparent !important;
        color: #D6DEE9 !important;
    }

    div[data-testid="stDataFrame"] [role="grid"],
    div[data-testid="stDataFrame"] [data-testid="stTable"],
    div[data-testid="stDataFrame"] canvas {
        background-color: #0B1220 !important;
        color: #D6DEE9 !important;
    }

    div[data-testid="stDataFrame"] [role="columnheader"],
    div[data-testid="stDataFrame"] [role="rowheader"] {
        background-color: #101827 !important;
        color: #E5E7EB !important;
        font-weight: 500 !important;
    }

    div[data-testid="stDataFrame"] [role="gridcell"] {
        background-color: #0B1220 !important;
        color: #D6DEE9 !important;
    }

    div[data-testid="stTable"],
    div[data-testid="stTable"] table,
    div[data-testid="stTable"] thead,
    div[data-testid="stTable"] tbody,
    div[data-testid="stTable"] tr,
    div[data-testid="stTable"] th,
    div[data-testid="stTable"] td {
        background-color: #0B1220 !important;
        color: #D6DEE9 !important;
        border-color: rgba(148, 163, 184, 0.14) !important;
        font-family: 'Geist', 'Inter', 'Segoe UI', sans-serif !important;
    }

    div[data-testid="stTable"] th {
        background-color: #101827 !important;
        color: #E5E7EB !important;
        font-weight: 500 !important;
    }

    div[data-testid="stPlotlyChart"] {
        border: 1px solid rgba(148, 163, 184, 0.14);
        border-radius: 8px;
        padding: 0.45rem;
        background:
            linear-gradient(180deg, rgba(15, 23, 42, 0.78), rgba(8, 13, 24, 0.72));
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.22);
    }

    div[data-testid="stDownloadButton"] button {
        border-radius: 8px;
        min-height: 2.65rem;
        font-weight: 520;
        letter-spacing: 0.01em;
        background: linear-gradient(135deg, #1D4ED8, #0891B2);
        color: white;
        border: 1px solid rgba(56, 189, 248, 0.42);
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 0.4rem;
        background: rgba(5, 10, 20, 0.75);
        border: 1px solid rgba(148, 163, 184, 0.14);
        border-radius: 8px;
        padding: 0.35rem;
        margin-bottom: 1rem;
    }

    .stTabs [data-baseweb="tab"] {
        height: 40px;
        border-radius: 7px;
        color: #CBD5E1;
        font-weight: 430;
        letter-spacing: 0.01em;
        padding: 0 0.9rem;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(29, 78, 216, 0.88), rgba(8, 145, 178, 0.78));
        color: #FFFFFF !important;
        font-weight: 520 !important;
        box-shadow: 0 8px 20px rgba(14, 165, 233, 0.18);
    }

    .stAlert {
        border-radius: 8px;
        border: 1px solid rgba(148, 163, 184, 0.18);
    }

    hr {
        border-color: rgba(148, 163, 184, 0.12);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.sidebar.markdown(
    """
    <div class="sidebar-brand">
        <div>
            <div class="sidebar-title">Portfolio</div>
            <div class="sidebar-kicker">Optimizer</div>
        </div>
        <div class="live-pill">Live</div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.sidebar.markdown("---")
st.sidebar.subheader("Optimizer Inputs")

input_tickers = st.sidebar.text_input(
    "Tickers",
    value="AAPL, MSFT, GOOGL, AMZN",
    help="Enter comma-separated ticker symbols.",
)

input_start_date = st.sidebar.date_input(
    "Start Date",
    value=date(2020, 1, 1),
)

input_end_date = st.sidebar.date_input(
    "End Date",
    value=date(2024, 1, 1),
)

input_risk_free_rate = st.sidebar.number_input(
    "Risk-Free Rate",
    min_value=0.0,
    max_value=0.20,
    value=0.02,
    step=0.005,
    format="%.3f",
    help="Use decimal format. Example: 0.02 = 2%.",
)

input_min_weight = st.sidebar.number_input(
    "Minimum Asset Weight",
    min_value=0.0,
    max_value=1.0,
    value=0.0,
    step=0.05,
    format="%.2f",
)

input_max_weight = st.sidebar.number_input(
    "Maximum Asset Weight",
    min_value=0.0,
    max_value=1.0,
    value=0.60,
    step=0.05,
    format="%.2f",
)

input_portfolio_value = st.sidebar.number_input(
    "Portfolio Value",
    min_value=1_000.0,
    max_value=1_000_000_000.0,
    value=1_000_000.0,
    step=50_000.0,
    format="%.2f",
)

input_monte_carlo_portfolios = st.sidebar.number_input(
    "Monte Carlo Portfolios",
    min_value=500,
    max_value=25_000,
    value=5_000,
    step=500,
    format="%d",
)

run_optimizer_button = st.sidebar.button(
    "Run Portfolio Optimizer",
    type="primary",
    use_container_width=True,
)

st.sidebar.markdown("---")
st.sidebar.subheader("Mode")

if st.session_state["live_results"] is not None:
    st.sidebar.success("Live mode active")
else:
    st.sidebar.info("Export fallback")

st.sidebar.markdown("---")
st.sidebar.subheader("Selected Inputs")
st.sidebar.caption(f"Tickers: {input_tickers}")
st.sidebar.caption(f"Dates: {input_start_date} to {input_end_date}")
st.sidebar.caption(f"Risk-free rate: {input_risk_free_rate:.2%}")
st.sidebar.caption(f"Weights: {input_min_weight:.0%} to {input_max_weight:.0%}")
st.sidebar.caption(f"Value: ${input_portfolio_value:,.0f}")
st.sidebar.caption(f"Simulations: {input_monte_carlo_portfolios:,}")

st.sidebar.markdown("---")
st.sidebar.markdown(
    """
    <div class="nav-group">
        <div class="nav-heading">Analytics</div>
        <div class="nav-item active"><span class="nav-dot"></span>Overview</div>
        <div class="nav-item"><span class="nav-dot"></span>Portfolio Optimization</div>
        <div class="nav-item"><span class="nav-dot"></span>Efficient Frontier</div>
        <div class="nav-item"><span class="nav-dot"></span>Allocation Analysis</div>
        <div class="nav-item"><span class="nav-dot"></span>Return Analytics</div>
        <div class="nav-item"><span class="nav-dot"></span>Risk Analytics</div>
        <div class="nav-item"><span class="nav-dot"></span>Backtesting</div>
        <div class="nav-heading">Research & Intelligence</div>
        <div class="nav-item"><span class="nav-dot"></span>Regimes & Forecasts</div>
        <div class="nav-item"><span class="nav-dot"></span>Strategy Research</div>
        <div class="nav-item"><span class="nav-dot"></span>Research Platform</div>
        <div class="nav-heading">System</div>
        <div class="nav-item"><span class="nav-dot"></span>Settings</div>
        <div class="nav-item"><span class="nav-dot"></span>Documentation</div>
        <div class="sidebar-live-card">
            <div><span></span>Live mode active</div>
            <p>Results update from your selected portfolio.</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

if run_optimizer_button:
    try:
        with st.spinner("Running live portfolio optimizer..."):
            live_results = run_portfolio_optimizer(
                tickers=input_tickers,
                start_date=str(input_start_date),
                end_date=str(input_end_date),
                risk_free_rate=input_risk_free_rate,
                min_weight=input_min_weight,
                max_weight=input_max_weight,
                portfolio_value=input_portfolio_value,
                monte_carlo_portfolios=int(input_monte_carlo_portfolios),
            )

            live_portfolio_results = build_live_portfolio_results(
                live_results
            )

            st.session_state["live_results"] = live_results
            st.session_state["live_portfolio_results"] = (
                live_portfolio_results
            )

        st.success("Live portfolio optimization completed successfully.")

    except Exception as error:
        st.session_state["live_results"] = None
        st.session_state["live_portfolio_results"] = pd.DataFrame()

        st.error("The live optimizer could not complete.")
        st.exception(error)

final_report = load_csv(CSV_FILES["Final Research Report"])
research_dashboard = load_csv(CSV_FILES["Research Master Dashboard"])
portfolio_results_export = load_csv(CSV_FILES["Portfolio Results"])
backtest_results = load_csv(CSV_FILES["Backtest Results"])
performance_summary = load_csv(CSV_FILES["Performance Summary"])
risk_dashboard = load_csv(CSV_FILES["Risk Dashboard"])
risk_governance = load_csv(CSV_FILES["Risk Governance Report"])
strategy_summary = load_csv(CSV_FILES["Strategy Summary"])
strategy_comparison = load_csv(CSV_FILES["Strategy Comparison"])
robustness_dashboard = load_csv(CSV_FILES["Robustness Dashboard"])
market_regime_summary = load_csv(CSV_FILES["Market Regime Summary"])
regime_attribution = load_csv(CSV_FILES["Regime Attribution"])
expected_return_forecasts = load_csv(CSV_FILES["Expected Return Forecasts"])
forecast_evaluation = load_csv(CSV_FILES["Forecast Evaluation"])
regime_forecast_dashboard = load_csv(
    CSV_FILES["Regime Forecast Dashboard"]
)
regime_strategy_dashboard = load_csv(
    CSV_FILES["Regime Strategy Dashboard"]
)
value_at_risk_summary = load_csv(CSV_FILES["Value-at-Risk Summary"])
stress_test_results = load_csv(CSV_FILES["Stress Test Results"])
scenario_analysis = load_csv(CSV_FILES["Scenario Analysis"])
market_shock_analysis = load_csv(CSV_FILES["Market Shock Analysis"])
concentration_summary = load_csv(CSV_FILES["Concentration Summary"])
tail_risk_summary = load_csv(CSV_FILES["Tail Risk Summary"])

if not st.session_state["live_portfolio_results"].empty:
    portfolio_results = st.session_state["live_portfolio_results"]
else:
    portfolio_results = portfolio_results_export

show_top_bar()

st.markdown(
    """
        <div class="hero-card">
            <div class="section-label">Institutional Research Platform</div>
            <div class="hero-title">Portfolio Optimizer</div>
            <div class="hero-subtitle">
            Live portfolio intelligence for optimization, risk analysis, backtesting,
            regime research, and investment reporting.
            </div>
        </div>
    """,
    unsafe_allow_html=True,
)

show_status_banner(st.session_state["live_results"] is not None)


def show_universe_context_panel(live_results):
    if live_results is None:
        return

    universe_metadata = live_results.get("universe_metadata", {})

    universe_type = universe_metadata.get(
        "universe_type",
        "Live Portfolio",
    )

    universe_message = universe_metadata.get(
        "universe_message",
        "Live results reflect the selected portfolio.",
    )

    selected_universe = universe_metadata.get("selected_universe", [])

    with st.container(border=True):
        st.markdown(f"#### {prettify_display_text(universe_type)}")
        st.write(prettify_display_text(universe_message))

        if selected_universe:
            st.caption(
                "Current live portfolio: "
                + ", ".join(selected_universe)
            )


show_universe_context_panel(st.session_state["live_results"])

tabs = st.tabs(
    [
        "Executive Overview",
        "Optimization",
        "Backtesting",
        "Risk",
        "Strategies",
        "Regimes & Forecasts",
        "Research Platform",
        "Downloads",
    ]
)

with tabs[0]:
    overview_expected_return = 0.0
    overview_total_return = 0.0
    overview_volatility = 0.0
    overview_sharpe = 0.0
    overview_drawdown = 0.0
    overview_regime = "Unknown"
    overview_model = "Momentum"

    if st.session_state["live_results"] is not None:
        live_results = st.session_state["live_results"]
        max_sharpe = live_results["max_sharpe_summary"]
        latest_regime = live_results.get("latest_market_regime", {})
        adaptive_model = get_first_value(
            live_results.get("adaptive_forecast_recommendation", pd.DataFrame()),
            "recommended_forecast_model",
            "Not Available",
        )
        live_backtest = live_results.get("live_backtest_table", pd.DataFrame())
        overview_expected_return = max_sharpe.get("return", 0.0)
        overview_total_return = get_first_value(
            live_backtest,
            "total_return",
            overview_expected_return,
        )
        overview_volatility = max_sharpe.get("volatility", 0.0)
        overview_sharpe = max_sharpe.get("sharpe_ratio", 0.0)
        overview_drawdown = get_first_value(
            live_backtest,
            "max_drawdown",
            latest_regime.get("drawdown", 0.0),
        )
        overview_regime = latest_regime.get("market_regime", "Unknown")
        overview_model = adaptive_model

        overview_columns = st.columns(5)

        with overview_columns[0]:
            show_metric_card(
                "Expected Return",
                f"{max_sharpe['return']:.2%}",
                "Optimized Max Sharpe",
                "green",
            )

        with overview_columns[1]:
            show_metric_card(
                "Expected Volatility",
                f"{max_sharpe['volatility']:.2%}",
                "Optimized Max Sharpe",
                "blue",
            )

        with overview_columns[2]:
            show_metric_card(
                "Sharpe Ratio",
                f"{max_sharpe['sharpe_ratio']:.3f}",
                "Risk-Adjusted Return",
                "purple",
            )

        with overview_columns[3]:
            show_metric_card(
                "Current Regime",
                str(latest_regime.get("market_regime", "Unknown")),
                "Market Regime",
                "yellow",
            )

        with overview_columns[4]:
            show_metric_card(
                "Adaptive Model",
                str(adaptive_model),
                "Recommended Forecast",
                "cyan",
            )

    elif not backtest_results.empty:
        optimized_backtest = backtest_results.iloc[0]
        overview_expected_return = optimized_backtest.get("annualized_return", 0.0)
        overview_total_return = optimized_backtest.get(
            "total_return",
            overview_expected_return,
        )
        overview_volatility = optimized_backtest.get("annualized_volatility", 0.0)
        overview_sharpe = optimized_backtest.get("sharpe_ratio", 0.0)
        overview_drawdown = optimized_backtest.get("max_drawdown", 0.0)

        overview_columns = st.columns(4)

        with overview_columns[0]:
            show_metric_card(
                "Annualized Return",
                f"{optimized_backtest['annualized_return']:.2%}",
                "Research Baseline",
                "green",
            )

        with overview_columns[1]:
            show_metric_card(
                "Annualized Volatility",
                f"{optimized_backtest['annualized_volatility']:.2%}",
                "Research Baseline",
                "blue",
            )

        with overview_columns[2]:
            show_metric_card(
                "Sharpe Ratio",
                f"{optimized_backtest['sharpe_ratio']:.3f}",
                "Research Baseline",
                "purple",
            )

        with overview_columns[3]:
            show_metric_card(
                "Maximum Drawdown",
                f"{optimized_backtest['max_drawdown']:.2%}",
                "Research Baseline",
                "red",
            )

    show_reference_overview(
        expected_return=overview_expected_return,
        total_return=overview_total_return,
        volatility=overview_volatility,
        sharpe_ratio=overview_sharpe,
        max_drawdown=overview_drawdown,
        regime=overview_regime,
        adaptive_model=overview_model,
    )

    show_dataframe("Final Institutional Research Report", final_report)
    show_dataframe("Research Master Dashboard", research_dashboard)
    show_dataframe("Performance Summary", performance_summary)

with tabs[1]:
    st.header("Portfolio Optimization")
    show_section_intro(
        "Optimization Engine",
        "Portfolio Construction",
        "Compare risk-return profiles, Sharpe ratios, volatility, and allocations.",
    )

    if portfolio_results.empty:
        st.warning("Portfolio optimization results are not available yet.")
    else:
        best_sharpe_row = portfolio_results.loc[
            portfolio_results["sharpe_ratio"].idxmax()
        ]

        lowest_volatility_row = portfolio_results.loc[
            portfolio_results["volatility"].idxmin()
        ]

        optimization_metrics = st.columns(4)

        with optimization_metrics[0]:
            show_metric_card(
                "Best Sharpe Portfolio",
                best_sharpe_row["portfolio"],
                "Highest Sharpe Ratio",
                "purple",
            )

        with optimization_metrics[1]:
            show_metric_card(
                "Best Sharpe Ratio",
                f"{best_sharpe_row['sharpe_ratio']:.3f}",
                "Risk-Adjusted Return",
                "purple",
            )

        with optimization_metrics[2]:
            show_metric_card(
                "Minimum Volatility Portfolio",
                lowest_volatility_row["portfolio"],
                "Lowest Expected Risk",
                "blue",
            )

        with optimization_metrics[3]:
            show_metric_card(
                "Minimum Volatility",
                f"{lowest_volatility_row['volatility']:.2%}",
                "Annualized Volatility",
                "blue",
            )

        chart_column_1, chart_column_2 = st.columns(2)

        with chart_column_1:
            st.plotly_chart(
                create_risk_return_chart(portfolio_results),
                use_container_width=True,
                key="optimization_risk_return_chart",
            )

        with chart_column_2:
            st.plotly_chart(
                create_sharpe_chart(portfolio_results),
                use_container_width=True,
                key="optimization_sharpe_chart",
            )

        st.plotly_chart(
            create_return_volatility_chart(portfolio_results),
            use_container_width=True,
            key="optimization_return_volatility_chart",
        )

        st.subheader("Portfolio Allocation")

        selected_portfolio, allocation_figure = (
            create_portfolio_allocation_chart(portfolio_results)
        )

        if allocation_figure is not None:
            allocation_column_1, allocation_column_2 = st.columns([1.2, 1])

            with allocation_column_1:
                st.plotly_chart(
                    allocation_figure,
                    use_container_width=True,
                )

            with allocation_column_2:
                selected_data = portfolio_results.loc[
                    portfolio_results["portfolio"] == selected_portfolio
                ]

                st.markdown("#### Selected Portfolio Metrics")

                if not selected_data.empty:
                    selected_row = selected_data.iloc[0]

                    show_metric_card(
                        "Expected Return",
                        f"{selected_row['return']:.2%}",
                        selected_portfolio,
                        "green",
                    )

                    show_metric_card(
                        "Volatility",
                        f"{selected_row['volatility']:.2%}",
                        selected_portfolio,
                        "blue",
                    )

                    show_metric_card(
                        "Sharpe Ratio",
                        f"{selected_row['sharpe_ratio']:.3f}",
                        selected_portfolio,
                        "purple",
                    )

        show_dataframe("Portfolio Optimization Results", portfolio_results)

with tabs[2]:
    st.header("Backtesting")

    if st.session_state["live_results"] is not None:
        live_results = st.session_state["live_results"]
        live_backtest_results = live_results.get(
            "live_backtest_table",
            pd.DataFrame(),
        )

        if live_backtest_results.empty:
            st.warning("Live backtest results are not available yet.")
        else:
            st.info(
                "Showing live backtest results for the selected portfolio."
            )

            backtest_chart_column_1, backtest_chart_column_2 = st.columns(2)

            with backtest_chart_column_1:
                st.plotly_chart(
                    create_backtest_return_chart(live_backtest_results),
                    use_container_width=True,
                    key="live_backtest_return_chart",
                )

            with backtest_chart_column_2:
                st.plotly_chart(
                    create_backtest_sharpe_chart(live_backtest_results),
                    use_container_width=True,
                    key="live_backtest_sharpe_chart",
                )

            backtest_chart_column_3, backtest_chart_column_4 = st.columns(2)

            with backtest_chart_column_3:
                st.plotly_chart(
                    create_backtest_drawdown_chart(live_backtest_results),
                    use_container_width=True,
                    key="live_backtest_drawdown_chart",
                )

            with backtest_chart_column_4:
                st.plotly_chart(
                    create_backtest_risk_return_chart(live_backtest_results),
                    use_container_width=True,
                    key="live_backtest_risk_return_chart",
                )

            show_dataframe("Live Backtest Results", live_backtest_results)

    else:
        if backtest_results.empty:
            st.warning("Backtest results are not available yet.")
        else:
            backtest_chart_column_1, backtest_chart_column_2 = st.columns(2)

            with backtest_chart_column_1:
                st.plotly_chart(
                    create_backtest_return_chart(backtest_results),
                    use_container_width=True,
                    key="backtest_return_chart",
                )

            with backtest_chart_column_2:
                st.plotly_chart(
                    create_backtest_sharpe_chart(backtest_results),
                    use_container_width=True,
                    key="backtest_sharpe_chart",
                )

            backtest_chart_column_3, backtest_chart_column_4 = st.columns(2)

            with backtest_chart_column_3:
                st.plotly_chart(
                    create_backtest_drawdown_chart(backtest_results),
                    use_container_width=True,
                    key="backtest_drawdown_chart",
                )

            with backtest_chart_column_4:
                st.plotly_chart(
                    create_backtest_risk_return_chart(backtest_results),
                    use_container_width=True,
                    key="backtest_risk_return_chart",
                )

            show_dataframe("Backtest Results", backtest_results)

with tabs[3]:
    st.header("Risk Management")

    if st.session_state["live_results"] is not None:
        live_results = st.session_state["live_results"]

        st.info(
            "Showing live risk analytics for the selected portfolio."
        )

        show_dataframe(
            "Live Institutional Risk Dashboard",
            live_results.get("live_risk_dashboard_table", pd.DataFrame()),
        )

        show_dataframe(
            "Live Value-at-Risk and CVaR Summary",
            live_results.get("value_at_risk_summary", pd.DataFrame()),
        )

        show_dataframe(
            "Live Drawdown Summary",
            live_results.get("live_drawdown_table", pd.DataFrame()),
        )

        show_dataframe(
            "Live Historical Stress Test Results",
            live_results.get("stress_test_results", pd.DataFrame()),
        )

        show_dataframe(
            "Live Market Shock Analysis",
            live_results.get("market_shock_analysis", pd.DataFrame()),
        )

        show_dataframe(
            "Live Concentration Risk Summary",
            live_results.get("live_concentration_table", pd.DataFrame()),
        )

        show_dataframe(
            "Live Tail Risk Summary",
            live_results.get("live_tail_risk_table", pd.DataFrame()),
        )

    else:
        show_dataframe("Institutional Risk Dashboard", risk_dashboard)
        show_dataframe("Risk Governance Report", risk_governance)
        show_dataframe("Value-at-Risk and CVaR Summary", value_at_risk_summary)
        show_dataframe("Historical Stress Test Results", stress_test_results)
        show_dataframe("Scenario Analysis", scenario_analysis)
        show_dataframe("Market Shock Analysis", market_shock_analysis)
        show_dataframe("Concentration Risk Summary", concentration_summary)
        show_dataframe("Tail Risk Summary", tail_risk_summary)

with tabs[4]:
    st.header("Strategy Research Laboratory")

    if st.session_state["live_results"] is not None:
        live_strategy_summary = create_live_strategy_summary(
            st.session_state["live_results"]
        )

        show_dataframe(
            "Live Strategy Summary",
            live_strategy_summary,
        )

        st.info(
            "Showing live strategy results for the selected portfolio."
        )

    else:
        show_dataframe("Strategy Summary", strategy_summary)
        show_dataframe("Strategy Comparison", strategy_comparison)
        show_dataframe("Robustness Dashboard", robustness_dashboard)

with tabs[5]:
    st.header("Regime & Forecast Research")

    show_section_intro(
        "Market Intelligence",
        "Regimes and Forecasts",
        "Review regime detection, return forecasts, model accuracy, and recommendations.",
    )

    if st.session_state["live_results"] is not None:
        live_results = st.session_state["live_results"]

        st.info(
            "Showing live regime and forecast research for the selected portfolio."
        )

        latest_market_regime = live_results.get("latest_market_regime")

        if latest_market_regime:
            regime_metric_columns = st.columns(4)

            with regime_metric_columns[0]:
                show_metric_card(
                    "Current Regime",
                    str(latest_market_regime.get("market_regime", "Unknown")),
                    "Latest Market Regime",
                    "yellow",
                )

            with regime_metric_columns[1]:
                show_metric_card(
                    "Rolling Return",
                    f"{latest_market_regime.get('rolling_return', 0.0):.2%}",
                    "Regime Window Return",
                    "green",
                )

            with regime_metric_columns[2]:
                show_metric_card(
                    "Rolling Volatility",
                    f"{latest_market_regime.get('rolling_volatility', 0.0):.2%}",
                    "Annualized Volatility",
                    "blue",
                )

            with regime_metric_columns[3]:
                show_metric_card(
                    "Current Drawdown",
                    f"{latest_market_regime.get('drawdown', 0.0):.2%}",
                    "Portfolio Drawdown",
                    "red",
                )

        show_dataframe(
            "Live Market Regime Summary",
            live_results.get("market_regime_summary", pd.DataFrame()),
        )

        show_dataframe(
            "Live Regime Attribution",
            live_results.get("regime_attribution", pd.DataFrame()),
        )

        show_dataframe(
            "Live Expected Return Forecasts",
            live_results.get("expected_return_forecasts", pd.DataFrame()),
        )

        show_dataframe(
            "Live Forecast Evaluation",
            live_results.get("forecast_evaluation", pd.DataFrame()),
        )

        show_dataframe(
            "Live Forecast Evaluation Summary",
            live_results.get("forecast_evaluation_summary", pd.DataFrame()),
        )

        show_dataframe(
            "Live Forecast Accuracy by Regime",
            live_results.get("regime_forecast_summary", pd.DataFrame()),
        )

        show_dataframe(
            "Live Forecast Model Evaluation",
            live_results.get("forecast_model_evaluation", pd.DataFrame()),
        )

        show_dataframe(
            "Live Adaptive Forecast Recommendation",
            live_results.get("adaptive_forecast_recommendation", pd.DataFrame()),
        )

        show_dataframe(
            "Live Regime Forecast Dashboard",
            live_results.get("regime_forecast_dashboard", pd.DataFrame()),
        )

        show_dataframe(
            "Live Regime Strategy Dashboard",
            live_results.get("regime_strategy_dashboard", pd.DataFrame()),
        )

    else:
        show_dataframe("Market Regime Summary", market_regime_summary)
        show_dataframe("Regime Attribution", regime_attribution)
        show_dataframe("Expected Return Forecasts", expected_return_forecasts)
        show_dataframe("Forecast Evaluation", forecast_evaluation)
        show_dataframe("Regime Forecast Dashboard", regime_forecast_dashboard)
        show_dataframe("Regime Strategy Dashboard", regime_strategy_dashboard)

with tabs[6]:
    st.header("Research Platform")

    show_section_intro(
        "Institutional Research",
        "Research Platform",
        "Review optimization, risk, backtest, regime, and forecast conclusions.",
    )

    if st.session_state["live_results"] is not None:
        live_results = st.session_state["live_results"]

        st.info(
            "Showing a live research summary for the selected portfolio."
        )

        live_research_summary = create_live_research_summary(live_results)

        st.subheader("Live Executive Conclusion")
        with st.container(border=True):
            st.write(create_live_executive_conclusion(live_results))

        show_dataframe(
            "Live Institutional Research Summary",
            live_research_summary,
        )

        show_dataframe(
            "Live Key Portfolio Statistics",
            live_results.get("portfolio_results_table", pd.DataFrame()),
        )

        show_dataframe(
            "Live Risk Conclusions",
            live_results.get("live_risk_dashboard_table", pd.DataFrame()),
        )

        show_dataframe(
            "Live Backtest Conclusions",
            live_results.get("live_backtest_table", pd.DataFrame()),
        )

        show_dataframe(
            "Live Regime and Forecast Conclusions",
            live_results.get("regime_forecast_dashboard", pd.DataFrame()),
        )

    else:
        show_dataframe("Research Master Dashboard", research_dashboard)
        show_dataframe("Final Institutional Research Report", final_report)

with tabs[7]:
    st.header("Export Center")

    st.markdown(
        """
        Download available research outputs. Missing files stay hidden.
        """
    )

    available_files = [
        (title, file_name)
        for title, file_name in CSV_FILES.items()
        if os.path.exists(os.path.join(EXPORTS_FOLDER, file_name))
    ]

    if not available_files:
        st.warning(
            "No saved research outputs are available. Run a full research "
            "refresh first."
        )
    else:
        download_columns = st.columns(2)

        for index, (title, file_name) in enumerate(available_files):
            with download_columns[index % 2]:
                show_download_button(title, file_name)

show_footer()
