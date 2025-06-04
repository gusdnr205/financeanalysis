import os
import pandas as pd
import yfinance as yf
from .bollinger import apply_bollinger

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

def load_data(ticker: str, start: str, end: str) -> pd.DataFrame:
    path = os.path.join(DATA_DIR, f"{ticker}_{start}_{end}.csv")
    if os.path.exists(path):
        df = pd.read_csv(path, index_col=0, parse_dates=True)
    else:
        df = yf.download(ticker, start=start, end=end, auto_adjust=False)
        df.to_csv(path)
    return df


def backtest_bollinger(ticker: str, start: str = "2020-01-01", end: str = "2024-01-01", cash: float = 10000.0):
    df = load_data(ticker, start, end)
    df = apply_bollinger(df)
    cash_balance = cash
    position = 0.0
    trades = []
    for date, row in df.iterrows():
        if row['Buy'] and cash_balance > 0:
            position = cash_balance / row['Close']
            cash_balance = 0
            trades.append({"action": "buy", "date": date.isoformat(), "price": float(row['Close'])})
        elif row['Sell'] and position > 0:
            cash_balance = position * row['Close']
            position = 0
            trades.append({"action": "sell", "date": date.isoformat(), "price": float(row['Close'])})
    final_value = cash_balance + position * df.iloc[-1]['Close']
    roi = (final_value - cash) / cash
    return {"final_value": final_value, "roi": roi, "trades": trades}
