from __future__ import annotations
from dataclasses import dataclass
from typing import Any
import math

@dataclass
class Candle:
    timestamp: int
    open: float
    high: float
    low: float
    close: float
    volume: float

def ema(values: list[float], period: int) -> float | None:
    if len(values) < period:
        return None
    alpha = 2 / (period + 1)
    result = sum(values[:period]) / period
    for value in values[period:]:
        result = alpha * value + (1 - alpha) * result
    return result

def rsi(values: list[float], period: int = 14) -> float | None:
    if len(values) < period + 1:
        return None
    gains, losses = [], []
    for a, b in zip(values[-period-1:-1], values[-period:]):
        delta = b - a
        gains.append(max(delta, 0.0))
        losses.append(max(-delta, 0.0))
    avg_gain = sum(gains) / period
    avg_loss = sum(losses) / period
    if avg_loss == 0:
        return 100.0 if avg_gain > 0 else 50.0
    rs = avg_gain / avg_loss
    return 100 - 100 / (1 + rs)

def atr(candles: list[Candle], period: int = 14) -> float | None:
    if len(candles) < period + 1:
        return None
    trs = []
    for prev, cur in zip(candles[-period-1:-1], candles[-period:]):
        trs.append(max(cur.high-cur.low, abs(cur.high-prev.close), abs(cur.low-prev.close)))
    return sum(trs) / period

def analyze_symbol(symbol: str, candles: list[Candle], params: dict[str, Any]) -> dict[str, Any]:
    if len(candles) < 205:
        raise ValueError(f"Histórico insuficiente: {len(candles)} velas; se necesitan al menos 205.")
    closes = [c.close for c in candles]
    volumes = [c.volume for c in candles]
    last = candles[-1]
    e20 = ema(closes, int(params["ema_fast"]))
    e50 = ema(closes, int(params["ema_medium"]))
    e200 = ema(closes, int(params["ema_slow"]))
    rv = rsi(closes, int(params["rsi_period"]))
    av = atr(candles, int(params["atr_period"]))
    vol_period = int(params["volume_period"])
    vol_avg = sum(volumes[-vol_period-1:-1]) / vol_period
    vol_ratio = last.volume / vol_avg if vol_avg > 0 else None
    lookback = int(params["level_lookback"])
    recent = candles[-lookback-1:-1]
    resistance = max(c.high for c in recent)
    support = min(c.low for c in recent)
    trend = "MIXTA"
    if e20 is not None and e50 is not None and e200 is not None:
        if e20 > e50 > e200:
            trend = "ALCISTA"
        elif e20 < e50 < e200:
            trend = "BAJISTA"
    buffer = (av or 0) * float(params["breakout_atr_buffer"])
    breakout = last.close > resistance + buffer
    vol_attention = vol_ratio is not None and vol_ratio >= float(params["volume_attention_ratio"])
    state = "OBSERVACIÓN"
    reason = "No se confirma un cierre por encima del máximo del periodo observado."
    if breakout and vol_attention:
        state = "POSIBLE RUPTURA"
        reason = "Cierre por encima de la resistencia reciente y volumen relativo elevado; requiere seguimiento, no confirma continuidad."
    elif breakout:
        state = "RUPTURA SIN CONFIRMACIÓN DE VOLUMEN"
        reason = "El cierre supera la resistencia, pero el volumen no alcanza el umbral experimental."
    return {
        "symbol": symbol, "timestamp": last.timestamp, "close": last.close,
        "ema20": e20, "ema50": e50, "ema200": e200, "rsi14": rv, "atr14": av,
        "volume_ratio": vol_ratio, "support": support, "resistance": resistance,
        "trend": trend, "state": state, "reason": reason
    }

def fmt(value: Any, digits: int = 4) -> str:
    if value is None:
        return "N/D"
    if isinstance(value, float) and not math.isfinite(value):
        return "N/D"
    return f"{value:,.{digits}f}"

