# bollinger_trader/main.py
import os
import yfinance as yf
import matplotlib.pyplot as plt
from strategies.bollinger import apply_bollinger
os.makedirs("output", exist_ok=True)  # <= 여기에 추가

ticker = 'AAPL'
df = yf.download(ticker, start='2022-01-01', end='2024-12-31', auto_adjust=False)
df = apply_bollinger(df)

plt.figure(figsize=(14, 6))
plt.plot(df['Close'], label='Close')
plt.plot(df['MA'], label='MA')
plt.plot(df['Upper'], label='Upper Band')
plt.plot(df['Lower'], label='Lower Band')
plt.fill_between(df.index, df['Lower'], df['Upper'], color='gray', alpha=0.1)
plt.scatter(df[df['Buy']].index, df[df['Buy']]['Close'], color='green', marker='^', label='Buy')
plt.scatter(df[df['Sell']].index, df[df['Sell']]['Close'], color='red', marker='v', label='Sell')
plt.legend()
plt.title(f"{ticker} - Bollinger Bands")
plt.grid(True)
plt.savefig("output/bollinger_result.png")
plt.show()
