<div align="center">

# 📈 AlphaTrader

### Institutional-Grade Stock Market Analysis Platform

[![Live Demo](https://img.shields.io/badge/🚀%20Live%20Demo-Click%20to%20Open-FF4B4B?style=for-the-badge)](https://alphatrader-88jhjtkygjbc47d5wpledu.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.40%2B-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Plotly](https://img.shields.io/badge/Plotly-Interactive%20Charts-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)](https://plotly.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Stars](https://img.shields.io/github/stars/audicitty/AlphaTrader?style=for-the-badge&color=yellow)](https://github.com/audicitty/AlphaTrader/stargazers)

> **A professional-grade stock market analysis platform** built with Python & Streamlit.
> Real-time charts · 20+ trading signals · AI news sentiment · risk metrics · market overview · stock screener.
> Everything a serious trader needs — in one place, for free.

## 🌐 [Try it Live → alphatrader.streamlit.app](https://alphatrader-88jhjtkygjbc47d5wpledu.streamlit.app/)

*No installation. No signup. Just open and start analyzing.*

---

[✨ Features](#-features) &nbsp;·&nbsp; [🎓 For Students](#-for-engineering-students) &nbsp;·&nbsp; [🚀 Run Locally](#-run-locally) &nbsp;·&nbsp; [🔧 Tech Stack](#-tech-stack) &nbsp;·&nbsp; [🤝 Contributing](#-contributing)

</div>

---

## ✨ Features

AlphaTrader packs **10 powerful analysis modules** into a single web app:

<details open>
<summary><b>📈 1. Chart Analysis — TradingView-style candlestick charts</b></summary>

- Professional dark-theme candlestick charts
- Indicator overlays: **SMA 20/50/200**, **EMA 12/26**, **Bollinger Bands**
- Sub-charts: **MACD**, **RSI**, **Volume** — all in one unified view
- Timeframes: `1mo` `3mo` `6mo` `1y` `2y` `5y` `max`
- Intervals: `5m` `15m` `30m` `1h` `1d` `1wk` `1mo`

</details>

<details open>
<summary><b>🎯 2. Trading Signals — 20+ auto-generated signals</b></summary>

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
<summary><b>📊 3. Technical Indicators — all industry-standard indicators in real-time</b></summary>

```
Trend      →  SMA 20, SMA 50, SMA 200, EMA 12, EMA 26
Momentum   →  RSI (14), MACD (12,26,9), Stochastic (14,3)
Volatility →  Bollinger Bands (20,2), ATR (14), ADX (14)
Volume     →  OBV, VWAP
```

</details>

<details>
<summary><b>📰 4. News Sentiment Analysis — AI-powered market mood detection</b></summary>

- Fetches **20 latest news articles** via NewsAPI
- **VADER Sentiment Scoring** — `-1.0` (very negative) to `+1.0` (very positive)
- Generates **Buy / Sell / Hold** recommendation from news sentiment
- Sentiment timeline chart + distribution histogram
- Confidence scoring (0–100%)

</details>

<details>
<summary><b>⚠️ 5. Risk Analysis — hedge-fund style metrics</b></summary>

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
<summary><b>📋 6. Performance Metrics · 🔮 7. Quantitative Analysis · 🌍 8. Market Overview · ⚖️ 9. Stock Comparison · 🔍 10. Stock Screener</b></summary>

- **Performance:** Daily/Weekly/Monthly returns, cumulative chart, skewness, kurtosis
- **Quant Analysis:** Return distribution stats, volume ratios, advanced measures
- **Market Overview:** S&P 500 sectors heatmap, major indices, top gainers/losers, most active
- **Stock Comparison:** Compare up to 10 stocks side-by-side with normalized chart + CSV export
- **Stock Screener:** Filter 60+ stocks by price, market cap, P/E, volume, sector

</details>

---

## 🎓 For Engineering Students

> **Perfect for final year projects, mini-projects, and data science assignments.**

AlphaTrader covers **multiple CS/IT engineering domains** in one project:

| Domain | What's implemented |
|---|---|
| 📊 **Data Science** | Real-time financial data processing with Pandas & NumPy |
| 📈 **Data Visualization** | Interactive Plotly charts — candlestick, heatmap, histogram, treemap |
| 🤖 **NLP / Sentiment Analysis** | VADER sentiment scoring on live news articles |
| ⚙️ **Algorithm Design** | 20+ signal generation algorithms across 5 categories |
| 🌐 **Web Development** | Full-stack web app with Streamlit + custom CSS |
| 📡 **API Integration** | yfinance, NewsAPI — real-world data pipelines |
| 📐 **Financial Mathematics** | Sharpe Ratio, VaR, Bollinger Bands, MACD, RSI from scratch |
| ☁️ **Cloud Deployment** | Deployed on Streamlit Community Cloud |

### How to use for your project

1. **Fork this repo** on GitHub (button top-right)
2. **Run locally** or open the [live demo](https://alphatrader-88jhjtkygjbc47d5wpledu.streamlit.app/)
3. **Extend it** — add your own module, indicator, or ML model as a new tab
4. **Present it** — the dark-theme UI makes for impressive demos

> **Suggested extensions for extra marks:**
> - Add an LSTM/Prophet price prediction tab
> - Integrate options chain analysis
> - Build a portfolio tracker with P&L calculation
> - Add WhatsApp/email price alerts

---

## 🚀 Run Locally

```bash
# 1. Clone
git clone https://github.com/audicitty/AlphaTrader.git
cd AlphaTrader

# 2. Install dependencies
pip install -r requirements.txt

# 3. (Optional) Add API keys for news sentiment
cp .env.example .env
# Edit .env — free key from https://newsapi.org

# 4. Run
streamlit run professional_trading_platform.py
```

Open **http://localhost:8501**. Done.

> The app works fully without any API keys. The News Sentiment tab needs a free [NewsAPI](https://newsapi.org/register) key.

---

## 📖 Usage

```
1. Enter a stock ticker   →  AAPL, MSFT, TSLA, NVDA, RELIANCE.NS, TCS.NS
2. Choose timeframe       →  1mo | 1y | 5y | max
3. Choose interval        →  1d | 1wk | 1h | 15m
4. Explore 10 tabs
```

**Compare Stocks:** Tab ⚖️ → Enter `MSFT,GOOGL,TSLA,NVDA` → Compare Stocks

**Screen Stocks:** Tab 🔍 → Set filters → Run Screener → Export CSV

---

## ⏱️ Data Limitations

| Interval | Max History |
|---|---|
| 5m, 15m, 30m | Last 60 days |
| 1h | Last 730 days |
| 1d, 1wk, 1mo | Full history |

---

## 🔧 Tech Stack

| Layer | Technology |
|---|---|
| **UI** | [Streamlit](https://streamlit.io) + Custom CSS dark theme |
| **Charts** | [Plotly](https://plotly.com) — candlestick, line, histogram, treemap, pie |
| **Market Data** | [yfinance](https://github.com/ranaroussi/yfinance) (Yahoo Finance) |
| **Risk Analytics** | [QuantStats](https://github.com/ranaroussi/quantstats) |
| **Sentiment** | [VADER](https://github.com/cjhutto/vaderSentiment) + [NewsAPI](https://newsapi.org) |
| **Data Processing** | Pandas, NumPy |
| **Deployment** | Streamlit Community Cloud |

---

## 📁 Project Structure

```
AlphaTrader/
├── professional_trading_platform.py   # Main app — all 10 modules (~2400 lines)
├── requirements.txt                   # Python dependencies
├── .env.example                       # API key template
├── runtime.txt                        # Python version for deployment
├── LICENSE                            # MIT License
├── ARCHITECTURE_FLOWCHARTS.txt        # System architecture & data flows
└── TECHNICAL_INDICATORS_GUIDE.txt     # Beginner-friendly indicators guide
```

---

## 🐛 Troubleshooting

**"Could not fetch data"** → Check internet. Try a different ticker. Wait 10s and refresh.

**"Sentiment not working"** → Add `NEWS_API_KEY` to `.env` (free at [newsapi.org](https://newsapi.org/register)).

**"ImportError"** → `pip install quantstats`

---

## 🤝 Contributing

1. **Fork** → `git checkout -b feature/your-feature` → commit → **Pull Request**

**Ideas:** international exchanges (NSE, LSE) · ML price prediction · options chain · portfolio tracker · price alerts

---

## ⚠️ Disclaimer

> For **educational and research purposes only.** Not financial advice. Trading involves risk. Always consult a qualified financial advisor.

---

## 📄 License

MIT — see [LICENSE](LICENSE).

---

<div align="center">

**Built with Python, Streamlit & passion for the markets**

⭐ **Found this useful? Star the repo — it helps other students find it!** ⭐

[![GitHub stars](https://img.shields.io/github/stars/audicitty/AlphaTrader?style=social)](https://github.com/audicitty/AlphaTrader/stargazers)
&nbsp;&nbsp;
[![Live Demo](https://img.shields.io/badge/Live%20Demo-Open%20App-FF4B4B?style=flat)](https://alphatrader-88jhjtkygjbc47d5wpledu.streamlit.app/)

</div>
