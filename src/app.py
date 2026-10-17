"""Beginner-friendly Streamlit interface for the notebook analyses."""

from datetime import datetime, timezone

import pandas as pd
import streamlit as st

from analysis import get_analyst_ratings, get_financials, get_news, get_price
from analysis_storage import (
    analysis_label,
    list_saved_analyses,
    read_analysis,
    save_analysis,
)


st.set_page_config(page_title="Stock Explorer", page_icon="📈", layout="wide")
st.title("Stock Explorer")
st.write("Choose an analysis and enter a stock ticker to explore Yahoo Finance data.")

ticker = st.text_input("Ticker symbol", value="MU", max_chars=10).strip().upper()
analysis_type = st.selectbox(
    "Analysis type",
    ["filings", "news", "stock price ratings"],
)


def _markdown_table(table: pd.DataFrame) -> str:
    """Render a dataframe as a dependency-free Markdown table."""
    if table.empty:
        return "_No data was found._"

    rows = table.reset_index()
    headers = [str(column).replace("|", "\\|") for column in rows.columns]
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows.itertuples(index=False, name=None):
        values = [str(value).replace("|", "\\|").replace("\n", " ") for value in row]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def _run_analysis(symbol: str, selected_analysis: str) -> str:
    """Fetch the selected analysis and return the Markdown shown to the user."""
    sections = [f"# {selected_analysis.title()} analysis for {symbol}"]

    if selected_analysis == "filings":
        for name, table in get_financials(symbol).items():
            sections.extend([f"## {name}", _markdown_table(table)])
    elif selected_analysis == "news":
        sections.extend(["## Recent news", _markdown_table(get_news(symbol))])
    else:
        price = get_price(symbol)
        sections.extend(
            [
                "## Current price",
                f"${price:,.2f}" if price is not None else "_A current price was not found._",
                "## Latest analyst recommendations",
                _markdown_table(get_analyst_ratings(symbol)),
            ]
        )

    created_at = datetime.now(timezone.utc)
    return "\n\n".join(
        [
            f"**Ticker:** {symbol}",
            f"**Analysis type:** {selected_analysis}",
            f"**Created:** {created_at.astimezone().strftime('%Y-%m-%d %H:%M:%S %Z')}",
            *sections,
        ]
    )


@st.dialog("Saved Analysis")
def _show_saved_analysis(markdown: str) -> None:
    st.markdown(markdown)


if st.button("Run", type="primary"):
    if not ticker:
        st.error("Please enter a ticker symbol.")
    else:
        try:
            with st.spinner("Loading data..."):
                st.session_state.current_analysis = {
                    "ticker": ticker,
                    "analysis_type": analysis_type,
                    "markdown": _run_analysis(ticker, analysis_type),
                }
        except Exception as error:
            st.error(f"Could not load data for {ticker}: {error}")


current_analysis = st.session_state.get("current_analysis")
if current_analysis:
    st.subheader("Current analysis")
    st.markdown(current_analysis["markdown"])
    if st.button("Save Analysis"):
        try:
            saved_path = save_analysis(
                current_analysis["markdown"],
                current_analysis["ticker"],
                current_analysis["analysis_type"],
            )
            st.success(f"Analysis saved as {saved_path.name}.")
        except OSError as error:
            st.error(f"Could not save the analysis: {error}")


st.subheader("Previous Analyses")
saved_analyses = list_saved_analyses()
if not saved_analyses:
    st.info("No analyses have been saved yet.")
else:
    selected_path = st.selectbox(
        "Select a saved analysis",
        saved_analyses,
        format_func=analysis_label,
    )
    if st.button("Show"):
        try:
            _show_saved_analysis(read_analysis(selected_path))
        except (OSError, ValueError) as error:
            st.error(f"Could not open the saved analysis: {error}")
