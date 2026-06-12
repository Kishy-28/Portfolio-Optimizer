import plotly.express as px

from formatting import prettify_chart_categories


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


def build_growth_curve_chart(growth_curve, width=760, height=250, top=20, bottom=230):
    if growth_curve is None:
        return None

    values = growth_curve.dropna().tolist()

    if len(values) < 2:
        return None

    num_points = min(14, len(values))
    step = (len(values) - 1) / (num_points - 1)
    sampled = [values[round(index * step)] for index in range(num_points)]

    min_value = min(sampled)
    max_value = max(sampled)
    value_range = (max_value - min_value) or 1.0

    points = []
    for index, value in enumerate(sampled):
        x = width * index / (num_points - 1)
        normalized = (value - min_value) / value_range
        y = bottom - normalized * (bottom - top)
        points.append((round(x, 1), round(y, 1)))

    polyline = " ".join(f"{x},{y}" for x, y in points)
    area_path = (
        "M" + " L".join(f"{x},{y}" for x, y in points)
        + f" L{width},{height} L0,{height} Z"
    )
    last_x, last_y = points[-1]

    return {
        "polyline": polyline,
        "area_path": area_path,
        "last_x": last_x,
        "last_y": last_y,
    }
