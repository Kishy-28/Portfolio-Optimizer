# Portfolio Optimizer

A dark Streamlit dashboard for portfolio optimization, backtesting, risk review, regime research, and saved research reporting. The app is built for quick scenario review while keeping a fallback path for previously generated research outputs.

## Key Features

- Live portfolio optimization from sidebar inputs
- Risk and return summary cards for fast review
- Backtesting views for realized performance, drawdown, and Sharpe ratio
- Risk management tables covering drawdowns, stress tests, VaR, market shocks, concentration, and tail risk
- Strategy, regime, and forecast research sections
- Download center for saved research outputs
- Export fallback mode when live results have not been generated

## App Architecture

The project uses a Streamlit front end backed by a Python optimization and research engine.

- `app.py` runs the Streamlit dashboard and live app experience.
- `main.py` can generate saved research outputs.
- `src/` contains the optimization, analytics, risk, reporting, and research modules.
- `exports/` contains saved outputs used by the dashboard fallback mode.

## Run Locally

1. Create and activate a virtual environment.

```bash
python -m venv .venv
```

2. Install dependencies.

```bash
pip install -r requirements.txt
```

3. Start the Streamlit app.

```bash
streamlit run app.py
```

4. Open the local URL shown by Streamlit.

## Deploy on Streamlit Community Cloud

Streamlit Community Cloud runs the selected entrypoint file from a GitHub repo and installs dependencies from the root `requirements.txt`.

1. Push the project to GitHub.
2. Go to Streamlit Community Cloud.
3. Create a new app.
4. Select the GitHub repository.
5. Select branch: `main`.
6. Set app file path: `app.py`.
7. Deploy.
8. If deployment fails, check the logs for missing packages or import errors.

## Screenshots Checklist

- Executive Overview
- Optimization
- Backtesting
- Risk Management
- Regimes & Forecasts
- Research Platform
- Downloads

## Live Mode and Export Fallback

Live mode runs the optimizer from the current sidebar inputs and updates the dashboard with the selected portfolio settings.

Export fallback mode keeps the app usable when live results have not been generated. In that mode, the dashboard reads saved research outputs from `exports/`.

## Resume Bullets

- Built a Streamlit portfolio analytics dashboard with live optimization, risk review, backtesting, and downloadable research outputs.
- Implemented a fallback reporting workflow that keeps the dashboard usable from saved exports when live calculations are not active.
- Designed a dark fintech-style interface with cleaned tables, Plotly visualizations, and organized research sections for portfolio review.

## LinkedIn Project Description

I built a Portfolio Optimizer dashboard in Streamlit to make portfolio research easier to review and present. The app supports live optimization scenarios, backtesting, risk analytics, regime and forecast research, and saved output downloads in a polished dark interface.

## Interview Talking Points

- Why I built it: To turn portfolio optimization research into an interactive dashboard that is easier to explore, explain, and share.
- What the optimizer does: It compares portfolio allocations using return, volatility, Sharpe ratio, drawdown, and related risk metrics.
- How live mode works: The Streamlit sidebar sends the selected inputs into the live optimizer and updates the dashboard with fresh results.
- How export fallback works: If live results are not available, the app reads saved research outputs from `exports/` so the dashboard still has usable content.
- Risk analytics included: Value at Risk, stress tests, drawdown analysis, market shocks, concentration risk, tail risk, and governance-style summaries.
- What I would improve next: Add authentication, richer portfolio upload support, persistent scenario history, and more production-grade deployment monitoring.

## Expected Repo Structure

```text
app.py
main.py
requirements.txt
README.md
.gitignore
exports/
src/
```
