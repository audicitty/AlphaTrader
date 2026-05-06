<div align="center">

<img src="https://img.shields.io/badge/AlphaTrader-Professional%20Trading%20Platform-1a1a2e?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZmlsbD0iIzAwZmY4OCIgZD0iTTIgMjBoMjBWNEwyIDIwem0xOC0ySDRMMTggNnYxMnoiLz48L3N2Zz4=" alt="AlphaTrader"/>

# 📈 AlphaTrader

### Institutional-Grade Stock Market Analysis Platform

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.40%2B-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Plotly](https://img.shields.io/badge/Plotly-Interactive%20Charts-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)](https://plotly.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Stars](https://img.shields.io/github/stars/audicitty/AlphaTrader?style=for-the-badge&color=yellow)](https://github.com/audicitty/AlphaTrader/stargazers)
[![Forks](https://img.shields.io/github/forks/audicitty/AlphaTrader?style=for-the-badge&color=blue)](https://github.com/audicitty/AlphaTrader/network/members)

> **A professional-grade stock market analysis platform** built with Python & Streamlit.
> Real-time charts · 20+ trading signals · AI news sentiment · risk metrics · market overview · stock screener.
> Everything a serious trader needs — in one place, for free.

[🚀 Quick Start](#-quick-start) &nbsp;·&nbsp; [✨ Features](#-features) &nbsp;·&nbsp; [📸 Screenshots](#-screenshots) &nbsp;·&nbsp; [🔧 Tech Stack](#-tech-stack) &nbsp;·&nbsp; [🤝 Contributing](#-contributing)

</div>

---

## 📸 Screenshots

<div align="center">

| 📈 TradingView-Style Charts | 🎯 20+ Auto Trading Signals |
|:--:|:--:|
| Professional dark-theme candlestick charts with SMA, EMA, Bollinger Bands, MACD, RSI & Volume overlays | Automatically generated bullish/bearish/neutral signals across Trend · Momentum · Volatility · Volume · Price Action |

| 🌍 Live Market Overview | ⚖️ Side-by-Side Stock Comparison |
|:--:|:--:|
| S&P 500 sectors heatmap · major indices · top gainers/losers · most active stocks | Compare up to 10 stocks with normalized chart, full metrics table, and CSV export |

</div>

> Dark theme UI — TradingView-inspired interface with real-time data from Yahoo Finance.

---

## ✨ Features

AlphaTrader packs **10 powerful analysis modules** into a single web app:

<details open>
<summary><b>📈 1. Chart Analysis</b></summary>

- TradingView-style **candlestick charts** with professional dark theme
- Indicator overlays: **SMA 20/50/200**, **EMA 12/26**, **Bollinger Bands**
- Sub-charts: **MACD**, **RSI**, **Volume** — all in one unified view
- Configurable timeframes: `1mo` `3mo` `6mo` `1y` `2y` `5y` `max`
- Configurable intervals: `5m` `15m` `30m` `1h` `1d` `1wk` `1mo`
- Key price levels: 52-Week High/Low, 20-Day Average

</details>

<details open>
<summary><b>🎯 2. Trading Signals — 20+ Signals</b></summary>

Automatically generated signals across 5 categories:

| Category | Signals |
|---|---|
| 📊 **Trend** | Strong Uptrend/Downtrend, Golden Cross, Death Cross, SMA alignment |
| ⚡ **Momentum** | RSI Overbought/Oversold, RSI Divergence, MACD Crossover |
| 💥 **Volatility** | Bollinger Band Squeeze, Above/Below BB, ATR levels |
| 📦 **Volume** | Volume Spike, OBV Trend, Volume Confirmation |
| 🕯️ **Price Action** | Daily Change, 52-Week Position, Support/Resistance, VWAP |

Color-coded: 🟢 Bullish &nbsp;·&nbsp; 🔴 Bearish &nbsp;·&nbsp; 🔵 Opportunity &nbsp;·&nbsp; 🟡 Caution

</details>

<details>
<summary><b>📊 3. Technical Indicators</b></summary>

All industry-standard indicators calculated in real-time:

```
Trend      →  SMA 20, SMA 50, SMA 200, EMA 12, EMA 26
Momentum   →  RSI (14), MACD (12,26,9), Stochastic (14,3)
Volatility →  Bollinger Bands (20,2), ATR (14), ADX (14)
Volume     →  OBV, VWAP
```

</details>

<details>
<summary><b>📰 4. News Sentiment Analysis</b></summary>

- Fetches **20 latest news articles** via NewsAPI
- **VADER Sentiment Scoring** — from `-1.0` (very negative) to `+1.0` (very positive)
- Generates **Buy / Sell / Hold** recommendation from aggregated news sentiment
- Sentiment timeline chart + distribution histogram
- Confidence scoring (0–100%)

</details>

<details>
<summary><b>⚠️ 5. Risk Analysis</b></summary>

Hedge-fund style risk metrics:

| Metric | Description |
|---|---|
| **Sharpe Ratio** | Risk-adjusted return (>1 good, >2 excellent) |
| **Sortino Ratio** | Downside-only risk-adjusted return |
| **Max Drawdown** | Largest peak-to-trough decline |
| **Volatility** | Annualized price volatility |
| **VaR (95%)** | Max expected daily loss at 95% confidence |
| **Calmar Ratio** | Annual return / max drawdown |
| **Win Rate** | % of days with positive return |

</details>

<details>
<summary><b>📋 6. Performance Metrics</b></summary>

- Returns: Daily · Weekly · Monthly · Full Period
- Returns distribution histogram
- Cumulative compounded returns chart
- Statistical measures: Mean, Median, Std Dev, Skewness, Kurtosis

</details>

<details>
<summary><b>🔮 7. Quantitative Analysis</b></summary>

- Statistical analysis of price return distributions
- Volume metrics: Average vs Current, Volume Ratio, Max/Min
- Advanced quant measures for deep-dive research

</details>

<details>
<summary><b>🌍 8. Market Overview Dashboard</b></summary>

One glance at the entire market:

- **Major Indices**: S&P 500, Dow Jones, NASDAQ, Russell 2000, VIX
- **Sector Heatmap**: All 11 S&P 500 sectors with % change (interactive treemap)
- **Top Gainers & Losers**: Live movers from 30+ popular stocks
- **Most Active**: Highest volume stocks of the day

</details>

<details>
<summary><b>⚖️ 9. Stock Comparison Tool</b></summary>

Compare up to **10 stocks side-by-side**:

- Normalized price chart (Base = 100) for fair apple-to-apple comparison
- Full metrics: Price · Market Cap · P/E · Beta · Dividend Yield
- Returns comparison: 1M / 3M / 1Y
- Volatility · RSI · Relative Strength vs S&P 500
- Sector distribution pie chart
- **CSV export** of all comparison data

</details>

<details>
<summary><b>🔍 10. Stock Screener</b></summary>

Filter 60+ stocks by your own criteria:

| Filter | Options |
|---|---|
| **Price Range** | Min / Max price ($) |
| **Market Cap** | Micro → Mega cap |
| **P/E Ratio** | Maximum P/E filter |
| **Volume** | Minimum daily volume |
| **Sector** | Any of 11 S&P 500 sectors |

Results include: Symbol · Name · Price · Change% · Market Cap · P/E · Volume · Sector — with **CSV export**.

</details>

---

## 🚀 Quick Start

### Prerequisites

- Python **3.10+**
- pip

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/audicitty/AlphaTrader.git
cd AlphaTrader

# 2. Install dependencies
pip install -r requirements.txt

# 3. (Optional) Set up API keys for news sentiment
cp .env.example .env
# Edit .env and add your free NewsAPI key from https://newsapi.org

# 4. Run the app
streamlit run professional_trading_platform.py
```

Open **http://localhost:8501** in your browser. That's it.

> **Note:** The app works fully without any API keys. The News Sentiment tab requires a free [NewsAPI](https://newsapi.org/register) key.

---

## 📖 Usage Guide

```
1. Enter a stock ticker in the sidebar  →  e.g., AAPL, MSFT, TSLA, NVDA, RELIANCE.NS
2. Choose your timeframe               →  1mo | 1y | 5y | max
3. Choose your interval                →  1d | 1wk | 1h | 15m
4. Explore the 10 analysis tabs
```

**Compare Stocks**
```
Tab ⚖️ → Enter: MSFT,GOOGL,TSLA,NVDA → Select period → Compare Stocks
```

**Screen Stocks**
```
Tab 🔍 → Set price / market cap / P/E / sector filters → Run Screener → Export CSV
```

**News Sentiment**
```
Tab 📰 → Click "Analyze News Sentiment" → View score + recommendation + all articles
```

---

## ⏱️ Data Limitations

| Interval | Max Historical Data |
|---|---|
| 5m, 15m, 30m | Last 60 days |
| 1h | Last 730 days |
| 1d, 1wk, 1mo | Full history available |

> The app warns you automatically if you select an incompatible period/interval combination.

---

## 🔧 Tech Stack

| Layer | Technology |
|---|---|
| **UI Framework** | [Streamlit](https://streamlit.io) + Custom CSS dark theme |
| **Charts** | [Plotly](https://plotly.com) — candlestick, line, bar, histogram, treemap, pie |
| **Market Data** | [yfinance](https://github.com/ranaroussi/yfinance) (Yahoo Finance) |
| **Technical Indicators** | [pandas-ta](https://github.com/twopirllc/pandas-ta) + NumPy |
| **Risk Analytics** | [QuantStats](https://github.com/ranaroussi/quantstats) |
| **Sentiment** | [VADER](https://github.com/cjhutto/vaderSentiment) + [NewsAPI](https://newsapi.org) |
| **Data Processing** | Pandas, NumPy, statsmodels, scikit-learn |

---

## 📁 Project Structure

```
AlphaTrader/
│
├── professional_trading_platform.py   # Main app — all 10 modules
├── requirements.txt                   # Python dependencies
├── .env.example                       # API key template (copy to .env)
├── LICENSE                            # MIT License
├── README.md                          # This file
│
├── ARCHITECTURE_FLOWCHARTS.txt        # System architecture & data flows
└── TECHNICAL_INDICATORS_GUIDE.txt     # Beginner-friendly indicators guide
```

---

## 🐛 Troubleshooting

**"Could not fetch data for symbol"**
→ Check your internet. Try a different ticker. Yahoo Finance may be rate-limited — wait 10s and refresh.

**"Sentiment analysis not working"**
→ Add your `NEWS_API_KEY` to a `.env` file (free key from [newsapi.org](https://newsapi.org/register)).

**"Indicators missing / ImportError"**
```bash
pip install pandas-ta quantstats
```

**"App is slow"**
→ Use shorter timeframes. Fewer comparison stocks. Restart to clear Streamlit cache.

---

## 🤝 Contributing

Contributions are welcome! Here's how:

1. **Fork** this repository
2. **Create** a feature branch: `git checkout -b feature/amazing-feature`
3. **Commit** your changes: `git commit -m 'Add amazing feature'`
4. **Push** to the branch: `git push origin feature/amazing-feature`
5. **Open** a Pull Request

**Ideas for contributions:**
- 🌐 Add international stock exchanges (NSE, LSE, TSX)
- 🤖 ML-based price prediction module
- 📊 Options chain analysis
- 🔔 Price alert system
- 🌙 Additional color themes
- 📱 Mobile-responsive layout improvements

---

## ⚠️ Disclaimer

> **This platform is for EDUCATIONAL and RESEARCH purposes ONLY.**
>
> - Does **NOT** constitute financial or investment advice
> - Past performance does **NOT** guarantee future results
> - Trading involves **substantial risk of loss**
> - Always consult a **qualified financial advisor** before investing
> - Data sourced from third-party APIs may be delayed or inaccurate

---

## 📄 License

Distributed under the MIT License. See [LICENSE](LICENSE) for details.

---

<div align="center">

**Built with Python, Streamlit & love for the markets**

⭐ **If AlphaTrader saves you time or helps your research — drop a star!** ⭐

[![GitHub stars](https://img.shields.io/github/stars/audicitty/AlphaTrader?style=social)](https://github.com/audicitty/AlphaTrader/stargazers)
&nbsp;&nbsp;
[![GitHub forks](https://img.shields.io/github/forks/audicitty/AlphaTrader?style=social)](https://github.com/audicitty/AlphaTrader/network/members)

</div>
