def validate_tickers(tickers):
    if not tickers:
        raise ValueError("Ticker list cannot be empty.")

    if not isinstance(tickers, list):
        raise TypeError("Tickers must be provided as a list.")

    for ticker in tickers:
        if not isinstance(ticker, str):
            raise TypeError("Each ticker must be a string.")


def validate_price_data(prices):
    if prices is None:
        raise ValueError("Price data is missing.")

    if prices.empty:
        raise ValueError("Price data is empty. Check your tickers or date range.")

    if prices.isnull().all().any():
        raise ValueError("At least one ticker has no valid price data.")