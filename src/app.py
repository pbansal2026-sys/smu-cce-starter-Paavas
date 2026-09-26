"""Beginner-friendly Streamlit interface for the notebook analyses."""

import streamlit as st

from analysis import get_analyst_ratings, get_financials, get_news, get_price


st.set_page_config(page_title="Stock Explorer", page_icon="📈", layout="wide")
st.title("Stock Explorer")
st.write("Choose an analysis and enter a stock ticker to explore Yahoo Finance data.")

ticker = st.text_input("Ticker symbol", value="MU", max_chars=10).strip().upper()
analysis_type = st.selectbox(
    "Analysis type",
    ["filings", "news", "stock price ratings"],
)

if st.button("Run", type="primary"):
    if not ticker:
        st.error("Please enter a ticker symbol.")
    else:
        try:
            with st.spinner("Loading data..."):
                if analysis_type == "filings":
                    st.subheader(f"Financial statements for {ticker}")
                    financials = get_financials(ticker)
                    for name, table in financials.items():
                        st.write(f"**{name}**")
                        if table.empty:
                            st.info(f"No {name.lower()} data was found.")
                        else:
                            st.dataframe(table, use_container_width=True)

                elif analysis_type == "news":
                    st.subheader(f"Recent news for {ticker}")
                    news = get_news(ticker)
                    if news.empty:
                        st.info("No recent news was found.")
                    else:
                        st.dataframe(news, use_container_width=True, hide_index=True)

                else:
                    st.subheader(f"Price and analyst ratings for {ticker}")
                    price = get_price(ticker)
                    if price is None:
                        st.info("A current price was not found.")
                    else:
                        st.metric("Current price", f"${price:,.2f}")

                    ratings = get_analyst_ratings(ticker)
                    st.write("**Latest analyst recommendations**")
                    if ratings.empty:
                        st.info("No analyst recommendations were found.")
                    else:
                        st.dataframe(ratings, use_container_width=True)
        except Exception as error:
            st.error(f"Could not load data for {ticker}: {error}")