from fastapi import FastAPI
from bybit import get_kline, get_ticker
import asyncio

app = FastAPI()

SYMBOLS = ["BTCUSDT", "BONKUSDT"]
TIMEFRAMES = ["1m", "5m", "15m", "1h", "4h", "1d"]

@app.get("/market")
async def market():
    result = {}
    for symbol in SYMBOLS:
        ticker = await get_ticker(symbol)
        klines = {}
        # Gather klines concurrently for all timeframes for this symbol
        kline_tasks = [get_kline(symbol, tf) for tf in TIMEFRAMES]
        klines_results = await asyncio.gather(*kline_tasks)
        for i, tf in enumerate(TIMEFRAMES):
            klines[tf] = klines_results[i]
        result[symbol] = {
            "ticker": ticker,
            "klines": klines
        }
    return result