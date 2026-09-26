"""Reusable data-fetching functions for the Streamlit app."""

import pandas as pd
import yfinance as yf


def _ticker_symbol(ticker: str) -> str:
    """Return a clean ticker symbol or raise a helpful error."""
    symbol = ticker.strip().upper()
    if not symbol:
        raise ValueError("Enter a ticker symbol, such as MU or GOOG.")
    return symbol


def get_financials(ticker: str) -> dict[str, pd.DataFrame]:
    """Return the latest income statement, balance sheet, and cash flow."""
    stock = yf.Ticker(_ticker_symbol(ticker))
    return {
        "Income Statement": stock.financials.head(),
        "Balance Sheet": stock.balance_sheet.head(),
        "Cash Flow": stock.cashflow.head(),
    }


def get_news(ticker: str, limit: int = 5) -> pd.DataFrame:
    """Return recent news articles as a small table."""
    symbol = _ticker_symbol(ticker)
    articles = yf.Ticker(symbol).news or []
    rows = []

    for article in articles[:limit]:
        content = article.get("content", article)
        rows.append(
            {
                "Title": content.get("title", "No title"),
                "Publisher": content.get("provider", {}).get("displayName", ""),
                "Summary": content.get("description", "No description"),
                "Link": content.get("canonicalUrl", {}).get("url", ""),
            }
        )

    return pd.DataFrame(rows, columns=["Title", "Publisher", "Summary", "Link"])


def get_price(ticker: str) -> float | None:
    """Return the latest available price for a ticker."""
    stock = yf.Ticker(_ticker_symbol(ticker))
    price = stock.info.get("currentPrice")

    if price is None:
        price = stock.fast_info.get("last_price")

    return float(price) if price is not None else None


def get_analyst_ratings(ticker: str) -> pd.DataFrame:
    """Return the ten most recent analyst recommendation rows."""
    recommendations = yf.Ticker(_ticker_symbol(ticker)).recommendations
    if recommendations is None or recommendations.empty:
        return pd.DataFrame()
    return recommendations.tail(10)