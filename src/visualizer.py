import matplotlib.pyplot as plt


def plot_efficient_frontier(
    portfolio_results,
    simulated_max_sharpe=None,
    simulated_min_volatility=None,
    optimized_max_sharpe=None,
    optimized_min_volatility=None,
    efficient_frontier=None,
    save_path=None,
    show_plot=True
):
    plt.figure(figsize=(10, 6))

    scatter = plt.scatter(
        portfolio_results["volatility"],
        portfolio_results["return"],
        c=portfolio_results["sharpe_ratio"],
        cmap="viridis",
        alpha=0.5
    )

    plt.colorbar(scatter, label="Sharpe Ratio")

    if efficient_frontier is not None:
        plt.plot(
            efficient_frontier["volatility"],
            efficient_frontier["return"],
            linewidth=3,
            label="Efficient Frontier"
        )

    if simulated_max_sharpe is not None:
        plt.scatter(
            simulated_max_sharpe["volatility"],
            simulated_max_sharpe["return"],
            marker="*",
            s=250,
            label="Simulated Max Sharpe"
        )

    if simulated_min_volatility is not None:
        plt.scatter(
            simulated_min_volatility["volatility"],
            simulated_min_volatility["return"],
            marker="X",
            s=200,
            label="Simulated Min Volatility"
        )

    if optimized_max_sharpe is not None:
        plt.scatter(
            optimized_max_sharpe["volatility"],
            optimized_max_sharpe["return"],
            marker="D",
            s=180,
            label="Optimized Max Sharpe"
        )

    if optimized_min_volatility is not None:
        plt.scatter(
            optimized_min_volatility["volatility"],
            optimized_min_volatility["return"],
            marker="P",
            s=180,
            label="Optimized Min Volatility"
        )

    plt.xlabel("Annual Volatility")
    plt.ylabel("Expected Annual Return")
    plt.title("Efficient Frontier with Simulated and Optimized Portfolios")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    if save_path is not None:
        plt.savefig(save_path, dpi=300)

    if show_plot:
        plt.show()

    plt.close()


def plot_backtest_growth(
    portfolio_growth,
    benchmark_growth=None,
    save_path=None,
    show_plot=True
):
    plt.figure(figsize=(10, 6))

    plt.plot(
        portfolio_growth.index,
        portfolio_growth,
        linewidth=2,
        label="Portfolio"
    )

    if benchmark_growth is not None:
        plt.plot(
            benchmark_growth.index,
            benchmark_growth,
            linewidth=2,
            label="Benchmark"
        )

    plt.xlabel("Date")
    plt.ylabel("Growth of $1")
    plt.title("Backtest Portfolio Growth vs Benchmark")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    if save_path is not None:
        plt.savefig(save_path, dpi=300)

    if show_plot:
        plt.show()

    plt.close()


def plot_drawdown(
    portfolio_drawdown,
    benchmark_drawdown=None,
    save_path=None,
    show_plot=True
):
    plt.figure(figsize=(10, 6))

    plt.plot(
        portfolio_drawdown.index,
        portfolio_drawdown,
        linewidth=2,
        label="Portfolio Drawdown"
    )

    if benchmark_drawdown is not None:
        plt.plot(
            benchmark_drawdown.index,
            benchmark_drawdown,
            linewidth=2,
            label="Benchmark Drawdown"
        )

    plt.xlabel("Date")
    plt.ylabel("Drawdown")
    plt.title("Portfolio Drawdown vs Benchmark")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    if save_path is not None:
        plt.savefig(save_path, dpi=300)

    if show_plot:
        plt.show()

    plt.close()


def plot_rolling_metric(
    portfolio_metric,
    benchmark_metric=None,
    title="Rolling Metric",
    ylabel="Value",
    portfolio_label="Portfolio",
    benchmark_label="Benchmark",
    save_path=None,
    show_plot=True
):
    plt.figure(figsize=(10, 6))

    plt.plot(
        portfolio_metric.index,
        portfolio_metric,
        linewidth=2,
        label=portfolio_label
    )

    if benchmark_metric is not None:
        plt.plot(
            benchmark_metric.index,
            benchmark_metric,
            linewidth=2,
            label=benchmark_label
        )

    plt.xlabel("Date")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    if save_path is not None:
        plt.savefig(save_path, dpi=300)

    if show_plot:
        plt.show()

    plt.close()