import time
import pandas as pd
import yfinance as yf
import logging
from strategies.bollinger import apply_bollinger

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(message)s",
    handlers=[
        logging.FileHandler("live_trading.log"),
        logging.StreamHandler(),
    ],
)


def run_live_trading(ticker: str = "AAPL", interval: str = "1m", cash: float = 10000.0):
    """볼린저 밴드 신호로 간단한 실시간 매매를 시뮬레이션합니다."""
    data = pd.DataFrame()
    position = 0.0
    cash_balance = cash
    start_cash = cash
    last_processed = None
    logging.info("%s 종목 실시간 거래 시작 (초기 자본: $%.2f)", ticker, cash)
    while True:
        # Fetch the latest intraday data
        df = yf.download(ticker, period="1d", interval=interval, auto_adjust=False)
        if df.empty:
            logging.warning("데이터를 가져오지 못함")
            time.sleep(60)
            continue
        if not data.empty:
            df = df[df.index > data.index[-1]]
        if df.empty:
            time.sleep(60)
            continue
        data = pd.concat([data, df])
        if len(data) > 1000:
            data = data.iloc[-1000:]
        signals = apply_bollinger(data)
        new_signals = signals if last_processed is None else signals[signals.index > last_processed]
        for ts, row in new_signals.iterrows():
            price = row["Close"]
            if row["Buy"] and cash_balance > 0:
                position = cash_balance / price
                cash_balance = 0
                logging.info("%s 매수 %.4f주 (가격 %.2f)", ts, position, price)
            elif row["Sell"] and position > 0:
                cash_balance = position * price
                position = 0
                logging.info("%s 매도 (가격 %.2f)", ts, price)
            value = cash_balance + position * price
            profit = value - start_cash
            logging.info("%s 포트폴리오 가치 %.2f (수익 %.2f)", ts, value, profit)
            last_processed = ts
        time.sleep(60)


if __name__ == "__main__":
    run_live_trading()
