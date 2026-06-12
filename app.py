import os
from datetime import date

import pandas as pd
import plotly.express as px
import streamlit as st

from src.app_pipeline import run_portfolio_optimizer
from styles import APP_CSS
from data import EXPORTS_FOLDER, CSV_FILES, load_csv
from formatting import (
    prettify_label,
    prettify_value,
    prettify_display_text,
    format_percent_value,
    format_number_value,
    prettify_chart_categories,
    prettify_dataframe,
)
from charts import (
    format_percentage_axis,
    configure_chart,
    create_risk_return_chart,
    create_sharpe_chart,
    create_return_volatility_chart,
    create_backtest_return_chart,
    create_backtest_sharpe_chart,
    create_backtest_drawdown_chart,
    create_backtest_risk_return_chart,
    build_growth_curve_chart,
)


def show_dataframe(title, dataframe):
    with st.container(border=True):
        st.subheader(title)

        if dataframe is None or dataframe.empty:
            st.warning(f"{title} is not available yet.")
        else:
            display_dataframe = prettify_dataframe(dataframe)
            st.dataframe(
                display_dataframe,
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
    current_regime = "Unknown"

    live_results = st.session_state.get("live_results")
    if live_results is not None:
        current_regime = live_results.get(
            "latest_market_regime",
            {},
        ).get("market_regime", "Unknown")
    elif not market_regime_summary.empty:
        regime_column = next(
            (
                column
                for column in market_regime_summary.columns
                if column.lower() in {"market_regime", "regime"}
            ),
            None,
        )
        if regime_column is not None:
            current_regime = market_regime_summary.iloc[-1].get(
                regime_column,
                "Unknown",
            )

    live_pill_markup = (
        '<div class="live-pill">Live</div>'
        if st.session_state.get("live_results") is not None
        else ""
    )

    st.markdown(
        f"""
        <div class="top-shell">
            <div class="top-brand">
                <div class="brand-text">
                    <div>Portfolio</div>
                    <div>Optimizer</div>
                </div>{live_pill_markup}
            </div>
            <div class="top-meta">
                <div class="meta-item">
                    <span>Portfolio Universe</span>
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
                <div class="meta-item">
                    <span>Current Regime</span>
                    <strong>{prettify_display_text(current_regime)}</strong>
                </div>
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
    live_results = st.session_state["live_results"]
    conclusion = (
        create_live_executive_conclusion(live_results)
        if live_results is not None
        else create_export_executive_conclusion(
            portfolio_results,
            backtest_results,
            regime_forecast_dashboard,
            input_tickers,
        )
    )
    risk_source = (
        live_results.get("live_risk_dashboard_table", pd.DataFrame())
        if live_results is not None
        else risk_dashboard
    )
    var_source = (
        live_results.get("value_at_risk_summary", pd.DataFrame())
        if live_results is not None
        else value_at_risk_summary
    )
    concentration_source = (
        live_results.get("live_concentration_table", pd.DataFrame())
        if live_results is not None
        else concentration_summary
    )
    tail_source = (
        live_results.get("live_tail_risk_table", pd.DataFrame())
        if live_results is not None
        else tail_risk_summary
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

    growth_curve = (
        live_results.get("portfolio_backtest", {}).get("growth_curve")
        if live_results is not None
        else None
    )
    growth_chart = build_growth_curve_chart(growth_curve)

    if growth_chart is not None:
        performance_chart_markup = f"""
                <svg class="performance-chart" viewBox="0 0 760 250" preserveAspectRatio="none">
                    <defs>
                        <linearGradient id="lineFade" x1="0" y1="0" x2="0" y2="1">
                            <stop offset="0%" stop-color="#1687FF" stop-opacity="0.28"/>
                            <stop offset="100%" stop-color="#1687FF" stop-opacity="0"/>
                        </linearGradient>
                    </defs>
                    <path d="{growth_chart['area_path']}" fill="url(#lineFade)"/>
                    <polyline points="{growth_chart['polyline']}" fill="none" stroke="#1687FF" stroke-width="3"/>
                    <circle cx="{growth_chart['last_x']}" cy="{growth_chart['last_y']}" r="6" fill="#1687FF"/>
                </svg>"""
    else:
        performance_chart_markup = """
                <div class="performance-chart performance-chart-placeholder">
                    <span>Run the live optimizer to view the portfolio performance chart.</span>
                </div>"""

    allocation_colors = ["#1687FF", "#23C7C9", "#7B8AA0"]
    allocation_dot_classes = ["blue-dot", "cyan-dot", "slate-dot"]
    allocation_breakdown = get_allocation_breakdown(portfolio_results)

    if allocation_breakdown:
        cumulative_weight = 0.0
        gradient_segments = []
        legend_rows = []

        for index, (label, weight) in enumerate(allocation_breakdown):
            color = allocation_colors[min(index, len(allocation_colors) - 1)]
            dot_class = allocation_dot_classes[min(index, len(allocation_dot_classes) - 1)]
            start_pct = cumulative_weight * 100
            cumulative_weight = min(cumulative_weight + weight, 1.0)
            end_pct = cumulative_weight * 100

            gradient_segments.append(f"{color} {start_pct:.2f}% {end_pct:.2f}%")
            legend_rows.append(
                f'<div><i class="{dot_class}"></i>{prettify_display_text(label)}'
                f'<strong>{weight:.1%}</strong></div>'
            )

        allocation_gradient = ", ".join(gradient_segments)
        allocation_top_label = f"{allocation_breakdown[0][1]:.1%}"
        allocation_legend_markup = "".join(legend_rows)
    else:
        allocation_gradient = "rgba(148, 163, 184, 0.18) 0% 100%"
        allocation_top_label = "N/A"
        allocation_legend_markup = (
            '<div><i class="slate-dot"></i>Allocation Pending<strong>N/A</strong></div>'
        )

    st.markdown(
        f"""
        <div class="reference-grid">
            <div class="dashboard-panel performance-panel">
                <div class="panel-header">
                    <span>Live Portfolio Performance</span>
                </div>{performance_chart_markup}
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
                    <div class="allocation-ring" style="background: conic-gradient({allocation_gradient});"><span>{allocation_top_label}</span></div>
                    <div class="allocation-legend">
                        {allocation_legend_markup}
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
    caption_markup = (
        f'<div class="metric-caption">{display_caption}</div>'
        if display_caption
        else ""
    )

    st.markdown(
        f"""
        <div class="metric-card metric-{accent}">
            <div class="metric-label">{display_label}</div>
            <div class="metric-value">{display_value}</div>
            {caption_markup}
        </div>
        """,
        unsafe_allow_html=True,
    )


def show_footer():
    st.markdown("---")
    st.caption(
        "Portfolio Optimizer | Interactive Research Dashboard"
    )


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


def render_backtest_charts(backtest_data, key_prefix):
    chart_column_1, chart_column_2 = st.columns(2)

    with chart_column_1:
        st.plotly_chart(
            create_backtest_return_chart(backtest_data),
            use_container_width=True,
            key=f"{key_prefix}_return_chart",
        )

    with chart_column_2:
        st.plotly_chart(
            create_backtest_sharpe_chart(backtest_data),
            use_container_width=True,
            key=f"{key_prefix}_sharpe_chart",
        )

    chart_column_3, chart_column_4 = st.columns(2)

    with chart_column_3:
        st.plotly_chart(
            create_backtest_drawdown_chart(backtest_data),
            use_container_width=True,
            key=f"{key_prefix}_drawdown_chart",
        )

    with chart_column_4:
        st.plotly_chart(
            create_backtest_risk_return_chart(backtest_data),
            use_container_width=True,
            key=f"{key_prefix}_risk_return_chart",
        )


def get_first_value(dataframe, column, default=None):
    if dataframe is None or dataframe.empty or column not in dataframe.columns:
        return default

    return dataframe[column].iloc[0]


def get_allocation_breakdown(portfolio_results, portfolio_name="Optimized Max Sharpe", max_segments=2):
    if portfolio_results is None or portfolio_results.empty:
        return []

    matches = portfolio_results.loc[portfolio_results["portfolio"] == portfolio_name]
    row = matches.iloc[0] if not matches.empty else portfolio_results.iloc[0]

    identifier_columns = {"portfolio", "return", "volatility", "sharpe_ratio"}
    asset_columns = [
        column for column in portfolio_results.columns if column not in identifier_columns
    ]

    weights = []
    for column in asset_columns:
        value = pd.to_numeric(row.get(column), errors="coerce")
        if value is not None and not pd.isna(value) and value > 1e-8:
            weights.append((column, float(value)))

    weights.sort(key=lambda item: item[1], reverse=True)

    if len(weights) <= max_segments:
        return weights

    top_weights = weights[:max_segments]
    other_weight = sum(weight for _, weight in weights[max_segments:])

    return top_weights + [("Other", other_weight)]


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


def describe_sharpe_ratio(sharpe_ratio):
    if sharpe_ratio >= 1.5:
        return "a strong risk-adjusted profile"
    if sharpe_ratio >= 0.75:
        return "a reasonable risk-adjusted profile"
    if sharpe_ratio >= 0:
        return "a fairly modest risk-adjusted profile"
    return "a risk-adjusted profile that currently looks weak"


def create_live_executive_conclusion(live_results):
    max_sharpe = live_results.get("max_sharpe_summary", {})
    latest_regime = live_results.get("latest_market_regime", {})
    inputs = live_results.get("inputs", {})

    tickers = ", ".join(inputs.get("tickers", []))
    regime = prettify_display_text(
        latest_regime.get("market_regime", "an undetermined regime")
    )
    sharpe_ratio = max_sharpe.get("sharpe_ratio", 0)

    return (
        f"For {tickers}, the max Sharpe portfolio built from this run targets "
        f"a {max_sharpe.get('return', 0):.2%} return against "
        f"{max_sharpe.get('volatility', 0):.2%} volatility, "
        f"putting its Sharpe ratio at {sharpe_ratio:.3f}, "
        f"{describe_sharpe_ratio(sharpe_ratio)}. "
        f"Markets are currently classified as {regime}, which is worth "
        f"keeping in mind when weighing these numbers."
    )


def get_dashboard_metric(dataframe, metric_name, default=None):
    if (
        dataframe is None
        or dataframe.empty
        or "metric" not in dataframe.columns
        or "value" not in dataframe.columns
    ):
        return default

    match = dataframe.loc[dataframe["metric"] == metric_name]

    if match.empty:
        return default

    return match.iloc[0]["value"]


def create_export_executive_conclusion(
    portfolio_results,
    backtest_results,
    regime_forecast_dashboard,
    tickers,
):
    if portfolio_results is None or portfolio_results.empty:
        return (
            "No saved results are available yet, run the optimizer or check "
            "the exports folder to populate the optimization, risk, backtest, "
            "and research views."
        )

    max_sharpe_matches = portfolio_results.loc[
        portfolio_results["portfolio"] == "Optimized Max Sharpe"
    ]
    max_sharpe_row = (
        max_sharpe_matches.iloc[0]
        if not max_sharpe_matches.empty
        else portfolio_results.iloc[0]
    )

    backtest_row = None
    if backtest_results is not None and not backtest_results.empty:
        backtest_matches = backtest_results.loc[
            backtest_results["strategy"].str.contains(
                "Max Sharpe", case=False, na=False
            )
        ]
        backtest_row = (
            backtest_matches.iloc[0]
            if not backtest_matches.empty
            else backtest_results.iloc[0]
        )

    regime = prettify_display_text(
        get_dashboard_metric(
            regime_forecast_dashboard,
            "Latest Regime",
            "an undetermined regime",
        )
    )
    sharpe_ratio = max_sharpe_row.get("sharpe_ratio", 0)

    conclusion = (
        f"These are the saved results for {tickers}. The max Sharpe portfolio "
        f"is built for a {max_sharpe_row.get('return', 0):.2%} return at "
        f"{max_sharpe_row.get('volatility', 0):.2%} volatility, for a Sharpe "
        f"ratio of {sharpe_ratio:.3f}, {describe_sharpe_ratio(sharpe_ratio)}."
    )

    if backtest_row is not None:
        drawdown = backtest_row.get("max_drawdown", 0)
        conclusion += (
            f" Backtesting it against history produced a "
            f"{backtest_row.get('total_return', 0):.2%} total return, with the "
            f"portfolio dipping as much as {drawdown:.2%} from its peak along "
            f"the way."
        )

    conclusion += f" These figures were generated under {regime} conditions."

    return conclusion


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

st.markdown(APP_CSS, unsafe_allow_html=True)

sidebar_live_pill_markup = (
    '<div class="live-pill">Live</div>'
    if st.session_state.get("live_results") is not None
    else ""
)

st.sidebar.markdown(
    f"""
    <div class="sidebar-brand">
        <div>
            <div class="sidebar-title">Portfolio</div>
            <div class="sidebar-kicker">Optimizer</div>
        </div>{sidebar_live_pill_markup}
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
                "",
                "green",
            )

        with overview_columns[1]:
            show_metric_card(
                "Annualized Volatility",
                f"{optimized_backtest['annualized_volatility']:.2%}",
                "",
                "blue",
            )

        with overview_columns[2]:
            show_metric_card(
                "Sharpe Ratio",
                f"{optimized_backtest['sharpe_ratio']:.3f}",
                "",
                "purple",
            )

        with overview_columns[3]:
            show_metric_card(
                "Maximum Drawdown",
                f"{optimized_backtest['max_drawdown']:.2%}",
                "",
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

            render_backtest_charts(live_backtest_results, "live_backtest")
            show_dataframe("Live Backtest Results", live_backtest_results)

    else:
        if backtest_results.empty:
            st.warning("Backtest results are not available yet.")
        else:
            render_backtest_charts(backtest_results, "backtest")
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

    st.subheader("Data Completeness")
    st.caption(
        "These tables describe the saved research bundle itself, including how "
        "many output files were generated and whether they're fully populated, "
        "rather than portfolio results."
    )
    show_dataframe("Research Master Dashboard", research_dashboard)
    show_dataframe("Final Institutional Research Report", final_report)

show_footer()
