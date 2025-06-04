from fastapi import FastAPI
import yfinance as yf
import os
from strategies.bollinger import apply_bollinger
from strategies.backtest import backtest_bollinger

app = FastAPI()
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

@app.get("/analyze/{ticker}")
async def analyze(ticker: str):
    df = yf.download(ticker, period="1mo", interval="1d", auto_adjust=False)
    if df.empty:
        return {"error": "No data"}
    df = apply_bollinger(df)
    last = df.iloc[-1]
    return {
        "close": float(last["Close"]),
        "ma": float(last["MA"]),
        "upper": float(last["Upper"]),
        "lower": float(last["Lower"]),
        "buy_signal": bool(last["Buy"]),
        "sell_signal": bool(last["Sell"]),
    }

@app.get("/backtest/{ticker}")
async def backtest(ticker: str, start: str = "2022-01-01", end: str = "2024-12-31"):
    result = backtest_bollinger(ticker, start, end)
    return result
