# Finance Analysis

This project analyzes financial data using Bollinger Bands and provides a FastAPI server for real-time tracking and simple backtesting.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

Start the FastAPI server:

```bash
uvicorn server:app --reload
```

Then access:

- `/analyze/{ticker}` – Get latest Bollinger Band signals for a ticker
- `/backtest/{ticker}` – Run a backtest on historical data
