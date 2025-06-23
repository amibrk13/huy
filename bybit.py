import httpx

BASE_URL = "https://api.bybit.com"

async def get_kline(symbol: str, interval: str):
    url = f"{BASE_URL}/spot/quote/v1/kline"
    params = {"symbol": symbol, "interval": interval, "limit": 1}
    async with httpx.AsyncClient() as client:
        r = await client.get(url, params=params)
        r.raise_for_status()
        data = r.json()
        if data["ret_code"] == 0 and data["result"]:
            k = data["result"][0]
            return {
                "open": k[1],
                "high": k[2],
                "low": k[3],
                "close": k[4],
                "volume": k[5],
                "timestamp": k[0]
            }
        return None

async def get_ticker(symbol: str):
    url = f"{BASE_URL}/spot/quote/v1/ticker/24hr"
    params = {"symbol": symbol}
    async with httpx.AsyncClient() as client:
        r = await client.get(url, params=params)
        r.raise_for_status()
        data = r.json()
        if data["ret_code"] == 0 and data["result"]:
            t = data["result"]
            return {
                "lastPrice": t["lastPrice"],
                "priceChangePercent": t["priceChangePercent"],
                "highPrice": t["highPrice"],
                "lowPrice": t["lowPrice"],
                "baseVolume": t["volume"],
                "quoteVolume": t["quoteVolume"],
                "bidPrice": t["bidPrice"],
                "askPrice": t["askPrice"],
                "openPrice": t["openPrice"],
                "closePrice": t["closePrice"]
            }
        return None