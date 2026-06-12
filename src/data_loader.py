import yfinance as yf

from src.validation import validate_tickers, validate_price_data


def load_price_data(tickers, start_date, end_date):
    """
    Downloads adjusted closing price data for the given tickers.
    """

    validate_tickers(tickers)

    data = yf.download(
        tickers,
        start=start_date,
        end=end_date,
        auto_adjust=True
    )

    prices = data["Close"]

    validate_price_data(prices)

    return prices


def load_volume_data(tickers, start_date, end_date):
    """
    Downloads trading volume data for the given tickers.
    """

    validate_tickers(tickers)

    data = yf.download(
        tickers,
        start=start_date,
        end=end_date,
        auto_adjust=True
    )

    volume = data["Volume"]

    validate_price_data(volume)

    return volume