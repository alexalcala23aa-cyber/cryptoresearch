from __future__ import annotations
from datetime import datetime, timezone
from .analysis import Candle

def fetch_closed_candles(exchange, symbol: str, timeframe: str, limit: int) -> list[Candle]:
    rows = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
    if not rows or len(rows) < 2:
        raise ValueError("La API devolvió pocas velas.")
    # CCXT devuelve normalmente la vela en curso al final. Se descarta siempre.
    closed = rows[:-1]
    candles = []
    previous_ts = None
    for row in closed:
        ts, op, high, low, close, volume = row
        vals = [op, high, low, close, volume]
        if any(v is None for v in vals):
            continue
        if not (low <= min(op, close) <= max(op, close) <= high):
            continue
        if volume < 0 or (previous_ts is not None and ts <= previous_ts):
            continue
        candles.append(Candle(int(ts), float(op), float(high), float(low), float(close), float(volume)))
        previous_ts = ts
    return candles

def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

