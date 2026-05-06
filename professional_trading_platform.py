"""
PROFESSIONAL TRADING PLATFORM - Institutional Grade
Market-Standard Analysis & Trading Tools
Built with Industry Best Practices
"""

import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
import time
import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Check for optional libraries
try:
    import quantstats as qs
    QUANTSTATS_AVAILABLE = True
except:
    QUANTSTATS_AVAILABLE = False

try:
    import pandas_ta as pta
    PANDAS_TA_AVAILABLE = True
except:
    PANDAS_TA_AVAILABLE = False

try:
    from newsapi import NewsApiClient
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    NEWS_AVAILABLE = True
except:
    NEWS_AVAILABLE = False

warnings.filterwarnings('ignore')

# API Keys — set via .env file or environment variables
NEWS_API_KEY = os.getenv('NEWS_API_KEY', '')
FINNHUB_API_KEY = os.getenv('FINNHUB_API_KEY', '')

# ==================== PAGE CONFIGURATION ====================

st.set_page_config(
    page_title="Professional Trading Platform",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional CSS
st.markdown("""
<style>
    /* Dark theme professional colors */
    :root {
        --bg-primary: #0e1117;
        --bg-secondary: #262730;
        --text-primary: #fafafa;
        --accent-green: #26a69a;
        --accent-red: #ef5350;
        --accent-blue: #42a5f5;
    }
    
    .main-header {
        font-size: 2.8rem;
        font-weight: 700;
        background: linear-gradient(120deg, #42a5f5, #26a69a);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    .subtitle {
        text-align: center;
        color: #9e9e9e;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        margin: 0.5rem 0;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        background-color: var(--bg-secondary);
        padding: 0.5rem;
        border-radius: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        border-radius: 6px;
        color: white;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(120deg, #42a5f5, #26a69a);
    }
    
    /* Professional data tables */
    .dataframe {
        font-size: 0.9rem;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: var(--bg-secondary);
    }
</style>
""", unsafe_allow_html=True)

# ==================== PROFESSIONAL DATA FETCHING ====================

@st.cache_data(ttl=3600)
def fetch_professional_data(symbol, period='2y', interval='1d'):
    """Fetch data with professional error handling"""
    try:
        df = None

        # Try ticker.history with retries (rate-limit resilient)
        for attempt in range(3):
            try:
                ticker = yf.Ticker(symbol)
                df = ticker.history(period=period, interval=interval)
                if df is not None and not df.empty:
                    if isinstance(df.columns, pd.MultiIndex):
                        df.columns = df.columns.get_level_values(0)
                    break
            except Exception:
                df = None
            if attempt < 2:
                time.sleep(1)

        # Fallback to shorter periods if full period fails
        if df is None or df.empty:
            for fallback_period in ['1y', '6mo', '1mo']:
                if fallback_period == period:
                    continue
                try:
                    ticker = yf.Ticker(symbol)
                    df = ticker.history(period=fallback_period, interval=interval)
                    if df is not None and not df.empty:
                        if isinstance(df.columns, pd.MultiIndex):
                            df.columns = df.columns.get_level_values(0)
                        break
                except Exception:
                    df = None

        # Last resort: yf.download
        if df is None or df.empty:
            try:
                df = yf.download(symbol, period=period, interval=interval,
                                 progress=False, auto_adjust=True)
                if df is not None and not df.empty:
                    if isinstance(df.columns, pd.MultiIndex):
                        df.columns = df.columns.get_level_values(0)
            except Exception:
                pass
        
        if df is None or df.empty:
            st.error(f"❌ Could not fetch data for {symbol}. Please check:\n"
                    f"- Symbol is correct (e.g., MSFT, GOOGL, TSLA)\n"
                    f"- You have internet connection\n"
                    f"- Yahoo Finance is accessible\n"
                    f"- Try a different symbol from the Popular Symbols list")
            return None, None
        
        # Get company info with error handling
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            company_info = {
                'name': info.get('longName', info.get('shortName', symbol)),
                'sector': info.get('sector', 'N/A'),
                'industry': info.get('industry', 'N/A'),
                'marketCap': info.get('marketCap', 0),
                'pe': info.get('trailingPE', 0),
                'forwardPE': info.get('forwardPE', 0),
                'beta': info.get('beta', 1.0),
                'dividendYield': info.get('dividendYield', 0),
                'fiftyTwoWeekHigh': info.get('fiftyTwoWeekHigh', 0),
                'fiftyTwoWeekLow': info.get('fiftyTwoWeekLow', 0),
                'avgVolume': info.get('averageVolume', 0)
            }
        except Exception as e:
            # Fallback company info from data
            company_info = {
                'name': symbol,
                'sector': 'N/A',
                'industry': 'N/A',
                'marketCap': 0,
                'pe': 0,
                'forwardPE': 0,
                'beta': 1.0,
                'dividendYield': 0,
                'fiftyTwoWeekHigh': float(df['High'].max()) if 'High' in df.columns and not df.empty else 0,
                'fiftyTwoWeekLow': float(df['Low'].min()) if 'Low' in df.columns and not df.empty else 0,
                'avgVolume': float(df['Volume'].mean()) if 'Volume' in df.columns and not df.empty else 0
            }
        
        return df, company_info
    except Exception as e:
        st.error(f"Error fetching {symbol}: {str(e)}")
        return None, None

# ==================== PROFESSIONAL TECHNICAL ANALYSIS ====================

def calculate_professional_indicators(df):
    """Calculate institutional-grade technical indicators"""
    try:
        data = df.copy()
        
        if not PANDAS_TA_AVAILABLE:
            # Use simple pandas calculations if pandas_ta not available
            data['SMA_20'] = data['Close'].rolling(window=20).mean()
            data['SMA_50'] = data['Close'].rolling(window=50).mean()
            data['SMA_200'] = data['Close'].rolling(window=200).mean()
            data['EMA_12'] = data['Close'].ewm(span=12, adjust=False).mean()
            data['EMA_26'] = data['Close'].ewm(span=26, adjust=False).mean()
            
            # Simple RSI calculation
            delta = data['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            data['RSI'] = 100 - (100 / (1 + rs))
            
            # Simple MACD
            data['MACD_12_26_9'] = data['EMA_12'] - data['EMA_26']
            data['MACDs_12_26_9'] = data['MACD_12_26_9'].ewm(span=9, adjust=False).mean()
            data['MACDh_12_26_9'] = data['MACD_12_26_9'] - data['MACDs_12_26_9']
            
            # Simple Bollinger Bands
            data['BBM_20_2.0'] = data['Close'].rolling(window=20).mean()
            std = data['Close'].rolling(window=20).std()
            data['BBU_20_2.0'] = data['BBM_20_2.0'] + (std * 2)
            data['BBL_20_2.0'] = data['BBM_20_2.0'] - (std * 2)
            
            # Simple ATR
            high_low = data['High'] - data['Low']
            high_close = np.abs(data['High'] - data['Close'].shift())
            low_close = np.abs(data['Low'] - data['Close'].shift())
            ranges = pd.concat([high_low, high_close, low_close], axis=1)
            true_range = np.max(ranges, axis=1)
            data['ATR'] = true_range.rolling(14).mean()
            
            return data
        
        # Moving Averages (Industry Standard)
        data['SMA_20'] = pta.sma(data['Close'], length=20)
        data['SMA_50'] = pta.sma(data['Close'], length=50)
        data['SMA_200'] = pta.sma(data['Close'], length=200)
        data['EMA_12'] = pta.ema(data['Close'], length=12)
        data['EMA_26'] = pta.ema(data['Close'], length=26)
        
        # MACD (Standard Settings: 12, 26, 9)
        macd = pta.macd(data['Close'], fast=12, slow=26, signal=9)
        if macd is not None:
            data = pd.concat([data, macd], axis=1)
        
        # RSI (14-period standard)
        data['RSI'] = pta.rsi(data['Close'], length=14)
        
        # Bollinger Bands (20, 2)
        bbands = pta.bbands(data['Close'], length=20, std=2)
        if bbands is not None:
            data = pd.concat([data, bbands], axis=1)
        
        # ATR (14-period for volatility)
        data['ATR'] = pta.atr(data['High'], data['Low'], data['Close'], length=14)
        
        # ADX (Trend Strength)
        adx = pta.adx(data['High'], data['Low'], data['Close'], length=14)
        if adx is not None:
            data = pd.concat([data, adx], axis=1)
        
        # OBV (Volume Analysis)
        data['OBV'] = pta.obv(data['Close'], data['Volume'])
        
        # VWAP (Intraday benchmark)
        data['VWAP'] = pta.vwap(data['High'], data['Low'], data['Close'], data['Volume'])
        
        # Stochastic Oscillator
        stoch = pta.stoch(data['High'], data['Low'], data['Close'], k=14, d=3)
        if stoch is not None:
            data = pd.concat([data, stoch], axis=1)
        
        return data
    except Exception as e:
        st.warning(f"Indicator calculation warning: {str(e)}")
        return df

# ==================== PROFESSIONAL CHARTING ====================

def create_professional_chart(df, symbol, show_volume=True):
    """Create TradingView-style professional chart"""
    try:
        # Determine number of rows
        rows = 4 if show_volume else 3
        row_heights = [0.5, 0.15, 0.15, 0.2] if show_volume else [0.6, 0.2, 0.2]
        
        fig = make_subplots(
            rows=rows, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.03,
            subplot_titles=(f'{symbol} - Price Action', 'MACD', 'RSI', 'Volume') if show_volume else (f'{symbol} - Price Action', 'MACD', 'RSI'),
            row_heights=row_heights
        )
        
        # Candlestick Chart
        fig.add_trace(go.Candlestick(
            x=df.index,
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Close'],
            name='OHLC',
            increasing_line_color='#26a69a',
            decreasing_line_color='#ef5350'
        ), row=1, col=1)
        
        # Moving Averages
        if 'SMA_20' in df.columns:
            fig.add_trace(go.Scatter(
                x=df.index, y=df['SMA_20'],
                name='SMA 20', line=dict(color='#ffa726', width=1.5)
            ), row=1, col=1)
        
        if 'SMA_50' in df.columns:
            fig.add_trace(go.Scatter(
                x=df.index, y=df['SMA_50'],
                name='SMA 50', line=dict(color='#42a5f5', width=1.5)
            ), row=1, col=1)
        
        if 'SMA_200' in df.columns:
            fig.add_trace(go.Scatter(
                x=df.index, y=df['SMA_200'],
                name='SMA 200', line=dict(color='#ab47bc', width=2)
            ), row=1, col=1)
        
        # Bollinger Bands
        if 'BBL_20_2.0' in df.columns and 'BBU_20_2.0' in df.columns:
            fig.add_trace(go.Scatter(
                x=df.index, y=df['BBU_20_2.0'],
                name='BB Upper', line=dict(color='gray', width=1, dash='dash'),
                showlegend=False
            ), row=1, col=1)
            
            fig.add_trace(go.Scatter(
                x=df.index, y=df['BBL_20_2.0'],
                name='BB Lower', line=dict(color='gray', width=1, dash='dash'),
                fill='tonexty', fillcolor='rgba(128,128,128,0.1)',
                showlegend=False
            ), row=1, col=1)
        
        # MACD
        if 'MACD_12_26_9' in df.columns:
            fig.add_trace(go.Scatter(
                x=df.index, y=df['MACD_12_26_9'],
                name='MACD', line=dict(color='#42a5f5', width=2)
            ), row=2, col=1)
            
            if 'MACDs_12_26_9' in df.columns:
                fig.add_trace(go.Scatter(
                    x=df.index, y=df['MACDs_12_26_9'],
                    name='Signal', line=dict(color='#ef5350', width=2)
                ), row=2, col=1)
            
            if 'MACDh_12_26_9' in df.columns:
                colors = ['#26a69a' if val >= 0 else '#ef5350' for val in df['MACDh_12_26_9']]
                fig.add_trace(go.Bar(
                    x=df.index, y=df['MACDh_12_26_9'],
                    name='Histogram', marker_color=colors
                ), row=2, col=1)
        
        # RSI
        if 'RSI' in df.columns:
            fig.add_trace(go.Scatter(
                x=df.index, y=df['RSI'],
                name='RSI', line=dict(color='#ab47bc', width=2)
            ), row=3, col=1)
            
            fig.add_hline(y=70, line_dash="dash", line_color="#ef5350", row=3, col=1, opacity=0.5)
            fig.add_hline(y=30, line_dash="dash", line_color="#26a69a", row=3, col=1, opacity=0.5)
            fig.add_hrect(y0=30, y1=70, fillcolor="gray", opacity=0.1, row=3, col=1)
        
        # Volume
        if show_volume:
            colors = ['#26a69a' if df['Close'].iloc[i] >= df['Open'].iloc[i] else '#ef5350' 
                     for i in range(len(df))]
            fig.add_trace(go.Bar(
                x=df.index, y=df['Volume'],
                name='Volume', marker_color=colors, opacity=0.7
            ), row=4, col=1)
        
        # Layout
        fig.update_layout(
            height=900,
            showlegend=True,
            xaxis_rangeslider_visible=False,
            hovermode='x unified',
            template='plotly_dark',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        fig.update_xaxes(title_text="Date", row=rows, col=1)
        fig.update_yaxes(title_text="Price", row=1, col=1)
        fig.update_yaxes(title_text="MACD", row=2, col=1)
        fig.update_yaxes(title_text="RSI", row=3, col=1)
        if show_volume:
            fig.update_yaxes(title_text="Volume", row=4, col=1)
        
        return fig
    except Exception as e:
        st.error(f"Chart creation error: {str(e)}")
        return None

# ==================== PROFESSIONAL ANALYSIS FUNCTIONS ====================

def generate_trading_signals(df):
    """Generate 20+ professional trading signals"""
    try:
        signals = []
        latest = df.iloc[-1]
        prev = df.iloc[-2]
        
        # === TREND ANALYSIS (5 signals) ===
        if 'SMA_50' in df.columns and 'SMA_200' in df.columns:
            # 1. Overall Trend
            if latest['Close'] > latest['SMA_50'] > latest['SMA_200']:
                signals.append(("🟢 STRONG UPTREND", "Price > SMA 50 > SMA 200 (Bullish alignment)", "BULLISH"))
            elif latest['Close'] < latest['SMA_50'] < latest['SMA_200']:
                signals.append(("🔴 STRONG DOWNTREND", "Price < SMA 50 < SMA 200 (Bearish alignment)", "BEARISH"))
            else:
                signals.append(("⚪ MIXED TREND", "Moving averages not aligned", "NEUTRAL"))
            
            # 2. Golden/Death Cross
            if latest['SMA_50'] > latest['SMA_200'] and prev['SMA_50'] <= prev['SMA_200']:
                signals.append(("🟢 GOLDEN CROSS", "SMA 50 crossed above SMA 200 - Major bullish signal", "VERY BULLISH"))
            elif latest['SMA_50'] < latest['SMA_200'] and prev['SMA_50'] >= prev['SMA_200']:
                signals.append(("🔴 DEATH CROSS", "SMA 50 crossed below SMA 200 - Major bearish signal", "VERY BEARISH"))
        
        # 3. Short-term Trend (SMA 20)
        if 'SMA_20' in df.columns:
            if latest['Close'] > latest['SMA_20']:
                distance = ((latest['Close'] / latest['SMA_20']) - 1) * 100
                signals.append(("🟢 ABOVE SMA 20", f"Price {distance:.1f}% above 20-day average", "BULLISH"))
            else:
                distance = ((latest['Close'] / latest['SMA_20']) - 1) * 100
                signals.append(("🔴 BELOW SMA 20", f"Price {distance:.1f}% below 20-day average", "BEARISH"))
        
        # 4. Price vs SMA 50
        if 'SMA_50' in df.columns:
            if latest['Close'] > latest['SMA_50']:
                signals.append(("🟢 ABOVE SMA 50", "Price above 50-day average (Medium-term bullish)", "BULLISH"))
            else:
                signals.append(("🔴 BELOW SMA 50", "Price below 50-day average (Medium-term bearish)", "BEARISH"))
        
        # 5. Price vs SMA 200
        if 'SMA_200' in df.columns:
            if latest['Close'] > latest['SMA_200']:
                signals.append(("🟢 ABOVE SMA 200", "Price above 200-day average (Long-term bullish)", "BULLISH"))
            else:
                signals.append(("🔴 BELOW SMA 200", "Price below 200-day average (Long-term bearish)", "BEARISH"))
        
        # === MOMENTUM ANALYSIS (6 signals) ===
        
        # 6-7. RSI Analysis
        if 'RSI' in df.columns:
            rsi = latest['RSI']
            prev_rsi = prev['RSI']
            
            if rsi > 70:
                signals.append(("⚠️ RSI OVERBOUGHT", f"RSI at {rsi:.1f} (>70) - Potential reversal", "CAUTION"))
            elif rsi < 30:
                signals.append(("💡 RSI OVERSOLD", f"RSI at {rsi:.1f} (<30) - Potential bounce", "OPPORTUNITY"))
            elif 40 <= rsi <= 60:
                signals.append(("⚪ RSI NEUTRAL", f"RSI at {rsi:.1f} (40-60 range)", "NEUTRAL"))
            elif rsi > 60:
                signals.append(("🟢 RSI BULLISH", f"RSI at {rsi:.1f} (Strong momentum)", "BULLISH"))
            else:
                signals.append(("🔴 RSI BEARISH", f"RSI at {rsi:.1f} (Weak momentum)", "BEARISH"))
            
            # RSI Divergence
            if rsi > prev_rsi and latest['Close'] < prev['Close']:
                signals.append(("💡 BULLISH RSI DIVERGENCE", "RSI rising while price falling - Potential reversal", "OPPORTUNITY"))
            elif rsi < prev_rsi and latest['Close'] > prev['Close']:
                signals.append(("⚠️ BEARISH RSI DIVERGENCE", "RSI falling while price rising - Potential reversal", "CAUTION"))
        
        # 8-9. MACD Analysis
        if 'MACD_12_26_9' in df.columns and 'MACDs_12_26_9' in df.columns:
            macd = latest['MACD_12_26_9']
            signal = latest['MACDs_12_26_9']
            prev_macd = prev['MACD_12_26_9']
            prev_signal = prev['MACDs_12_26_9']
            
            # MACD Crossover
            if macd > signal and prev_macd <= prev_signal:
                signals.append(("🟢 MACD BULLISH CROSS", "MACD crossed above signal - Buy signal", "BUY SIGNAL"))
            elif macd < signal and prev_macd >= prev_signal:
                signals.append(("🔴 MACD BEARISH CROSS", "MACD crossed below signal - Sell signal", "SELL SIGNAL"))
            
            # MACD Position
            if macd > 0 and signal > 0:
                signals.append(("🟢 MACD POSITIVE", "Both MACD and signal above zero (Bullish)", "BULLISH"))
            elif macd < 0 and signal < 0:
                signals.append(("🔴 MACD NEGATIVE", "Both MACD and signal below zero (Bearish)", "BEARISH"))
        
        # 10. Stochastic
        if 'STOCHk_14_3_3' in df.columns:
            stoch_k = latest['STOCHk_14_3_3']
            if stoch_k > 80:
                signals.append(("⚠️ STOCHASTIC OVERBOUGHT", f"Stochastic at {stoch_k:.1f} (>80)", "CAUTION"))
            elif stoch_k < 20:
                signals.append(("💡 STOCHASTIC OVERSOLD", f"Stochastic at {stoch_k:.1f} (<20)", "OPPORTUNITY"))
        
        # 11. ADX (Trend Strength)
        if 'ADX_14' in df.columns:
            adx = latest['ADX_14']
            if adx > 25:
                signals.append(("🔥 STRONG TREND", f"ADX at {adx:.1f} (>25) - Trend is strong", "SIGNIFICANT"))
            elif adx < 20:
                signals.append(("⚪ WEAK TREND", f"ADX at {adx:.1f} (<20) - No clear trend", "NEUTRAL"))
        
        # === VOLATILITY ANALYSIS (4 signals) ===
        
        # 12-13. Bollinger Bands
        if 'BBL_20_2.0' in df.columns and 'BBU_20_2.0' in df.columns:
            bb_upper = latest['BBU_20_2.0']
            bb_lower = latest['BBL_20_2.0']
            bb_mid = latest['BBM_20_2.0']
            
            if latest['Close'] > bb_upper:
                signals.append(("⚠️ ABOVE UPPER BB", "Price extended beyond upper band - Overbought", "OVERBOUGHT"))
            elif latest['Close'] < bb_lower:
                signals.append(("💡 BELOW LOWER BB", "Price extended beyond lower band - Oversold", "OVERSOLD"))
            elif latest['Close'] > bb_mid:
                signals.append(("🟢 ABOVE BB MIDDLE", "Price above middle band (Bullish)", "BULLISH"))
            else:
                signals.append(("🔴 BELOW BB MIDDLE", "Price below middle band (Bearish)", "BEARISH"))
            
            # BB Squeeze
            bb_width = ((bb_upper - bb_lower) / bb_mid) * 100
            if bb_width < 10:
                signals.append(("🔥 BB SQUEEZE", f"Bands narrowing ({bb_width:.1f}%) - Breakout imminent", "SIGNIFICANT"))
        
        # 14. ATR (Volatility)
        if 'ATR' in df.columns:
            atr = latest['ATR']
            atr_pct = (atr / latest['Close']) * 100
            if atr_pct > 3:
                signals.append(("⚠️ HIGH VOLATILITY", f"ATR at {atr_pct:.1f}% of price - High risk", "CAUTION"))
            elif atr_pct < 1:
                signals.append(("⚪ LOW VOLATILITY", f"ATR at {atr_pct:.1f}% of price - Low movement", "NEUTRAL"))
        
        # === VOLUME ANALYSIS (3 signals) ===
        
        # 15. Volume Spike
        if 'Volume' in df.columns:
            avg_volume = df['Volume'].rolling(20).mean().iloc[-1]
            current_volume = latest['Volume']
            volume_ratio = current_volume / avg_volume
            
            if volume_ratio > 2:
                signals.append(("🔥 EXTREME VOLUME", f"Volume {(volume_ratio-1)*100:.0f}% above average - Major activity", "VERY SIGNIFICANT"))
            elif volume_ratio > 1.5:
                signals.append(("📊 HIGH VOLUME", f"Volume {(volume_ratio-1)*100:.0f}% above average - Increased activity", "SIGNIFICANT"))
            elif volume_ratio < 0.5:
                signals.append(("⚪ LOW VOLUME", f"Volume {(1-volume_ratio)*100:.0f}% below average - Low interest", "NEUTRAL"))
        
        # 16. OBV Trend
        if 'OBV' in df.columns:
            obv_sma = df['OBV'].rolling(20).mean()
            if latest['OBV'] > obv_sma.iloc[-1]:
                signals.append(("🟢 OBV BULLISH", "On-Balance Volume above average (Accumulation)", "BULLISH"))
            else:
                signals.append(("🔴 OBV BEARISH", "On-Balance Volume below average (Distribution)", "BEARISH"))
        
        # 17. Volume Confirmation
        if 'Volume' in df.columns:
            price_change = latest['Close'] - prev['Close']
            volume_change = latest['Volume'] - prev['Volume']
            
            if price_change > 0 and volume_change > 0:
                signals.append(("🟢 VOLUME CONFIRMS UP", "Price up with increasing volume (Strong)", "BULLISH"))
            elif price_change < 0 and volume_change > 0:
                signals.append(("🔴 VOLUME CONFIRMS DOWN", "Price down with increasing volume (Weak)", "BEARISH"))
            elif price_change > 0 and volume_change < 0:
                signals.append(("⚠️ WEAK RALLY", "Price up but volume decreasing (Suspect)", "CAUTION"))
        
        # === PRICE ACTION (3 signals) ===
        
        # 18. Daily Change
        daily_change = ((latest['Close'] - prev['Close']) / prev['Close']) * 100
        if daily_change > 2:
            signals.append(("🟢 STRONG GAIN", f"Price up {daily_change:.1f}% today", "BULLISH"))
        elif daily_change < -2:
            signals.append(("🔴 STRONG DECLINE", f"Price down {daily_change:.1f}% today", "BEARISH"))
        elif daily_change > 0:
            signals.append(("🟢 MODEST GAIN", f"Price up {daily_change:.1f}% today", "BULLISH"))
        else:
            signals.append(("🔴 MODEST DECLINE", f"Price down {daily_change:.1f}% today", "BEARISH"))
        
        # 19. 52-Week Position
        high_52w = df['High'].rolling(252).max().iloc[-1]
        low_52w = df['Low'].rolling(252).min().iloc[-1]
        position = ((latest['Close'] - low_52w) / (high_52w - low_52w)) * 100
        
        if position > 80:
            signals.append(("🔥 NEAR 52W HIGH", f"Price at {position:.0f}% of 52-week range", "VERY BULLISH"))
        elif position < 20:
            signals.append(("💡 NEAR 52W LOW", f"Price at {position:.0f}% of 52-week range", "OPPORTUNITY"))
        elif position > 50:
            signals.append(("🟢 UPPER HALF", f"Price at {position:.0f}% of 52-week range", "BULLISH"))
        else:
            signals.append(("🔴 LOWER HALF", f"Price at {position:.0f}% of 52-week range", "BEARISH"))
        
        # 20. Support/Resistance
        recent_high = df['High'].rolling(20).max().iloc[-1]
        recent_low = df['Low'].rolling(20).min().iloc[-1]
        
        if latest['Close'] >= recent_high * 0.99:
            signals.append(("🔥 AT RESISTANCE", f"Price near 20-day high (${recent_high:.2f})", "SIGNIFICANT"))
        elif latest['Close'] <= recent_low * 1.01:
            signals.append(("💡 AT SUPPORT", f"Price near 20-day low (${recent_low:.2f})", "SIGNIFICANT"))
        
        # === VWAP (1 signal) ===
        
        # 21. VWAP
        if 'VWAP' in df.columns:
            if latest['Close'] > latest['VWAP']:
                signals.append(("🟢 ABOVE VWAP", "Price above Volume-Weighted Average Price (Institutional buying)", "BULLISH"))
            else:
                signals.append(("🔴 BELOW VWAP", "Price below Volume-Weighted Average Price (Institutional selling)", "BEARISH"))
        
        return signals
    except Exception as e:
        return [("⚠️ ERROR", f"Signal generation failed: {str(e)}", "ERROR")]

def calculate_risk_metrics(df):
    """Calculate professional risk metrics"""
    try:
        returns = df['Close'].pct_change().dropna()
        
        if QUANTSTATS_AVAILABLE:
            # Use QuantStats if available
            sharpe = qs.stats.sharpe(returns)
            sortino = qs.stats.sortino(returns)
            max_dd = qs.stats.max_drawdown(returns)
            calmar = qs.stats.calmar(returns)
        else:
            # Manual calculations if QuantStats not available
            # Sharpe Ratio (annualized)
            sharpe = (returns.mean() / returns.std()) * np.sqrt(252) if returns.std() != 0 else 0
            
            # Sortino Ratio (downside deviation)
            downside_returns = returns[returns < 0]
            downside_std = downside_returns.std() * np.sqrt(252)
            sortino = (returns.mean() * 252) / downside_std if downside_std != 0 else 0
            
            # Max Drawdown
            cumulative = (1 + returns).cumprod()
            running_max = cumulative.expanding().max()
            drawdown = (cumulative - running_max) / running_max
            max_dd = drawdown.min()
            
            # Calmar Ratio
            annual_return = returns.mean() * 252
            calmar = annual_return / abs(max_dd) if max_dd != 0 else 0
        
        # Volatility (annualized)
        volatility = returns.std() * np.sqrt(252)
        
        # Value at Risk (95%)
        var_95 = np.percentile(returns, 5)
        
        # Win Rate
        win_rate = len(returns[returns > 0]) / len(returns) * 100
        
        return {
            'sharpe': sharpe,
            'sortino': sortino,
            'max_drawdown': max_dd,
            'volatility': volatility,
            'var_95': var_95,
            'calmar': calmar,
            'win_rate': win_rate
        }
    except Exception as e:
        st.warning(f"Risk calculation error: {str(e)}")
        return None


# ==================== SENTIMENT ANALYSIS ====================

def fetch_news_articles(symbol, company_name):
    """Fetch news articles for sentiment analysis - Get 20 relevant articles"""
    try:
        if not NEWS_AVAILABLE:
            return None
        
        newsapi = NewsApiClient(api_key=NEWS_API_KEY)
        
        # Try multiple search strategies to get enough articles
        all_articles = []
        
        # Strategy 1: Search by company name
        try:
            articles1 = newsapi.get_everything(
                q=f'"{company_name}"',
                language='en',
                sort_by='publishedAt',
                page_size=20
            )
            if articles1 and 'articles' in articles1:
                all_articles.extend(articles1['articles'])
        except:
            pass
        
        # Strategy 2: Search by symbol (if we don't have enough)
        if len(all_articles) < 20:
            try:
                articles2 = newsapi.get_everything(
                    q=f'{symbol} stock',
                    language='en',
                    sort_by='publishedAt',
                    page_size=20
                )
                if articles2 and 'articles' in articles2:
                    # Add articles that aren't duplicates
                    existing_urls = {a.get('url') for a in all_articles}
                    for article in articles2['articles']:
                        if article.get('url') not in existing_urls:
                            all_articles.append(article)
                            if len(all_articles) >= 20:
                                break
            except:
                pass
        
        # Strategy 3: Broader search if still not enough
        if len(all_articles) < 20:
            try:
                # Extract first word of company name for broader search
                first_word = company_name.split()[0] if company_name else symbol
                articles3 = newsapi.get_everything(
                    q=f'{first_word}',
                    language='en',
                    sort_by='publishedAt',
                    page_size=30
                )
                if articles3 and 'articles' in articles3:
                    existing_urls = {a.get('url') for a in all_articles}
                    for article in articles3['articles']:
                        if article.get('url') not in existing_urls:
                            all_articles.append(article)
                            if len(all_articles) >= 20:
                                break
            except:
                pass
        
        # Clean and validate articles
        valid_articles = []
        for article in all_articles:
            try:
                # Ensure article has required fields
                if article.get('title') and article.get('url'):
                    valid_articles.append(article)
                    if len(valid_articles) >= 20:
                        break
            except:
                continue
        
        return valid_articles[:20] if valid_articles else None
        
    except Exception as e:
        st.warning(f"Could not fetch news: {str(e)}")
        return None

def analyze_sentiment_score(text):
    """Analyze sentiment using VADER"""
    try:
        if not NEWS_AVAILABLE:
            return 0
        
        analyzer = SentimentIntensityAnalyzer()
        scores = analyzer.polarity_scores(text)
        return scores['compound']  # Returns -1 to +1
    except:
        return 0

def generate_sentiment_recommendation(avg_sentiment, sentiment_strength):
    """Generate buy/sell/hold recommendation based on sentiment"""
    
    # Strong signals
    if avg_sentiment > 0.3 and sentiment_strength == "VERY POSITIVE":
        return "STRONG BUY", "🟢🟢🟢", "Very positive news sentiment with strong conviction"
    elif avg_sentiment > 0.15:
        return "BUY", "🟢🟢", "Positive news sentiment suggests upward momentum"
    elif avg_sentiment > 0.05:
        return "WEAK BUY", "🟢", "Slightly positive sentiment, consider accumulating"
    elif avg_sentiment < -0.3 and sentiment_strength == "VERY NEGATIVE":
        return "STRONG SELL", "🔴🔴🔴", "Very negative news sentiment with strong conviction"
    elif avg_sentiment < -0.15:
        return "SELL", "🔴🔴", "Negative news sentiment suggests downward pressure"
    elif avg_sentiment < -0.05:
        return "WEAK SELL", "🔴", "Slightly negative sentiment, consider reducing position"
    else:
        return "HOLD", "⚪", "Neutral sentiment, maintain current position"

def calculate_sentiment_metrics(articles):
    """Calculate comprehensive sentiment metrics"""
    try:
        if not articles:
            return None
        
        sentiments = []
        positive_count = 0
        negative_count = 0
        neutral_count = 0
        
        article_sentiments = []
        
        for article in articles:
            title = article.get('title', '')
            description = article.get('description', '')
            text = f"{title} {description}"
            
            if text:
                sentiment = analyze_sentiment_score(text)
                sentiments.append(sentiment)
                
                article_sentiments.append({
                    'title': title,
                    'sentiment': sentiment,
                    'url': article.get('url', ''),
                    'published': article.get('publishedAt', ''),
                    'source': article.get('source', {}).get('name', 'Unknown')
                })
                
                if sentiment > 0.05:
                    positive_count += 1
                elif sentiment < -0.05:
                    negative_count += 1
                else:
                    neutral_count += 1
        
        if not sentiments:
            return None
        
        avg_sentiment = np.mean(sentiments)
        sentiment_std = np.std(sentiments)
        
        # Determine sentiment strength
        if abs(avg_sentiment) > 0.3:
            strength = "VERY POSITIVE" if avg_sentiment > 0 else "VERY NEGATIVE"
        elif abs(avg_sentiment) > 0.15:
            strength = "POSITIVE" if avg_sentiment > 0 else "NEGATIVE"
        elif abs(avg_sentiment) > 0.05:
            strength = "SLIGHTLY POSITIVE" if avg_sentiment > 0 else "SLIGHTLY NEGATIVE"
        else:
            strength = "NEUTRAL"
        
        # Calculate sentiment trend (recent vs older)
        recent_sentiment = np.mean(sentiments[:5]) if len(sentiments) >= 5 else avg_sentiment
        older_sentiment = np.mean(sentiments[5:]) if len(sentiments) > 5 else avg_sentiment
        sentiment_trend = recent_sentiment - older_sentiment
        
        return {
            'avg_sentiment': avg_sentiment,
            'sentiment_std': sentiment_std,
            'strength': strength,
            'positive_count': positive_count,
            'negative_count': negative_count,
            'neutral_count': neutral_count,
            'total_articles': len(sentiments),
            'sentiment_trend': sentiment_trend,
            'article_sentiments': article_sentiments
        }
    except Exception as e:
        st.error(f"Error calculating sentiment: {str(e)}")
        return None

def plot_sentiment_distribution(article_sentiments):
    """Plot sentiment distribution"""
    try:
        sentiments = [a['sentiment'] for a in article_sentiments]
        
        fig = go.Figure()
        
        # Histogram
        fig.add_trace(go.Histogram(
            x=sentiments,
            nbinsx=20,
            name='Sentiment Distribution',
            marker_color='#42a5f5',
            opacity=0.7
        ))
        
        # Add vertical lines for thresholds
        fig.add_vline(x=0, line_dash="dash", line_color="white", annotation_text="Neutral")
        fig.add_vline(x=0.05, line_dash="dot", line_color="green", annotation_text="Positive")
        fig.add_vline(x=-0.05, line_dash="dot", line_color="red", annotation_text="Negative")
        
        fig.update_layout(
            title='News Sentiment Distribution',
            xaxis_title='Sentiment Score',
            yaxis_title='Number of Articles',
            height=400,
            template='plotly_dark'
        )
        
        return fig
    except:
        return None

def plot_sentiment_timeline(article_sentiments):
    """Plot sentiment over time"""
    try:
        # Sort by date
        sorted_articles = sorted(article_sentiments, key=lambda x: x['published'])
        
        dates = [a['published'][:10] for a in sorted_articles]
        sentiments = [a['sentiment'] for a in sorted_articles]
        
        fig = go.Figure()
        
        # Line chart
        fig.add_trace(go.Scatter(
            x=dates,
            y=sentiments,
            mode='lines+markers',
            name='Sentiment',
            line=dict(color='#42a5f5', width=2),
            marker=dict(size=8)
        ))
        
        # Add threshold lines
        fig.add_hline(y=0, line_dash="dash", line_color="white")
        fig.add_hline(y=0.05, line_dash="dot", line_color="green", opacity=0.5)
        fig.add_hline(y=-0.05, line_dash="dot", line_color="red", opacity=0.5)
        
        fig.update_layout(
            title='Sentiment Trend Over Time',
            xaxis_title='Date',
            yaxis_title='Sentiment Score',
            height=400,
            template='plotly_dark'
        )
        
        return fig
    except:
        return None

# ==================== MARKET OVERVIEW FUNCTIONS ====================

@st.cache_data(ttl=300)  # Cache for 5 minutes
def fetch_market_indices():
    """Fetch major market indices"""
    try:
        indices = {
            '^GSPC': 'S&P 500',
            '^DJI': 'Dow Jones',
            '^IXIC': 'NASDAQ',
            '^RUT': 'Russell 2000',
            '^VIX': 'VIX'
        }
        
        data = {}
        for symbol, name in indices.items():
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period='5d')
            if not hist.empty:
                current = hist['Close'].iloc[-1]
                prev = hist['Close'].iloc[-2] if len(hist) >= 2 else current
                change = ((current - prev) / prev) * 100
                data[name] = {
                    'price': current,
                    'change': change,
                    'symbol': symbol
                }
        return data
    except Exception as e:
        st.warning(f"Could not fetch indices: {str(e)}")
        return {}

@st.cache_data(ttl=300)
def fetch_sector_performance():
    """Fetch sector ETF performance"""
    try:
        sectors = {
            'XLK': 'Technology',
            'XLF': 'Financials',
            'XLV': 'Healthcare',
            'XLE': 'Energy',
            'XLI': 'Industrials',
            'XLY': 'Consumer Discretionary',
            'XLP': 'Consumer Staples',
            'XLB': 'Materials',
            'XLRE': 'Real Estate',
            'XLU': 'Utilities',
            'XLC': 'Communication'
        }
        
        data = []
        for symbol, name in sectors.items():
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period='5d')
            if not hist.empty:
                current = hist['Close'].iloc[-1]
                prev = hist['Close'].iloc[-2] if len(hist) >= 2 else current
                change = ((current - prev) / prev) * 100
                data.append({
                    'Sector': name,
                    'Symbol': symbol,
                    'Price': current,
                    'Change %': change
                })
        
        return pd.DataFrame(data).sort_values('Change %', ascending=False)
    except Exception as e:
        st.warning(f"Could not fetch sectors: {str(e)}")
        return pd.DataFrame()

@st.cache_data(ttl=300)
def fetch_top_movers():
    """Fetch top gainers and losers"""
    try:
        # Popular stocks to check
        symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NVDA', 'AMD', 
                   'NFLX', 'DIS', 'BA', 'JPM', 'BAC', 'WMT', 'PG', 'JNJ', 'V', 'MA',
                   'PYPL', 'INTC', 'CSCO', 'PFE', 'KO', 'PEP', 'NKE', 'MCD', 'COST',
                   'ADBE', 'CRM', 'ORCL']
        
        data = []
        for symbol in symbols:
            try:
                ticker = yf.Ticker(symbol)
                hist = ticker.history(period='2d')
                if len(hist) >= 2:
                    current = hist['Close'].iloc[-1]
                    prev = hist['Close'].iloc[-2]
                    change = ((current - prev) / prev) * 100
                    volume = hist['Volume'].iloc[-1]
                    data.append({
                        'Symbol': symbol,
                        'Price': current,
                        'Change %': change,
                        'Volume': volume
                    })
            except:
                continue
        
        df = pd.DataFrame(data)
        return df
    except Exception as e:
        st.warning(f"Could not fetch movers: {str(e)}")
        return pd.DataFrame()

def create_sector_heatmap(sector_df):
    """Create sector performance heatmap"""
    try:
        if sector_df.empty:
            return None
        
        fig = go.Figure(data=go.Treemap(
            labels=sector_df['Sector'],
            parents=[''] * len(sector_df),
            values=abs(sector_df['Change %']),
            text=sector_df['Change %'].apply(lambda x: f"{x:+.2f}%"),
            textposition='middle center',
            marker=dict(
                colors=sector_df['Change %'],
                colorscale='RdYlGn',
                cmid=0,
                colorbar=dict(title="Change %")
            ),
            hovertemplate='<b>%{label}</b><br>Change: %{text}<extra></extra>'
        ))
        
        fig.update_layout(
            title='Sector Performance Heatmap',
            height=500,
            template='plotly_dark'
        )
        
        return fig
    except Exception as e:
        st.warning(f"Could not create heatmap: {str(e)}")
        return None

# ==================== COMPARISON & SCREENING FUNCTIONS ====================

@st.cache_data(ttl=600)
def fetch_multiple_stocks(symbols, period='1y'):
    """Fetch data for multiple stocks"""
    try:
        data = {}
        for symbol in symbols:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period=period)
            info = ticker.info
            
            if not hist.empty:
                data[symbol] = {
                    'history': hist,
                    'current_price': hist['Close'].iloc[-1],
                    'name': info.get('longName', symbol),
                    'sector': info.get('sector', 'N/A'),
                    'industry': info.get('industry', 'N/A'),
                    'market_cap': info.get('marketCap', 0),
                    'pe_ratio': info.get('trailingPE', 0),
                    'beta': info.get('beta', 0),
                    'dividend_yield': info.get('dividendYield', 0),
                    'profit_margin': info.get('profitMargins', 0),
                    'revenue_growth': info.get('revenueGrowth', 0)
                }
        return data
    except Exception as e:
        st.error(f"Error fetching stocks: {str(e)}")
        return {}

def calculate_comparison_metrics(stocks_data):
    """Calculate comparison metrics for multiple stocks"""
    try:
        comparison = []
        
        for symbol, data in stocks_data.items():
            hist = data['history']
            
            # Calculate returns
            returns_1m = ((hist['Close'].iloc[-1] / hist['Close'].iloc[-21]) - 1) * 100 if len(hist) >= 21 else 0
            returns_3m = ((hist['Close'].iloc[-1] / hist['Close'].iloc[-63]) - 1) * 100 if len(hist) >= 63 else 0
            returns_1y = ((hist['Close'].iloc[-1] / hist['Close'].iloc[0]) - 1) * 100
            
            # Calculate volatility
            daily_returns = hist['Close'].pct_change().dropna()
            volatility = daily_returns.std() * np.sqrt(252) * 100
            
            # Calculate RSI
            if PANDAS_TA_AVAILABLE:
                rsi = pta.rsi(hist['Close'], length=14).iloc[-1] if len(hist) >= 14 else 50
            else:
                # Simple RSI calculation
                delta = hist['Close'].diff()
                gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                rs = gain / loss
                rsi_series = 100 - (100 / (1 + rs))
                rsi = rsi_series.iloc[-1] if len(rsi_series) > 0 else 50
            
            # Calculate relative strength vs S&P 500
            try:
                spy = yf.Ticker('^GSPC').history(period='1y')
                spy_return = ((spy['Close'].iloc[-1] / spy['Close'].iloc[0]) - 1) * 100
                relative_strength = returns_1y - spy_return
            except:
                relative_strength = 0
            
            comparison.append({
                'Symbol': symbol,
                'Name': data['name'][:30],
                'Price': data['current_price'],
                'Market Cap': data['market_cap'],
                'P/E': data['pe_ratio'],
                'Beta': data['beta'],
                'Div Yield %': data['dividend_yield'] * 100 if data['dividend_yield'] else 0,
                '1M Return %': returns_1m,
                '3M Return %': returns_3m,
                '1Y Return %': returns_1y,
                'Volatility %': volatility,
                'RSI': rsi,
                'Rel Strength %': relative_strength,
                'Sector': data['sector']
            })
        
        return pd.DataFrame(comparison)
    except Exception as e:
        st.error(f"Error calculating metrics: {str(e)}")
        return pd.DataFrame()

def create_comparison_chart(stocks_data):
    """Create normalized price comparison chart"""
    try:
        fig = go.Figure()
        
        for symbol, data in stocks_data.items():
            hist = data['history']
            # Normalize to 100
            normalized = (hist['Close'] / hist['Close'].iloc[0]) * 100
            
            fig.add_trace(go.Scatter(
                x=hist.index,
                y=normalized,
                mode='lines',
                name=symbol,
                line=dict(width=2)
            ))
        
        fig.update_layout(
            title='Normalized Price Comparison (Base = 100)',
            xaxis_title='Date',
            yaxis_title='Normalized Price',
            height=500,
            template='plotly_dark',
            hovermode='x unified',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        return fig
    except Exception as e:
        st.error(f"Error creating chart: {str(e)}")
        return None

def stock_screener(min_price=0, max_price=10000, min_market_cap=0, max_pe=100, 
                   min_volume=0, sectors=None):
    """Screen stocks based on criteria"""
    try:
        # Popular stocks universe
        universe = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NVDA', 'AMD', 
                    'NFLX', 'DIS', 'BA', 'JPM', 'BAC', 'WMT', 'PG', 'JNJ', 'V', 'MA',
                    'PYPL', 'INTC', 'CSCO', 'PFE', 'KO', 'PEP', 'NKE', 'MCD', 'COST',
                    'ADBE', 'CRM', 'ORCL', 'QCOM', 'TXN', 'AVGO', 'SBUX', 'BKNG',
                    'GILD', 'AMGN', 'ISRG', 'REGN', 'VRTX', 'MRNA', 'BIIB', 'ILMN',
                    'GM', 'F', 'CAT', 'DE', 'HON', 'UPS', 'FDX', 'LMT', 'RTX',
                    'GS', 'MS', 'C', 'WFC', 'AXP', 'BLK', 'SCHW', 'USB', 'PNC',
                    'XOM', 'CVX', 'COP', 'SLB', 'EOG', 'PSX', 'VLO', 'MPC']
        
        results = []
        
        for symbol in universe:
            try:
                ticker = yf.Ticker(symbol)
                info = ticker.info
                hist = ticker.history(period='5d')
                
                if hist.empty:
                    continue
                
                price = hist['Close'].iloc[-1]
                market_cap = info.get('marketCap', 0)
                pe = info.get('trailingPE', 0)
                volume = hist['Volume'].iloc[-1]
                sector = info.get('sector', 'N/A')
                
                # Apply filters
                if price < min_price or price > max_price:
                    continue
                if market_cap < min_market_cap:
                    continue
                if pe > max_pe and pe > 0:
                    continue
                if volume < min_volume:
                    continue
                if sectors and sector not in sectors:
                    continue
                
                # Calculate additional metrics
                change = ((hist['Close'].iloc[-1] / hist['Close'].iloc[-2]) - 1) * 100 if len(hist) >= 2 else 0
                
                results.append({
                    'Symbol': symbol,
                    'Name': info.get('longName', symbol)[:30],
                    'Price': price,
                    'Change %': change,
                    'Market Cap': market_cap,
                    'P/E': pe if pe > 0 else 'N/A',
                    'Volume': volume,
                    'Sector': sector,
                    'Industry': info.get('industry', 'N/A')[:30]
                })
            except:
                continue
        
        return pd.DataFrame(results)
    except Exception as e:
        st.error(f"Screening error: {str(e)}")
        return pd.DataFrame()

# ==================== MAIN APPLICATION ====================

def main():
    # Show warnings for missing libraries
    if not QUANTSTATS_AVAILABLE:
        st.sidebar.warning("⚠️ quantstats not installed. Risk metrics will be limited.")
    if not PANDAS_TA_AVAILABLE:
        st.sidebar.warning("⚠️ pandas_ta not installed. Some indicators will be limited.")
    
    # Header
    st.markdown('<h1 class="main-header">Professional Trading Platform</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Institutional-Grade Market Analysis & Trading Tools</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.image("https://img.icons8.com/fluency/96/000000/combo-chart.png", width=80)
        st.title("⚙️ Trading Console")
        
        # Symbol input
        st.subheader("📊 Market Selection")
        symbol = st.text_input("Stock Symbol", value="MSFT", help="Enter ticker symbol (e.g., MSFT, GOOGL, TSLA)").upper()
        
        # Popular symbols helper
        with st.expander("💡 Popular Symbols"):
            st.markdown("""
            **Tech:** AAPL, MSFT, GOOGL, AMZN, META, NVDA, TSLA
            
            **Finance:** JPM, BAC, GS, MS, V, MA
            
            **Healthcare:** JNJ, PFE, UNH, ABBV
            
            **Consumer:** WMT, KO, PEP, NKE, MCD
            
            **Energy:** XOM, CVX, COP
            """)
        
        # Timeframe
        st.subheader("📅 Timeframe")
        period = st.selectbox("Period", ['1mo', '3mo', '6mo', '1y', '2y', '5y', 'max'], index=3)
        
        interval_options = {
            "1 Day": "1d", "1 Week": "1wk", "1 Month": "1mo",
            "5 Minutes": "5m", "15 Minutes": "15m", "30 Minutes": "30m", "1 Hour": "1h"
        }
        selected_interval_display = st.selectbox("Select Interval", list(interval_options.keys()), index=0)
        interval = interval_options[selected_interval_display]
        
        # Validate interval/period combination
        if interval in ['5m', '15m', '30m'] and period not in ['1mo', '5d', '1d']:
            st.warning(f"⚠️ Intraday data ({interval}) is limited to the last 60 days. Data may be truncated.")
        elif interval == '1h' and period in ['5y', 'max']:
            st.warning("⚠️ Hourly data is limited to the last 730 days. Data may be truncated.")
        
        show_volume = st.checkbox("Show Volume on Chart", True)
        show_signals = st.checkbox("Trading Signals", True)
        show_risk = st.checkbox("Risk Metrics", True)
        
        st.markdown("---")
        st.caption("⚠️ Professional tools for educational purposes")
        st.caption("Not financial advice")
    
    # Fetch data
    with st.spinner(f"📥 Fetching {symbol} data..."):
        df, company_info = fetch_professional_data(symbol, period=period, interval=interval)
    
    if df is None or df.empty:
        st.error(f"❌ Could not fetch data for {symbol}. Please check the symbol and try again.")
        return
    
    # Calculate indicators
    with st.spinner("📊 Calculating technical indicators..."):
        df = calculate_professional_indicators(df)
    
    # Success message
    st.success(f"✅ Loaded {len(df)} data points for {company_info['name']}")
    
    # Company Info Bar
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    current_price = df['Close'].iloc[-1]
    prev_price = df['Close'].iloc[-2]
    change = current_price - prev_price
    change_pct = (change / prev_price) * 100
    
    col1.metric("Price", f"${current_price:.2f}", f"{change_pct:+.2f}%")
    col2.metric("Market Cap", f"${company_info['marketCap']/1e9:.2f}B" if company_info['marketCap'] > 0 else "N/A")
    col3.metric("P/E Ratio", f"{company_info['pe']:.2f}" if company_info['pe'] > 0 else "N/A")
    col4.metric("Beta", f"{company_info['beta']:.2f}" if company_info['beta'] > 0 else "N/A")
    col5.metric("52W High", f"${company_info['fiftyTwoWeekHigh']:.2f}" if company_info['fiftyTwoWeekHigh'] > 0 else "N/A")
    col6.metric("52W Low", f"${company_info['fiftyTwoWeekLow']:.2f}" if company_info['fiftyTwoWeekLow'] > 0 else "N/A")
    
    st.markdown("---")
    
    # Pre-compute returns for use across multiple tabs
    returns = df['Close'].pct_change().dropna()

    # Main Tabs
    tabs = st.tabs([
        "📈 Chart Analysis",
        "🎯 Trading Signals",
        "📊 Technical Indicators",
        "📰 Sentiment Analysis",
        "⚠️ Risk Analysis",
        "📋 Performance Metrics",
        "🔮 Quantitative Analysis",
        "🌍 Market Overview",
        "⚖️ Stock Comparison",
        "🔍 Stock Screener"
    ])
    
    # TAB 1: Chart Analysis
    with tabs[0]:
        st.subheader("📈 Professional Chart Analysis")
        
        chart = create_professional_chart(df, symbol, show_volume=show_volume)
        if chart:
            st.plotly_chart(chart, use_container_width=True)
        
        # Key Levels
        st.subheader("🎯 Key Price Levels")
        col1, col2, col3 = st.columns(3)
        
        high_52w = df['High'].rolling(252).max().iloc[-1]
        low_52w = df['Low'].rolling(252).min().iloc[-1]
        avg_20d = df['Close'].rolling(20).mean().iloc[-1]
        
        col1.metric("52-Week High", f"${high_52w:.2f}")
        col2.metric("52-Week Low", f"${low_52w:.2f}")
        col3.metric("20-Day Average", f"${avg_20d:.2f}")
    
    # TAB 2: Trading Signals
    with tabs[1]:
        st.subheader("🎯 Professional Trading Signals")
        
        signals = []  # Initialize signals
        
        if show_signals:
            signals = generate_trading_signals(df)
            
            if signals:
                for signal_name, description, sentiment in signals:
                    if "BULLISH" in sentiment or "BUY" in sentiment:
                        st.success(f"**{signal_name}**\n\n{description}")
                    elif "BEARISH" in sentiment or "SELL" in sentiment:
                        st.error(f"**{signal_name}**\n\n{description}")
                    elif "CAUTION" in sentiment or "OVERBOUGHT" in sentiment:
                        st.warning(f"**{signal_name}**\n\n{description}")
                    elif "OPPORTUNITY" in sentiment or "OVERSOLD" in sentiment:
                        st.info(f"**{signal_name}**\n\n{description}")
                    else:
                        st.info(f"**{signal_name}**\n\n{description}")
            else:
                st.info("No significant signals detected at this time.")
        else:
            st.info("Enable 'Trading Signals' in the sidebar to view signals.")
        
        # Signal Summary
        if signals:  # Only show summary if signals exist
            st.markdown("---")
            st.subheader("📊 Signal Summary")
            
            col1, col2, col3 = st.columns(3)
            
            bullish_count = sum(1 for _, _, s in signals if "BULLISH" in s or "BUY" in s)
            bearish_count = sum(1 for _, _, s in signals if "BEARISH" in s or "SELL" in s)
            neutral_count = len(signals) - bullish_count - bearish_count
        
            col1.metric("Bullish Signals", bullish_count, delta="Positive" if bullish_count > bearish_count else None)
            col2.metric("Bearish Signals", bearish_count, delta="Negative" if bearish_count > bullish_count else None)
            col3.metric("Neutral/Other", neutral_count)
            
            # Overall Recommendation
            if bullish_count > bearish_count + 1:
                st.success("🟢 **OVERALL: BULLISH** - Multiple bullish indicators detected")
            elif bearish_count > bullish_count + 1:
                st.error("🔴 **OVERALL: BEARISH** - Multiple bearish indicators detected")
            else:
                st.info("⚪ **OVERALL: NEUTRAL** - Mixed signals, exercise caution")
    
    # TAB 3: Technical Indicators
    with tabs[2]:
        st.subheader("📊 Technical Indicator Values")
        
        latest = df.iloc[-1]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Trend Indicators")
            indicator_data = []
            
            if 'SMA_20' in df.columns:
                indicator_data.append({"Indicator": "SMA 20", "Value": f"${latest['SMA_20']:.2f}"})
            if 'SMA_50' in df.columns:
                indicator_data.append({"Indicator": "SMA 50", "Value": f"${latest['SMA_50']:.2f}"})
            if 'SMA_200' in df.columns:
                indicator_data.append({"Indicator": "SMA 200", "Value": f"${latest['SMA_200']:.2f}"})
            if 'EMA_12' in df.columns:
                indicator_data.append({"Indicator": "EMA 12", "Value": f"${latest['EMA_12']:.2f}"})
            if 'EMA_26' in df.columns:
                indicator_data.append({"Indicator": "EMA 26", "Value": f"${latest['EMA_26']:.2f}"})
            
            if indicator_data:
                st.dataframe(pd.DataFrame(indicator_data), hide_index=True, use_container_width=True)
        
        with col2:
            st.markdown("#### Momentum Indicators")
            momentum_data = []
            
            if 'RSI' in df.columns:
                momentum_data.append({"Indicator": "RSI (14)", "Value": f"{latest['RSI']:.2f}"})
            if 'MACD_12_26_9' in df.columns:
                momentum_data.append({"Indicator": "MACD", "Value": f"{latest['MACD_12_26_9']:.4f}"})
            if 'MACDs_12_26_9' in df.columns:
                momentum_data.append({"Indicator": "MACD Signal", "Value": f"{latest['MACDs_12_26_9']:.4f}"})
            if 'ATR' in df.columns:
                momentum_data.append({"Indicator": "ATR (14)", "Value": f"{latest['ATR']:.2f}"})
            
            if momentum_data:
                st.dataframe(pd.DataFrame(momentum_data), hide_index=True, use_container_width=True)
        
        # Bollinger Bands
        if 'BBL_20_2.0' in df.columns:
            st.markdown("#### Bollinger Bands (20, 2)")
            bb_data = pd.DataFrame([
                {"Level": "Upper Band", "Value": f"${latest['BBU_20_2.0']:.2f}"},
                {"Level": "Middle Band", "Value": f"${latest['BBM_20_2.0']:.2f}"},
                {"Level": "Lower Band", "Value": f"${latest['BBL_20_2.0']:.2f}"}
            ])
            st.dataframe(bb_data, hide_index=True, use_container_width=True)
    
    # TAB 4: Sentiment Analysis
    with tabs[3]:
        st.subheader("📰 News Sentiment Analysis")
        
        if not NEWS_AVAILABLE:
            st.warning("⚠️ Sentiment analysis requires newsapi-python and vaderSentiment libraries.")
            st.info("Install with: pip install newsapi-python vaderSentiment")
        else:
            st.info("💡 Analyzing recent news articles to determine market sentiment and generate trading recommendations")
            
            if st.button("🔍 Analyze News Sentiment", type="primary"):
                with st.spinner(f"📰 Fetching and analyzing news for {symbol}..."):
                    # Fetch news
                    articles = fetch_news_articles(symbol, company_info['name'])
                    
                    if articles and len(articles) > 0:
                        # Calculate sentiment metrics
                        sentiment_metrics = calculate_sentiment_metrics(articles)
                        
                        if sentiment_metrics:
                            # Generate recommendation
                            recommendation, emoji, explanation = generate_sentiment_recommendation(
                                sentiment_metrics['avg_sentiment'],
                                sentiment_metrics['strength']
                            )
                            
                            # Display main recommendation
                            st.markdown("---")
                            st.markdown("### 🎯 Sentiment-Based Recommendation")
                            
                            # Big recommendation card
                            if "BUY" in recommendation:
                                st.success(f"## {emoji} {recommendation}")
                                st.success(f"**{explanation}**")
                            elif "SELL" in recommendation:
                                st.error(f"## {emoji} {recommendation}")
                                st.error(f"**{explanation}**")
                            else:
                                st.info(f"## {emoji} {recommendation}")
                                st.info(f"**{explanation}**")
                            
                            st.markdown("---")
                            
                            # Sentiment metrics
                            st.markdown("### 📊 Sentiment Metrics")
                            
                            col1, col2, col3, col4 = st.columns(4)
                            
                            col1.metric(
                                "Average Sentiment",
                                f"{sentiment_metrics['avg_sentiment']:.3f}",
                                help="Range: -1 (very negative) to +1 (very positive)"
                            )
                            
                            col2.metric(
                                "Sentiment Strength",
                                sentiment_metrics['strength']
                            )
                            
                            col3.metric(
                                "Articles Analyzed",
                                sentiment_metrics['total_articles']
                            )
                            
                            trend_emoji = "📈" if sentiment_metrics['sentiment_trend'] > 0 else "📉" if sentiment_metrics['sentiment_trend'] < 0 else "➡️"
                            col4.metric(
                                "Sentiment Trend",
                                f"{trend_emoji} {sentiment_metrics['sentiment_trend']:.3f}",
                                help="Positive = improving sentiment, Negative = deteriorating"
                            )
                            
                            # Sentiment breakdown
                            st.markdown("---")
                            st.markdown("### 📈 Sentiment Breakdown")
                            
                            col1, col2, col3 = st.columns(3)
                            
                            col1.metric(
                                "🟢 Positive Articles",
                                sentiment_metrics['positive_count'],
                                f"{(sentiment_metrics['positive_count']/sentiment_metrics['total_articles']*100):.0f}%"
                            )
                            
                            col2.metric(
                                "⚪ Neutral Articles",
                                sentiment_metrics['neutral_count'],
                                f"{(sentiment_metrics['neutral_count']/sentiment_metrics['total_articles']*100):.0f}%"
                            )
                            
                            col3.metric(
                                "🔴 Negative Articles",
                                sentiment_metrics['negative_count'],
                                f"{(sentiment_metrics['negative_count']/sentiment_metrics['total_articles']*100):.0f}%"
                            )
                            
                            # Visualizations
                            st.markdown("---")
                            st.markdown("### 📊 Sentiment Visualizations")
                            
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                dist_fig = plot_sentiment_distribution(sentiment_metrics['article_sentiments'])
                                if dist_fig:
                                    st.plotly_chart(dist_fig, use_container_width=True)
                            
                            with col2:
                                timeline_fig = plot_sentiment_timeline(sentiment_metrics['article_sentiments'])
                                if timeline_fig:
                                    st.plotly_chart(timeline_fig, use_container_width=True)
                            
                            # Individual articles - TOP 20 NEWS
                            st.markdown("---")
                            st.markdown("### 📰 Top 20 News Articles")
                            
                            # Create tabs for different views
                            news_tabs = st.tabs(["📊 By Sentiment", "🕐 By Date", "📋 All Articles"])
                            
                            # TAB 1: Sorted by Sentiment Strength
                            with news_tabs[0]:
                                st.markdown("#### Sorted by Sentiment Impact")
                                
                                # Sort by absolute sentiment (most impactful first)
                                sorted_by_sentiment = sorted(
                                    sentiment_metrics['article_sentiments'],
                                    key=lambda x: abs(x['sentiment']),
                                    reverse=True
                                )
                                
                                for i, article in enumerate(sorted_by_sentiment[:20], 1):
                                    sentiment = article['sentiment']
                                    
                                    # Determine color and emoji
                                    if sentiment > 0.2:
                                        sentiment_label = "🟢🟢 VERY POSITIVE"
                                        color = "success"
                                    elif sentiment > 0.05:
                                        sentiment_label = "🟢 POSITIVE"
                                        color = "success"
                                    elif sentiment < -0.2:
                                        sentiment_label = "🔴🔴 VERY NEGATIVE"
                                        color = "error"
                                    elif sentiment < -0.05:
                                        sentiment_label = "🔴 NEGATIVE"
                                        color = "error"
                                    else:
                                        sentiment_label = "⚪ NEUTRAL"
                                        color = "info"
                                    
                                    with st.expander(f"#{i} {sentiment_label} ({sentiment:.3f}) - {article['title'][:70]}..."):
                                        st.markdown(f"**📰 {article['title']}**")
                                        st.write(f"**Source:** {article['source']}")
                                        st.write(f"**Published:** {article['published'][:10]} {article['published'][11:16]}")
                                        st.write(f"**Sentiment Score:** {sentiment:.3f}")
                                        
                                        # Sentiment bar
                                        sentiment_pct = (sentiment + 1) / 2 * 100  # Convert -1 to 1 into 0 to 100
                                        st.progress(sentiment_pct / 100)
                                        
                                        st.markdown(f"[🔗 Read Full Article]({article['url']})")
                            
                            # TAB 2: Sorted by Date (Most Recent First)
                            with news_tabs[1]:
                                st.markdown("#### Latest News First")
                                
                                # Sort by date (most recent first)
                                sorted_by_date = sorted(
                                    sentiment_metrics['article_sentiments'],
                                    key=lambda x: x['published'],
                                    reverse=True
                                )
                                
                                for i, article in enumerate(sorted_by_date[:20], 1):
                                    sentiment = article['sentiment']
                                    
                                    # Determine emoji
                                    if sentiment > 0.05:
                                        emoji = "🟢"
                                    elif sentiment < -0.05:
                                        emoji = "🔴"
                                    else:
                                        emoji = "⚪"
                                    
                                    with st.expander(f"#{i} {emoji} {article['published'][:10]} - {article['title'][:70]}..."):
                                        st.markdown(f"**📰 {article['title']}**")
                                        st.write(f"**Source:** {article['source']}")
                                        st.write(f"**Published:** {article['published'][:10]} {article['published'][11:16]}")
                                        st.write(f"**Sentiment:** {sentiment:.3f}")
                                        
                                        # Sentiment interpretation
                                        if sentiment > 0.2:
                                            st.success("Very Positive News")
                                        elif sentiment > 0.05:
                                            st.success("Positive News")
                                        elif sentiment < -0.2:
                                            st.error("Very Negative News")
                                        elif sentiment < -0.05:
                                            st.error("Negative News")
                                        else:
                                            st.info("Neutral News")
                                        
                                        st.markdown(f"[🔗 Read Full Article]({article['url']})")
                            
                            # TAB 3: All Articles in Table Format
                            with news_tabs[2]:
                                st.markdown("#### All Articles Overview")
                                
                                # Create DataFrame for table view
                                news_df = pd.DataFrame([
                                    {
                                        '#': i+1,
                                        'Date': article['published'][:10],
                                        'Sentiment': f"{article['sentiment']:.3f}",
                                        'Type': '🟢 Positive' if article['sentiment'] > 0.05 else '🔴 Negative' if article['sentiment'] < -0.05 else '⚪ Neutral',
                                        'Source': article['source'],
                                        'Title': article['title'][:60] + '...' if len(article['title']) > 60 else article['title']
                                    }
                                    for i, article in enumerate(sentiment_metrics['article_sentiments'][:20])
                                ])
                                
                                st.dataframe(
                                    news_df,
                                    use_container_width=True,
                                    hide_index=True,
                                    column_config={
                                        '#': st.column_config.NumberColumn('#', width='small'),
                                        'Date': st.column_config.TextColumn('Date', width='small'),
                                        'Sentiment': st.column_config.TextColumn('Score', width='small'),
                                        'Type': st.column_config.TextColumn('Type', width='small'),
                                        'Source': st.column_config.TextColumn('Source', width='medium'),
                                        'Title': st.column_config.TextColumn('Title', width='large')
                                    }
                                )
                                
                                # Download option
                                csv = news_df.to_csv(index=False)
                                st.download_button(
                                    label="📥 Download News Data as CSV",
                                    data=csv,
                                    file_name=f"{symbol}_news_{datetime.now().strftime('%Y%m%d')}.csv",
                                    mime="text/csv"
                                )
                                
                                # Clickable links section
                                st.markdown("---")
                                st.markdown("#### 🔗 Quick Links to All Articles")
                                
                                for i, article in enumerate(sentiment_metrics['article_sentiments'][:20], 1):
                                    sentiment = article['sentiment']
                                    emoji = "🟢" if sentiment > 0.05 else "🔴" if sentiment < -0.05 else "⚪"
                                    st.markdown(f"{i}. {emoji} [{article['title']}]({article['url']}) - *{article['source']}*")
                            
                            # Trading strategy based on sentiment
                            st.markdown("---")
                            st.markdown("### 💡 Sentiment Trading Strategy")
                            
                            if sentiment_metrics['avg_sentiment'] > 0.15:
                                st.success(
                                    "**Bullish Sentiment Strategy:**\n"
                                    "- Consider entering long positions\n"
                                    "- Positive news flow supports upward momentum\n"
                                    "- Set stop loss 2-3% below entry\n"
                                    "- Take profits at resistance levels\n"
                                    "- Monitor for sentiment reversal"
                                )
                            elif sentiment_metrics['avg_sentiment'] < -0.15:
                                st.error(
                                    "**Bearish Sentiment Strategy:**\n"
                                    "- Avoid new long positions\n"
                                    "- Consider reducing exposure\n"
                                    "- Negative news may pressure price\n"
                                    "- Wait for sentiment improvement\n"
                                    "- Watch for capitulation signals"
                                )
                            else:
                                st.info(
                                    "**Neutral Sentiment Strategy:**\n"
                                    "- Wait for clearer sentiment direction\n"
                                    "- Use technical analysis for timing\n"
                                    "- Maintain current positions\n"
                                    "- Set tight stop losses\n"
                                    "- Be ready to act on sentiment shift"
                                )
                            
                            # Confidence level
                            st.markdown("---")
                            st.markdown("### 🎯 Recommendation Confidence")
                            
                            # Calculate confidence
                            confidence_factors = []
                            
                            if sentiment_metrics['total_articles'] >= 15:
                                confidence_factors.append(("High article count", 25))
                            elif sentiment_metrics['total_articles'] >= 10:
                                confidence_factors.append(("Moderate article count", 15))
                            else:
                                confidence_factors.append(("Low article count", 5))
                            
                            if abs(sentiment_metrics['avg_sentiment']) > 0.3:
                                confidence_factors.append(("Strong sentiment", 30))
                            elif abs(sentiment_metrics['avg_sentiment']) > 0.15:
                                confidence_factors.append(("Moderate sentiment", 20))
                            else:
                                confidence_factors.append(("Weak sentiment", 10))
                            
                            if sentiment_metrics['sentiment_std'] < 0.2:
                                confidence_factors.append(("High consistency", 25))
                            elif sentiment_metrics['sentiment_std'] < 0.3:
                                confidence_factors.append(("Moderate consistency", 15))
                            else:
                                confidence_factors.append(("Low consistency", 5))
                            
                            if abs(sentiment_metrics['sentiment_trend']) > 0.1:
                                confidence_factors.append(("Clear trend", 20))
                            else:
                                confidence_factors.append(("No clear trend", 10))
                            
                            total_confidence = sum(score for _, score in confidence_factors)
                            
                            if total_confidence >= 80:
                                st.success(f"### ✅ HIGH CONFIDENCE: {total_confidence}%")
                            elif total_confidence >= 60:
                                st.info(f"### ⚪ MODERATE CONFIDENCE: {total_confidence}%")
                            else:
                                st.warning(f"### ⚠️ LOW CONFIDENCE: {total_confidence}%")
                            
                            with st.expander("📊 Confidence Breakdown"):
                                for factor, score in confidence_factors:
                                    st.write(f"- {factor}: {score}%")
                        
                        else:
                            st.error("Could not analyze sentiment from articles")
                    else:
                        st.warning(f"No recent news articles found for {symbol}")
    
    # TAB 5: Risk Analysis
    with tabs[4]:
        st.subheader("⚠️ Professional Risk Analysis")
        
        if show_risk:
            risk_metrics = calculate_risk_metrics(df)
            
            if risk_metrics:
                col1, col2, col3, col4 = st.columns(4)
                
                col1.metric("Sharpe Ratio", f"{risk_metrics['sharpe']:.2f}", 
                           help="Risk-adjusted return (>1 is good, >2 is very good)")
                col2.metric("Sortino Ratio", f"{risk_metrics['sortino']:.2f}",
                           help="Downside risk-adjusted return")
                col3.metric("Max Drawdown", f"{risk_metrics['max_drawdown']*100:.2f}%",
                           help="Largest peak-to-trough decline")
                col4.metric("Volatility", f"{risk_metrics['volatility']*100:.2f}%",
                           help="Annualized price volatility")
                
                st.markdown("---")
                
                col1, col2, col3 = st.columns(3)
                
                col1.metric("VaR (95%)", f"{risk_metrics['var_95']*100:.2f}%",
                           help="Maximum expected daily loss (95% confidence)")
                col2.metric("Calmar Ratio", f"{risk_metrics['calmar']:.2f}",
                           help="Return vs max drawdown")
                col3.metric("Win Rate", f"{risk_metrics['win_rate']:.1f}%",
                           help="Percentage of positive return days")
                
                # Risk Assessment
                st.markdown("---")
                st.subheader("📋 Risk Assessment")
                
                if risk_metrics['sharpe'] > 1:
                    st.success("✅ **Good Risk-Adjusted Returns** - Sharpe ratio above 1")
                else:
                    st.warning("⚠️ **Below Average Risk-Adjusted Returns** - Sharpe ratio below 1")
                
                if abs(risk_metrics['max_drawdown']) > 0.20:
                    st.error("🔴 **High Drawdown Risk** - Maximum drawdown exceeds 20%")
                elif abs(risk_metrics['max_drawdown']) > 0.10:
                    st.warning("⚠️ **Moderate Drawdown Risk** - Maximum drawdown between 10-20%")
                else:
                    st.success("✅ **Low Drawdown Risk** - Maximum drawdown under 10%")
        else:
            st.info("Enable 'Risk Metrics' in the sidebar to view risk analysis.")
    
    # TAB 6: Performance Metrics
    with tabs[5]:
        st.subheader("📋 Performance Metrics")

        col1, col2, col3, col4 = st.columns(4)
        
        # Calculate returns
        daily_return = returns.iloc[-1] * 100
        weekly_return = ((df['Close'].iloc[-1] / df['Close'].iloc[-5]) - 1) * 100 if len(df) >= 5 else 0
        monthly_return = ((df['Close'].iloc[-1] / df['Close'].iloc[-21]) - 1) * 100 if len(df) >= 21 else 0
        ytd_return = ((df['Close'].iloc[-1] / df['Close'].iloc[0]) - 1) * 100
        
        col1.metric("Daily Return", f"{daily_return:+.2f}%")
        col2.metric("Weekly Return", f"{weekly_return:+.2f}%")
        col3.metric("Monthly Return", f"{monthly_return:+.2f}%")
        col4.metric("Period Return", f"{ytd_return:+.2f}%")
        
        # Returns Distribution
        st.markdown("---")
        st.subheader("📊 Returns Distribution")
        
        fig = go.Figure()
        fig.add_trace(go.Histogram(
            x=returns * 100,
            nbinsx=50,
            name='Daily Returns',
            marker_color='#42a5f5'
        ))
        
        fig.update_layout(
            title='Daily Returns Distribution (%)',
            xaxis_title='Return (%)',
            yaxis_title='Frequency',
            height=400,
            template='plotly_dark'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Cumulative Returns
        st.subheader("📈 Cumulative Returns")
        
        cumulative_returns = (1 + returns).cumprod()
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=returns.index,
            y=cumulative_returns,
            mode='lines',
            name='Cumulative Returns',
            line=dict(color='#26a69a', width=2),
            fill='tozeroy'
        ))
        
        fig.update_layout(
            title='Cumulative Returns Over Time',
            xaxis_title='Date',
            yaxis_title='Cumulative Return',
            height=400,
            template='plotly_dark'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # TAB 7: Quantitative Analysis
    with tabs[6]:
        st.subheader("🔮 Quantitative Analysis")
        
        st.info("📊 **Professional Quantitative Metrics**")
        
        # Statistical Analysis
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Statistical Measures")
            stats_data = pd.DataFrame([
                {"Metric": "Mean Daily Return", "Value": f"{returns.mean()*100:.4f}%"},
                {"Metric": "Median Daily Return", "Value": f"{returns.median()*100:.4f}%"},
                {"Metric": "Std Deviation", "Value": f"{returns.std()*100:.4f}%"},
                {"Metric": "Skewness", "Value": f"{returns.skew():.4f}"},
                {"Metric": "Kurtosis", "Value": f"{returns.kurtosis():.4f}"}
            ])
            st.dataframe(stats_data, hide_index=True, use_container_width=True)
        
        with col2:
            st.markdown("#### Volume Analysis")
            vol_data = pd.DataFrame([
                {"Metric": "Avg Volume (20d)", "Value": f"{df['Volume'].rolling(20).mean().iloc[-1]:,.0f}"},
                {"Metric": "Current Volume", "Value": f"{df['Volume'].iloc[-1]:,.0f}"},
                {"Metric": "Volume Ratio", "Value": f"{(df['Volume'].iloc[-1] / df['Volume'].rolling(20).mean().iloc[-1]):.2f}x"},
                {"Metric": "Max Volume", "Value": f"{df['Volume'].max():,.0f}"},
                {"Metric": "Min Volume", "Value": f"{df['Volume'].min():,.0f}"}
            ])
            st.dataframe(vol_data, hide_index=True, use_container_width=True)
    
    # TAB 8: Market Overview
    with tabs[7]:
        st.subheader("🌍 Market Overview Dashboard")
        
        # Market Indices
        st.markdown("### 📊 Major Market Indices")
        
        with st.spinner("Fetching market data..."):
            indices_data = fetch_market_indices()
        
        if indices_data:
            cols = st.columns(len(indices_data))
            for idx, (name, data) in enumerate(indices_data.items()):
                with cols[idx]:
                    st.metric(
                        name,
                        f"{data['price']:.2f}",
                        f"{data['change']:+.2f}%",
                        delta_color="normal"
                    )
        
        st.markdown("---")
        
        # Sector Performance
        st.markdown("### 🏭 Sector Performance")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            sector_df = fetch_sector_performance()
            if not sector_df.empty:
                heatmap = create_sector_heatmap(sector_df)
                if heatmap:
                    st.plotly_chart(heatmap, use_container_width=True)
        
        with col2:
            if not sector_df.empty:
                st.markdown("#### Top Sectors")
                top_sectors = sector_df.head(5)[['Sector', 'Change %']].copy()
                top_sectors['Change %'] = top_sectors['Change %'].apply(lambda x: f"{x:+.2f}%")
                st.dataframe(top_sectors, hide_index=True, use_container_width=True)
                
                st.markdown("#### Bottom Sectors")
                bottom_sectors = sector_df.tail(5)[['Sector', 'Change %']].copy()
                bottom_sectors['Change %'] = bottom_sectors['Change %'].apply(lambda x: f"{x:+.2f}%")
                st.dataframe(bottom_sectors, hide_index=True, use_container_width=True)
        
        st.markdown("---")
        
        # Top Movers
        st.markdown("### 🚀 Top Movers")
        
        movers_df = fetch_top_movers()
        
        if not movers_df.empty:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 📈 Top Gainers")
                gainers = movers_df.nlargest(10, 'Change %')[['Symbol', 'Price', 'Change %', 'Volume']].copy()
                gainers['Price'] = gainers['Price'].apply(lambda x: f"${x:.2f}")
                gainers['Change %'] = gainers['Change %'].apply(lambda x: f"+{x:.2f}%")
                gainers['Volume'] = gainers['Volume'].apply(lambda x: f"{x:,.0f}")
                st.dataframe(gainers, hide_index=True, use_container_width=True)
            
            with col2:
                st.markdown("#### 📉 Top Losers")
                losers = movers_df.nsmallest(10, 'Change %')[['Symbol', 'Price', 'Change %', 'Volume']].copy()
                losers['Price'] = losers['Price'].apply(lambda x: f"${x:.2f}")
                losers['Change %'] = losers['Change %'].apply(lambda x: f"{x:.2f}%")
                losers['Volume'] = losers['Volume'].apply(lambda x: f"{x:,.0f}")
                st.dataframe(losers, hide_index=True, use_container_width=True)
        
        st.markdown("---")
        
        # Most Active
        st.markdown("### 📊 Most Active Stocks")
        
        if not movers_df.empty:
            most_active = movers_df.nlargest(15, 'Volume')[['Symbol', 'Price', 'Change %', 'Volume']].copy()
            most_active['Price'] = most_active['Price'].apply(lambda x: f"${x:.2f}")
            most_active['Change %'] = most_active['Change %'].apply(lambda x: f"{x:+.2f}%")
            most_active['Volume'] = most_active['Volume'].apply(lambda x: f"{x:,.0f}")
            st.dataframe(most_active, hide_index=True, use_container_width=True)
    
    # TAB 9: Stock Comparison
    with tabs[8]:
        st.subheader("⚖️ Stock Comparison Tool")
        
        st.info("💡 Compare multiple stocks side-by-side to identify the best opportunities")
        
        # Stock selection
        st.markdown("### 📝 Select Stocks to Compare")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            comparison_symbols = st.text_input(
                "Enter stock symbols (comma-separated)",
                value="MSFT,GOOGL,TSLA,NVDA",
                help="Example: MSFT,GOOGL,TSLA,NVDA"
            )
        
        with col2:
            comparison_period = st.selectbox(
                "Time Period",
                ['1mo', '3mo', '6mo', '1y', '2y', '5y'],
                index=3
            )
        
        if st.button("🔍 Compare Stocks", type="primary"):
            symbols_list = [s.strip().upper() for s in comparison_symbols.split(',') if s.strip()]
            
            if len(symbols_list) < 2:
                st.warning("Please enter at least 2 stocks to compare")
            elif len(symbols_list) > 10:
                st.warning("Please limit comparison to 10 stocks maximum")
            else:
                with st.spinner(f"Fetching data for {len(symbols_list)} stocks..."):
                    stocks_data = fetch_multiple_stocks(symbols_list, period=comparison_period)
                
                if stocks_data:
                    # Price comparison chart
                    st.markdown("---")
                    st.markdown("### 📈 Price Performance Comparison")
                    
                    comparison_chart = create_comparison_chart(stocks_data)
                    if comparison_chart:
                        st.plotly_chart(comparison_chart, use_container_width=True)
                    
                    # Metrics comparison
                    st.markdown("---")
                    st.markdown("### 📊 Detailed Metrics Comparison")
                    
                    comparison_df = calculate_comparison_metrics(stocks_data)
                    
                    if not comparison_df.empty:
                        # Format the dataframe
                        display_df = comparison_df.copy()
                        display_df['Price'] = display_df['Price'].apply(lambda x: f"${x:.2f}")
                        display_df['Market Cap'] = display_df['Market Cap'].apply(
                            lambda x: f"${x/1e9:.2f}B" if x > 0 else "N/A"
                        )
                        display_df['P/E'] = display_df['P/E'].apply(
                            lambda x: f"{x:.2f}" if x > 0 else "N/A"
                        )
                        display_df['Beta'] = display_df['Beta'].apply(
                            lambda x: f"{x:.2f}" if x > 0 else "N/A"
                        )
                        display_df['Div Yield %'] = display_df['Div Yield %'].apply(lambda x: f"{x:.2f}%")
                        display_df['1M Return %'] = display_df['1M Return %'].apply(lambda x: f"{x:+.2f}%")
                        display_df['3M Return %'] = display_df['3M Return %'].apply(lambda x: f"{x:+.2f}%")
                        display_df['1Y Return %'] = display_df['1Y Return %'].apply(lambda x: f"{x:+.2f}%")
                        display_df['Volatility %'] = display_df['Volatility %'].apply(lambda x: f"{x:.2f}%")
                        display_df['RSI'] = display_df['RSI'].apply(lambda x: f"{x:.1f}")
                        display_df['Rel Strength %'] = display_df['Rel Strength %'].apply(lambda x: f"{x:+.2f}%")
                        
                        st.dataframe(display_df, hide_index=True, use_container_width=True)
                        
                        # Download option
                        csv = comparison_df.to_csv(index=False)
                        st.download_button(
                            label="📥 Download Comparison Data",
                            data=csv,
                            file_name=f"stock_comparison_{datetime.now().strftime('%Y%m%d')}.csv",
                            mime="text/csv"
                        )
                        
                        # Key insights
                        st.markdown("---")
                        st.markdown("### 💡 Key Insights")
                        
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            best_1y = comparison_df.loc[comparison_df['1Y Return %'].idxmax()]
                            st.success(f"**Best 1Y Return**\n\n{best_1y['Symbol']}: {best_1y['1Y Return %']:+.2f}%")
                        
                        with col2:
                            lowest_vol = comparison_df.loc[comparison_df['Volatility %'].idxmin()]
                            st.info(f"**Lowest Volatility**\n\n{lowest_vol['Symbol']}: {lowest_vol['Volatility %']:.2f}%")
                        
                        with col3:
                            best_rs = comparison_df.loc[comparison_df['Rel Strength %'].idxmax()]
                            st.success(f"**Best Rel. Strength**\n\n{best_rs['Symbol']}: {best_rs['Rel Strength %']:+.2f}%")
                        
                        # Sector comparison
                        if 'Sector' in comparison_df.columns:
                            st.markdown("---")
                            st.markdown("### 🏭 Sector Distribution")
                            
                            sector_counts = comparison_df['Sector'].value_counts()
                            
                            fig = go.Figure(data=[go.Pie(
                                labels=sector_counts.index,
                                values=sector_counts.values,
                                hole=0.3
                            )])
                            
                            fig.update_layout(
                                title='Stocks by Sector',
                                height=400,
                                template='plotly_dark'
                            )
                            
                            st.plotly_chart(fig, use_container_width=True)
                else:
                    st.error("Could not fetch data for the selected stocks")
    
    # TAB 10: Stock Screener
    with tabs[9]:
        st.subheader("🔍 Stock Screener")
        
        st.info("💡 Filter stocks based on your criteria to find investment opportunities")
        
        # Screening criteria
        st.markdown("### ⚙️ Screening Criteria")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("#### Price Range")
            min_price = st.number_input("Min Price ($)", min_value=0.0, value=0.0, step=1.0)
            max_price = st.number_input("Max Price ($)", min_value=0.0, value=10000.0, step=10.0)
        
        with col2:
            st.markdown("#### Market Cap")
            market_cap_options = {
                'Any': 0,
                'Micro (<$300M)': 0,
                'Small ($300M-$2B)': 300_000_000,
                'Mid ($2B-$10B)': 2_000_000_000,
                'Large ($10B-$200B)': 10_000_000_000,
                'Mega (>$200B)': 200_000_000_000
            }
            min_market_cap_label = st.selectbox("Min Market Cap", list(market_cap_options.keys()), index=0)
            min_market_cap = market_cap_options[min_market_cap_label]
        
        with col3:
            st.markdown("#### Other Filters")
            max_pe = st.number_input("Max P/E Ratio", min_value=0.0, value=100.0, step=5.0)
            min_volume = st.number_input("Min Volume", min_value=0, value=0, step=100000)
        
        # Sector filter
        st.markdown("#### Sector Filter (Optional)")
        all_sectors = ['Technology', 'Healthcare', 'Financial Services', 'Consumer Cyclical', 
                       'Industrials', 'Communication Services', 'Consumer Defensive', 
                       'Energy', 'Real Estate', 'Basic Materials', 'Utilities']
        
        selected_sectors = st.multiselect(
            "Select sectors (leave empty for all)",
            all_sectors,
            default=[]
        )
        
        if st.button("🔍 Run Screener", type="primary"):
            with st.spinner("Screening stocks... This may take a minute..."):
                screener_results = stock_screener(
                    min_price=min_price,
                    max_price=max_price,
                    min_market_cap=min_market_cap,
                    max_pe=max_pe,
                    min_volume=min_volume,
                    sectors=selected_sectors if selected_sectors else None
                )
            
            if not screener_results.empty:
                st.success(f"✅ Found {len(screener_results)} stocks matching your criteria")
                
                st.markdown("---")
                st.markdown("### 📊 Screening Results")
                
                # Format results
                display_results = screener_results.copy()
                display_results['Price'] = display_results['Price'].apply(lambda x: f"${x:.2f}")
                display_results['Change %'] = display_results['Change %'].apply(lambda x: f"{x:+.2f}%")
                display_results['Market Cap'] = display_results['Market Cap'].apply(
                    lambda x: f"${x/1e9:.2f}B" if x >= 1e9 else f"${x/1e6:.2f}M"
                )
                display_results['Volume'] = display_results['Volume'].apply(lambda x: f"{x:,.0f}")
                
                st.dataframe(display_results, hide_index=True, use_container_width=True)
                
                # Download option
                csv = screener_results.to_csv(index=False)
                st.download_button(
                    label="📥 Download Screener Results",
                    data=csv,
                    file_name=f"screener_results_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
                
                # Quick stats
                st.markdown("---")
                st.markdown("### 📈 Quick Statistics")
                
                col1, col2, col3, col4 = st.columns(4)
                
                col1.metric("Total Stocks", len(screener_results))
                col2.metric("Avg Price", f"${screener_results['Price'].mean():.2f}")
                col3.metric("Avg Change", f"{screener_results['Change %'].mean():+.2f}%")
                col4.metric("Sectors", screener_results['Sector'].nunique())
                
                # Sector breakdown
                st.markdown("---")
                st.markdown("### 🏭 Sector Breakdown")
                
                sector_breakdown = screener_results['Sector'].value_counts()
                
                fig = go.Figure(data=[go.Bar(
                    x=sector_breakdown.index,
                    y=sector_breakdown.values,
                    marker_color='#42a5f5'
                )])
                
                fig.update_layout(
                    title='Stocks by Sector',
                    xaxis_title='Sector',
                    yaxis_title='Number of Stocks',
                    height=400,
                    template='plotly_dark'
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
            else:
                st.warning("No stocks found matching your criteria. Try adjusting the filters.")
    
    # Footer
    st.markdown("---")
    # Footer placeholder

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error(f"Application Error: {str(e)}")
        st.info("Please refresh the page and try again.")
        import traceback
        with st.expander("Error Details"):
            st.code(traceback.format_exc())
