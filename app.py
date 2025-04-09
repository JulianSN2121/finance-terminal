{\rtf1\ansi\ansicpg1252\cocoartf2822
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import streamlit as st\
import yfinance as yf\
import pandas as pd\
\
st.set_page_config(page_title="KGV Analyzer", layout="wide")\
st.title("\uc0\u55357 \u56522  KGV Analyzer \'96 Kurs-Gewinn-Verh\'e4ltnis von Unternehmen")\
\
st.markdown("Gib ein oder mehrere Tickersymbole ein (z.\uc0\u8239 B. `AAPL`, `MSFT`, `GOOG`), getrennt durch Kommas:")\
\
input_tickers = st.text_input("Tickersymbole:", "AAPL, MSFT, GOOGL")\
tickers = [t.strip().upper() for t in input_tickers.split(",") if t.strip()]\
\
if tickers:\
    for ticker in tickers:\
        stock = yf.Ticker(ticker)\
        info = stock.info\
\
        st.divider()\
        st.subheader(f"\uc0\u55357 \u56524  \{ticker\} \'96 \{info.get('shortName', 'Unbekannt')\}")\
\
        # Aktuelles KGV\
        kgv = info.get("trailingPE")\
        st.metric("Aktuelles KGV", f"\{kgv:.2f\}" if kgv else "Nicht verf\'fcgbar")\
\
        # Historisches KGV \'fcber 5 Jahre\
        earnings = stock.earnings\
        price = stock.history(period="5y", interval="1mo")\
\
        if not earnings.empty and not price.empty:\
            price_yearly = price["Close"].resample("Y").last()\
            earnings_yearly = earnings["Earnings"]\
\
            # Sync Jahre\
            common_years = price_yearly.index.year.intersection(earnings.index)\
            kgv_hist = price_yearly[price_yearly.index.year.isin(common_years)] / earnings.loc[common_years]\
\
            st.line_chart(pd.DataFrame(\{\
                "Historisches KGV": kgv_hist\
            \}))\
        else:\
            st.warning("Keine historischen KGV-Daten verf\'fcgbar.")}