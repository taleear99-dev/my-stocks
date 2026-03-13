import streamlit as st
import yfinance as yf
import pandas as pd

# הגדרות דף
st.set_page_config(page_title="עוזר השקעות אישי", layout="wide")

# פונקציה לעברית בסיסית בממשק
st.markdown("""
    <style>
    .reportview-container { direction: rtl; }
    .main { text-align: right; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 עוזר השקעות חכם למתחילים")
st.write("כאן תוכל לנתח מניות ולקבל תובנות פשוטות על השוק.")

# בחירת מניה
ticker = st.text_input("הכנס סימול מניה (למשל TSLA, NVDA, AAPL):", "NVDA").upper()

if ticker:
    data = yf.Ticker(ticker)
    df = data.history(period="1y")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(f"גרף מחיר - {ticker}")
        st.line_chart(df['Close'])
        
    with col2:
        st.subheader("ניתוח מהיר למתחילים")
        current_price = df['Close'][-1]
        prev_price = df['Close'][-2]
        change = ((current_price - prev_price) / prev_price) * 100
        
        st.metric("מחיר נוכחי", f"${current_price:.2f}", f"{change:.2f}%")
        
        # המלצה בסיסית מבוססת ממוצעים
        ma50 = df['Close'].rolling(window=50).mean()[-1]
        if current_price > ma50:
            st.success("💡 המלצה: המניה במגמה עולה (מעל ממוצע 50 יום).")
        else:
            st.warning("⚠️ שים לב: המניה במגמה יורדת כרגע.")

st.divider()
st.subheader("📰 עדכונים מהבורסה")
news = data.news
for n in news[:3]:
    st.write(f"**{n['title']}**")
    st.write(f"[לקריאה נוספת]({n['link']})")
    