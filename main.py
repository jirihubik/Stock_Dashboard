""" main.py - STOCK DASHBOARD with Streamlit frontend """

import streamlit as st
from dotenv import load_dotenv
import logging
import os
import yfinance as yf
import matplotlib.pyplot as plt
from finnhubAPI_client import FinnhubAPIClient
from openAI_assistant import OpenAIAssistant  
from database import init_db, save_ticker_data  


logging.basicConfig(filename="stock_dashboard.log", level=logging.ERROR, encoding="utf-8")

load_dotenv()
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
finnhub_client = FinnhubAPIClient(api_key=FINNHUB_API_KEY)
openai_assistant = OpenAIAssistant() 

st.set_page_config(page_title="Stock Dashboard", layout="centered")

st.title("📈 Stock Dashboard")
st.markdown("Jednoduchý přehled o akciích s AI asistentem, grafy a benchmarkem.")

def plot_stock_graph(ticker, period,ma_value,benchmark="SPY"):
    """ plotting stock graph """
    try:
        stock_data = yf.Ticker(ticker).history(period=period)
        if stock_data.empty:
            st.error(f"❌ Pro ticker {ticker.upper()} nejsou dostupná cenová data. Možná byl delistován.")
            return 
        
        spy_data = yf.Ticker("SPY").history(period=period)
       
        stock_data['MA'] = stock_data['Close'].rolling(window=ma_value).mean()
        # Conversion of SPY to a comparable basis (normalization by the first value)
        spy_normalized = spy_data['Close'] / spy_data['Close'].iloc[0] * stock_data['Close'].iloc[0]
        
        fig, ax = plt.subplots(figsize=(12, 6))
       
        ax.plot(stock_data.index, stock_data['Close'], label=f'{ticker.upper()} Close', color='blue')
        
        ax.plot(stock_data.index, stock_data['MA'], label=f'{ma_value}-denní MA', color='orange', linestyle='--')
       
        ax.plot(spy_data.index, spy_normalized, label='SPY (Benchmark)', color='grey', linestyle=':')
       
        ax.set_title(f'Vývoj ceny akcie {ticker.upper()} s {ma_value}-denním klouzavým průměrem a SPY benchmarkem')
        ax.set_xlabel('Datum')
        ax.set_ylabel('Cena (Close)')
        ax.legend()
       
        st.pyplot(fig)

    except Exception as e:
        logging.error(f"Chyba při načítání dat pro {ticker}: {e}")
    

# user input form
with st.form(key='stock_form'):
    st.header("🔍 Vyhledat akcii")    
    
    ticker = st.text_input("Zadejte ticker akcie (např. AAPL, MSFT, GOOGL,...)", value="AAPL")    
    
    period = st.selectbox(
        "Vyberte období pro graf:",
        options=["1mo", "3mo", "6mo", "1y", "2y", "5y"],
        index=2  # Default 6 months
    )    
    
    ma_value = st.number_input(
        "Zadejte hodnotu pro Moving Average (MA):",
        min_value=1,
        max_value=200,
        value=20
    )    
    
    submit_button = st.form_submit_button(label="Zobrazit informace")

if submit_button:
    st.write("---")   
    st.header("🏢 Informace o společnosti")    
    profile = finnhub_client.get_company_profile(ticker)
    
    if 'error' in profile:
        st.error(profile['error'])
    else:
        save_ticker_data(
            ticker=ticker.upper(),
            company_name=profile.get("name", "N/A"),
            sector=profile.get("finnhubIndustry", "N/A"),
            website=profile.get("weburl", "N/A"),
            country=profile.get("country", "N/A"),
            ipo_date=profile.get("ipo", "N/A"),
        )
        
        st.subheader(profile.get("name", "Neznámá společnost"))
        st.write(f"**Ticker:** {profile.get('ticker', 'N/A')}")
        st.write(f"**Logo:** {profile.get('logo', 'N/A')}")
        st.write(f"**Sektor:** {profile.get('finnhubIndustry', 'N/A')}")
        st.write(f"**Web:** {profile.get('weburl', 'N/A')}")
        st.write(f"**Země:** {profile.get('country', 'N/A')}")
        st.write(f"**IPO datum:** {profile.get('ipo', 'N/A')}")

    st.write("---") 
    
    if 'error' in profile:
        st.error("❌ Nelze načíst informace o společnosti. Zkontrolujte ticker a zkuste to znovu.")
    else:
        summary = openai_assistant.get_openai_summary(ticker)        

        if not summary or summary.strip() == "":
            st.error("⚠️ Nebylo možné získat shrnutí společnosti. Zkuste jiný ticker.")
        else:
            st.header(f"📌 Shrnutí informací o společnosti")
            st.markdown(summary)

    st.write("---")    
    st.header("📊 Graf vývoje ceny akcie")
    plot_stock_graph(ticker, period,ma_value,benchmark="SPY")
