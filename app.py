import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="KGV Analyzer", layout="wide")
st.title("📊 KGV Analyzer – Kurs-Gewinn-Verhältnis von Unternehmen")

st.markdown("Gib ein oder mehrere Tickersymbole ein (z. B. `AAPL`, `MSFT`, `GOOG`), getrennt durch Kommas:")

input_tickers = st.text_input("Tickersymbole:", "AAPL, MSFT, GOOGL")
tickers = [t.strip().upper() for t in input_tickers.split(",") if t.strip()]

if tickers:
    for ticker in tickers:
        stock = yf.Ticker(ticker)
        info = stock.info

        st.divider()
        st.subheader(f"📌 {ticker} – {info.get('shortName', 'Unbekannt')}")

        # Aktuelles KGV
        kgv = info.get("trailingPE")
        st.metric("Aktuelles KGV", f"{kgv:.2f}" if kgv else "Nicht verfügbar")

        # Historisches KGV über 5 Jahre
        earnings = stock.earnings
        price = stock.history(period="5y", interval="1mo")

        if not earnings.empty and not price.empty:
            price_yearly = price["Close"].resample("Y").last()
            earnings_yearly = earnings["Earnings"]

            # Sync Jahre
            common_years = price_yearly.index.year.intersection(earnings.index)
            kgv_hist = price_yearly[price_yearly.index.year.isin(common_years)] / earnings.loc[common_years]

            st.line_chart(pd.DataFrame({
                "Historisches KGV": kgv_hist
            }))
        else:
            st.warning("Keine historischen KGV-Daten verfügbar.")
        