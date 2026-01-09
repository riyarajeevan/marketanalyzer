import streamlit as st
import pandas as pd
import numpy as np
import sys
import os

st.set_page_config(
    page_title="Market Analyzer", 
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon=None
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Google+Sans+Code:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Google Sans Code', sans-serif !important;
    }
    
    .main {
        background: #000000;
        color: #ffffff;
    }
    
    .stApp {
        background: #000000;
    }
    
    h1, h2, h3 {
        color: #ffffff;
        font-weight: 300;
        font-family: 'Google Sans Code', sans-serif !important;
    }
    
    h1 {
        font-size: 4.5rem;
        font-weight: 300;
        color: #ffffff;
        letter-spacing: -0.03em;
        line-height: 1.1;
        margin: 0;
        padding: 0;
    }
    
    h2 {
        font-size: 2rem;
        font-weight: 300;
        color: #ffffff;
        letter-spacing: -0.02em;
        line-height: 1.2;
        margin-top: 0;
        margin-bottom: 1rem;
    }
    
    h3 {
        font-size: 1.5rem;
        font-weight: 300;
        color: #ffffff;
        letter-spacing: -0.01em;
        line-height: 1.3;
        margin-top: 0;
        margin-bottom: 0.75rem;
    }
    
    .stButton>button {
        background: #592E83;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.5rem;
        font-weight: 400;
        font-size: 0.95rem;
    }
    
    .stButton>button:hover {
        background: #9984D4;
    }
    
    .stMetric {
        background: rgba(16, 12, 51, 0.5);
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #9984D4;
    }
    
    .stMetric label {
        color: #a0a0a0;
        font-size: 0.9rem;
        font-weight: 500;
    }
    
    .stMetric [data-testid="stMetricValue"] {
        color: #ffffff;
        font-size: 1.8rem;
        font-weight: 700;
    }
    
    .stMetric [data-testid="stMetricDelta"] {
        font-weight: 600;
    }
    
    [data-testid="stSidebar"] {
        background: #000000;
        border-right: 1px solid #9984D4;
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h2 {
        color: #ffffff;
        font-weight: 300;
    }
    
    .stSelectbox label, .stTextInput label, .stSlider label {
        color: #ffffff;
        font-weight: 500;
    }
    
    .stSelectbox>div>div {
        background: #100C33;
        border: 1px solid #9984D4;
        border-radius: 6px;
        color: #ffffff;
    }
    
    .stTextInput>div>div>input {
        background: #100C33;
        border: 1px solid #9984D4;
        border-radius: 6px;
        color: #ffffff;
    }
    
    .stSlider>div>div>div {
        background: #100C33;
    }
    
    .stSlider>div>div>div>div {
        background: #9984D4;
    }
    
    .element-container {
        margin-bottom: 0.75rem;
    }
    
    .stMarkdown {
        margin-bottom: 0.5rem;
    }
    
    [data-testid="stVerticalBlock"] {
        gap: 0.5rem;
    }
    
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    
    .stDataFrame {
        background: #100C33;
        border-radius: 8px;
        border: 1px solid #9984D4;
    }
    
    .stSpinner>div {
        border-color: #9984D4;
    }
    
    .stAlert {
        background: #100C33;
        border: 1px solid #9984D4;
        border-radius: 6px;
    }
</style>
""", unsafe_allow_html=True)

try:
    import plotly.graph_objects as go
    import plotly.express as px
except:
    st.error("need to install plotly")
    st.stop()

sys.path.append(os.path.dirname(__file__))

try:
    from src.data_fetchers import YahooFinanceFetcher
    from src.data_processing import ReturnCalculator, VolatilityCalculator
except Exception as e:
    st.error(f"error: {e}")
    st.stop()

if 'fetcher' not in st.session_state:
    st.session_state.fetcher = YahooFinanceFetcher()
if 'calc' not in st.session_state:
    st.session_state.calc = ReturnCalculator()
if 'risk_calc' not in st.session_state:
    st.session_state.risk_calc = VolatilityCalculator()

st.markdown("""
<div style='text-align: left; margin-bottom: 0.5rem; padding-top: 5rem;'>
    <h1 style='font-size: 4.5rem; font-weight: 300; color: #ffffff; letter-spacing: -0.03em; line-height: 1.1; margin: 0; padding: 0; font-family: "Google Sans Code", sans-serif;'>
        Market Analyzer
    </h1>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("<h2 style='color: #ffffff; margin-bottom: 1rem; font-size: 1.5rem; font-weight: 300; letter-spacing: -0.01em;'>Navigation</h2>", unsafe_allow_html=True)
page = st.sidebar.selectbox("", ["Stock Analysis", "Compare Stocks", "Risk Metrics"], label_visibility="collapsed")

colors = {
    'dark_purple': '#100C33',
    'tekhelet': '#592E83',
    'tropical_indigo': '#9984D4',
    'mountbatten_pink': '#A6809D',
    'brown_sugar': '#B27C66',
    'dark_bg': '#100C33',
    'darker_bg': '#000000',
    'border': '#9984D4',
    'text': '#ffffff',
    'text_secondary': '#a0a0a0'
}

plotly_template = {
    'layout': {
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
        'plot_bgcolor': 'rgba(16, 12, 51, 0.3)',
        'font': {'color': '#ffffff', 'family': 'Google Sans Code'},
        'xaxis': {
            'gridcolor': '#9984D4',
            'linecolor': '#9984D4'
        },
        'yaxis': {
            'gridcolor': '#9984D4',
            'linecolor': '#9984D4'
        }
    }
}

if page == "Stock Analysis":
    st.markdown("<h2 style='color: #ffffff; margin-top: 0; margin-bottom: 0.5rem;'>Stock Analysis</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #a0a0a0; margin-bottom: 0.75rem; font-size: 1rem;'>Analyze individual stocks with price charts, volume data, and returns analysis</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        ticker = st.text_input("Stock ticker", value="AAPL", placeholder="e.g., AAPL, MSFT, GOOGL")
    
    with col2:
        period = st.selectbox("Time period", ["1mo", "3mo", "6mo", "1y", "2y"], index=2)
    
    if st.button("Get Data", use_container_width=True) or ticker:
        try:
            with st.spinner("Fetching data..."):
                data = st.session_state.fetcher.get_stock_data(ticker, period=period)
            
            if len(data) == 0:
                st.error("no data found")
            else:
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Current Price", f"${data['close'].iloc[-1]:.2f}")
                with col2:
                    change = data['close'].iloc[-1] - data['close'].iloc[-2]
                    change_pct = (change / data['close'].iloc[-2]) * 100
                    delta_color = "normal" if change >= 0 else "inverse"
                    st.metric("Daily Change", f"${change:.2f}", f"{change_pct:.2f}%", delta_color=delta_color)
                with col3:
                    st.metric("Volume", f"{data['volume'].iloc[-1]:,.0f}")
                
                st.markdown("<h3 style='color: #ffffff; margin-top: 1rem; margin-bottom: 0.5rem;'>Price Chart</h3>", unsafe_allow_html=True)
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=data.index, 
                    y=data['close'], 
                    mode='lines', 
                    name='Price',
                    line=dict(color=colors['tropical_indigo'], width=2),
                    fill='tozeroy',
                    fillcolor=f"rgba(153, 132, 212, 0.2)"
                ))
                fig.update_layout(
                    title=dict(text=f"{ticker} Stock Price", font=dict(color='#ffffff', size=20, family='Google Sans Code')),
                    xaxis_title="Date",
                    yaxis_title="Price ($)",
                    height=450,
                    **plotly_template['layout']
                )
                st.plotly_chart(fig, use_container_width=True)
                
                st.markdown("<h3 style='color: #ffffff; margin-top: 1rem; margin-bottom: 0.5rem;'>Volume</h3>", unsafe_allow_html=True)
                fig2 = go.Figure()
                fig2.add_trace(go.Bar(
                    x=data.index, 
                    y=data['volume'], 
                    name='Volume',
                    marker_color=colors['tekhelet'],
                    marker_line_color=colors['tropical_indigo'],
                    marker_line_width=1
                ))
                fig2.update_layout(
                    title=dict(text="Trading Volume", font=dict(color='#ffffff', size=18, family='Google Sans Code')),
                    height=350,
                    **plotly_template['layout']
                )
                st.plotly_chart(fig2, use_container_width=True)
                
                st.markdown("<h3 style='color: #ffffff; margin-top: 1rem; margin-bottom: 0.5rem;'>Returns Analysis</h3>", unsafe_allow_html=True)
                returns = st.session_state.calc.simple_returns(data['close'])
                cum_returns = st.session_state.calc.cumulative_returns(returns)
                
                col1, col2 = st.columns(2)
                with col1:
                    fig3 = go.Figure()
                    fig3.add_trace(go.Scatter(
                        x=returns.index, 
                        y=returns, 
                        mode='lines', 
                        name='Daily Returns',
                        line=dict(color=colors['mountbatten_pink'], width=2),
                        fill='tozeroy',
                        fillcolor=f"rgba(166, 128, 157, 0.2)"
                    ))
                    fig3.add_hline(y=0, line_dash="dash", line_color="rgba(255, 255, 255, 0.3)")
                    fig3.update_layout(
                        title=dict(text="Daily Returns", font=dict(color='#ffffff', size=16, family='Google Sans Code')),
                        height=350,
                        **plotly_template['layout']
                    )
                    st.plotly_chart(fig3, use_container_width=True)
                
                with col2:
                    fig4 = go.Figure()
                    fig4.add_trace(go.Scatter(
                        x=cum_returns.index, 
                        y=cum_returns, 
                        mode='lines', 
                        name='Cumulative',
                        line=dict(color=colors['tropical_indigo'], width=2),
                        fill='tozeroy',
                        fillcolor=f"rgba(153, 132, 212, 0.2)"
                    ))
                    fig4.update_layout(
                        title=dict(text="Cumulative Returns", font=dict(color='#ffffff', size=16, family='Google Sans Code')),
                        height=350,
                        **plotly_template['layout']
                    )
                    st.plotly_chart(fig4, use_container_width=True)
                
                st.markdown("<h3 style='color: #ffffff; margin-top: 1rem; margin-bottom: 0.5rem;'>Returns Distribution</h3>", unsafe_allow_html=True)
                fig5 = go.Figure()
                fig5.add_trace(go.Histogram(
                    x=returns, 
                    nbinsx=50,
                    marker_color=colors['tekhelet'],
                    marker_line_color=colors['tropical_indigo'],
                    marker_line_width=1
                ))
                fig5.update_layout(
                    title=dict(text="Returns Histogram", font=dict(color='#ffffff', size=16, family='Google Sans Code')),
                    xaxis_title="Return",
                    yaxis_title="Frequency",
                    height=350,
                    **plotly_template['layout']
                )
                st.plotly_chart(fig5, use_container_width=True)
        
        except Exception as e:
            st.error(f"error: {e}")

elif page == "Compare Stocks":
    st.markdown("<h2 style='color: #ffffff; margin-top: 0; margin-bottom: 0.5rem;'>Compare Stocks</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #a0a0a0; margin-bottom: 0.75rem; font-size: 1rem;'>Compare multiple stocks side-by-side with performance metrics and risk analysis</p>", unsafe_allow_html=True)
    
    tickers_str = st.text_input("Tickers (comma separated)", value="AAPL, MSFT, GOOGL")
    period = st.selectbox("Period", ["1mo", "3mo", "6mo", "1y"], index=2)
    
    if st.button("Compare", use_container_width=True):
        tickers = [t.strip().upper() for t in tickers_str.split(",")]
        
        try:
            with st.spinner("Fetching data..."):
                data = st.session_state.fetcher.get_multiple_stocks(tickers, period=period)
            
            if len(data) == 0:
                st.error("no data")
            else:
                results = {}
                for ticker in tickers:
                    try:
                        # yfinance returns multi-index columns for multiple stocks
                        if isinstance(data.columns, pd.MultiIndex):
                            prices = data[('Close', ticker)]
                        else:
                            prices = data['close'] if 'close' in data.columns else data['Close']
                        
                        returns = st.session_state.calc.simple_returns(prices)
                        results[ticker] = {
                            'Return': st.session_state.calc.annualized_return(returns),
                            'Volatility': st.session_state.risk_calc.realized_volatility(returns),
                            'Sharpe': st.session_state.risk_calc.sharpe_ratio(returns),
                            'MaxDD': st.session_state.risk_calc.max_drawdown(returns)
                        }
                    except:
                        continue
                
                if len(results) > 0:
                    df = pd.DataFrame(results).T
                    st.markdown("<h3 style='color: #ffffff; margin-top: 1rem; margin-bottom: 0.5rem;'>Metrics</h3>", unsafe_allow_html=True)
                    st.dataframe(df.style.format({
                        'Return': '{:.2%}',
                        'Volatility': '{:.2%}',
                        'Sharpe': '{:.2f}',
                        'MaxDD': '{:.2%}'
                    }).background_gradient(subset=['Return', 'Sharpe'], cmap='Purples'), use_container_width=True)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        fig = px.scatter(
                            df.reset_index(), 
                            x='Volatility', 
                            y='Return', 
                            text='index', 
                            title="Risk vs Return",
                            color='Sharpe',
                            color_continuous_scale='Purples'
                        )
                        fig.update_traces(textposition="top center", marker_size=12)
                        fig.update_layout(
                            **plotly_template['layout'],
                            height=400
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    
                    with col2:
                        fig2 = go.Figure()
                        fig2.add_trace(go.Bar(
                            x=df.index, 
                            y=df['Sharpe'], 
                            name='Sharpe',
                            marker_color=colors['tekhelet'],
                            marker_line_color=colors['tropical_indigo'],
                            marker_line_width=1
                        ))
                        fig2.update_layout(
                            title=dict(text="Sharpe Ratios", font=dict(color='#ffffff', size=16, family='Google Sans Code')),
                            height=400,
                            **plotly_template['layout']
                        )
                        st.plotly_chart(fig2, use_container_width=True)
                    
                    st.markdown("<h3 style='color: #ffffff; margin-top: 1rem; margin-bottom: 0.5rem;'>Cumulative Returns</h3>", unsafe_allow_html=True)
                    fig3 = go.Figure()
                    chart_colors = [colors['tropical_indigo'], colors['tekhelet'], colors['mountbatten_pink'], colors['brown_sugar']]
                    for i, ticker in enumerate(tickers):
                        try:
                            if isinstance(data.columns, pd.MultiIndex):
                                prices = data[('Close', ticker)]
                            else:
                                prices = data['close'] if 'close' in data.columns else data['Close']
                            returns = st.session_state.calc.simple_returns(prices)
                            cum = st.session_state.calc.cumulative_returns(returns)
                            fig3.add_trace(go.Scatter(
                                x=cum.index, 
                                y=cum, 
                                mode='lines', 
                                name=ticker,
                                line=dict(color=chart_colors[i % len(chart_colors)], width=3)
                            ))
                        except:
                            continue
                    fig3.update_layout(
                        title=dict(text="Cumulative Returns Over Time", font=dict(color='#ffffff', size=16, family='Google Sans Code')),
                        height=450,
                        **plotly_template['layout']
                    )
                    st.plotly_chart(fig3, use_container_width=True)
        
        except Exception as e:
            st.error(f"error: {e}")

elif page == "Risk Metrics":
    st.markdown("<h2 style='color: #ffffff; margin-top: 0; margin-bottom: 0.5rem;'>Risk Metrics</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #a0a0a0; margin-bottom: 0.75rem; font-size: 1rem;'>Calculate volatility, Sharpe ratio, VaR, and other risk metrics for your portfolio</p>", unsafe_allow_html=True)
    
    ticker = st.text_input("Ticker", value="AAPL")
    period = st.selectbox("Period", ["3mo", "6mo", "1y", "2y"], index=2)
    rf_rate = st.slider("Risk free rate (%)", 0.0, 10.0, 2.0, 0.1) / 100
    
    if st.button("Calculate", use_container_width=True):
        try:
            with st.spinner("Calculating..."):
                data = st.session_state.fetcher.get_stock_data(ticker, period=period)
                returns = st.session_state.calc.simple_returns(data['close'])
                
                ann_return = st.session_state.calc.annualized_return(returns)
                vol = st.session_state.risk_calc.realized_volatility(returns)
                sharpe = st.session_state.risk_calc.sharpe_ratio(returns, rf_rate)
                max_dd = st.session_state.risk_calc.max_drawdown(returns)
                var_95 = st.session_state.risk_calc.var(returns, 0.05)
                cvar_95 = st.session_state.risk_calc.cvar(returns, 0.05)
                
                st.markdown(f"<h3 style='color: #ffffff; margin-top: 1rem; margin-bottom: 0.5rem;'>Metrics for {ticker}</h3>", unsafe_allow_html=True)
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Return", f"{ann_return:.2%}")
                    st.metric("Sharpe", f"{sharpe:.2f}")
                with col2:
                    st.metric("Volatility", f"{vol:.2%}")
                    st.metric("Max Drawdown", f"{max_dd:.2%}")
                with col3:
                    st.metric("VaR (95%)", f"{var_95:.2%}")
                    st.metric("CVaR (95%)", f"{cvar_95:.2%}")
                
                st.markdown("<h3 style='color: #ffffff; margin-top: 1rem; margin-bottom: 0.5rem;'>Rolling Volatility</h3>", unsafe_allow_html=True)
                rolling_vol = st.session_state.risk_calc.rolling_volatility(returns, 30)
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=rolling_vol.index, 
                    y=rolling_vol, 
                    mode='lines', 
                    name='30-day Vol',
                    line=dict(color=colors['tropical_indigo'], width=2),
                    fill='tozeroy',
                    fillcolor=f"rgba(153, 132, 212, 0.2)"
                ))
                fig.add_hline(
                    y=vol, 
                    line_dash="dash", 
                    annotation_text="Average Volatility",
                    line_color=colors['tekhelet']
                )
                fig.update_layout(
                    title=dict(text="Rolling Volatility", font=dict(color='#ffffff', size=16, family='Google Sans Code')),
                    height=400,
                    **plotly_template['layout']
                )
                st.plotly_chart(fig, use_container_width=True)
                
                st.markdown("<h3 style='color: #ffffff; margin-top: 1rem; margin-bottom: 0.5rem;'>Drawdown</h3>", unsafe_allow_html=True)
                cum = (1 + returns).cumprod()
                running_max = cum.expanding().max()
                drawdown = (cum - running_max) / running_max
                fig2 = go.Figure()
                fig2.add_trace(go.Scatter(
                    x=drawdown.index, 
                    y=drawdown, 
                    mode='lines', 
                    fill='tozeroy', 
                    name='Drawdown',
                    line=dict(color=colors['mountbatten_pink']),
                    fillcolor=f"rgba(166, 128, 157, 0.2)"
                ))
                fig2.update_layout(
                    title=dict(text="Portfolio Drawdown", font=dict(color='#ffffff', size=16, family='Google Sans Code')),
                    height=350,
                    **plotly_template['layout']
                )
                st.plotly_chart(fig2, use_container_width=True)
        
        except Exception as e:
            st.error(f"error: {e}")
