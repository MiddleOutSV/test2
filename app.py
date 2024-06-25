import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import random

def get_stock_data(ticker, indicator):
    try:
        stock = yf.Ticker(ticker)
        return stock.info.get(indicator)
    except:
        st.warning(f"Could not fetch {indicator} data for {ticker}")
        return None

def visualize_circle_data(tickers, data, title):
    if not data:
        st.error("No valid data available.")
        return

    fig, ax = plt.subplots(figsize=(12, 6))
    
    max_value = max(data)
    max_radius = 0.4  # 최대 원의 반지름
    
    x_position = 0
    for ticker, value in zip(tickers, data):
        radius = (value / max_value) * max_radius
        color = f'#{random.randint(0, 0xFFFFFF):06x}'
        circle = Circle((x_position, 0), radius, fill=True, alpha=0.6, color=color)
        ax.add_patch(circle)
        ax.text(x_position, -max_radius - 0.05, f"{ticker}\n{value:,.0f}", ha='center', va='top')
        x_position += 2 * max_radius + 0.1  # 원 사이의 간격
    
    ax.set_xlim(-max_radius, x_position - max_radius)
    ax.set_ylim(-max_radius - 0.2, max_radius)
    ax.set_aspect('equal')
    ax.axis('off')
    
    st.pyplot(fig)

def visualize_bar_data(tickers, data, title):
    if not data:
        st.error("No valid data available.")
        return

    fig, ax = plt.subplots(figsize=(12, 6))
    
    bars = ax.bar(tickers, data)
    
    # 각 막대 위에 값 표시
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.2f}', ha='center', va='bottom')
    
    plt.xticks(rotation=45)
    st.pyplot(fig)

st.title('주식 지표 비교 시각화')

tickers_input = st.text_input('ticker 심볼들을 쉼표로 구분하여 입력하세요 (예: AAPL,MSFT,GOOGL):')

indicators = {
    '시가총액': 'marketCap',
    '거래량': 'volume',
    '주당순이익(EPS)': 'trailingEps',
    '연간배당금': 'dividendRate',
    '배당 수익률': 'dividendYield',
    '기업가치/EBITDA 비율': 'enterpriseToEbitda',
    '잉여 현금 흐름': 'freeCashflow',
    '베타 계수': 'beta'
}

selected_indicator = st.selectbox('비교할 지표를 선택하세요:', list(indicators.keys()))

if tickers_input and selected_indicator:
    tickers = [ticker.strip() for ticker in tickers_input.split(',')]
    indicator_key = indicators[selected_indicator]
    
    data = []
    valid_tickers = []
    for ticker in tickers:
        value = get_stock_data(ticker, indicator_key)
        if value is not None:
            data.append(value)
            valid_tickers.append(ticker)
    
    if selected_indicator in ['시가총액', '거래량', '베타 계수']:
        visualize_circle_data(valid_tickers, data, f'{selected_indicator} 비교')
    else:
        visualize_bar_data(valid_tickers, data, f'{selected_indicator} 비교')
