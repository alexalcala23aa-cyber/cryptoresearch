from __future__ import annotations
import json
import logging
from pathlib import Path
import ccxt
from cryptoresearch.analysis import analyze_symbol
from cryptoresearch.data import fetch_closed_candles
from cryptoresearch.reporting import write_report

ROOT = Path(__file__).resolve().parent

def main() -> int:
    config = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
    logging.basicConfig(filename=ROOT / "reports" / "errores.log",
                        level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    exchange_class = getattr(ccxt, config["exchange"])
    exchange = exchange_class({"enableRateLimit": True, "timeout": 20000})
    exchange.load_markets()
    results, errors = [], []
    for symbol in config["symbols"]:
        try:
            if symbol not in exchange.markets:
                raise ValueError("Par no disponible en este mercado.")
            candles = fetch_closed_candles(exchange, symbol, config["timeframe"], int(config["candle_limit"]))
            result = analyze_symbol(symbol, candles, config["parameters"])
            results.append(result)
            print(f"{symbol}: {result['state']}")
        except Exception as exc:
            message = str(exc)[:240]
            errors.append((symbol, message))
            logging.exception("Fallo al analizar %s", symbol)
            print(f"{symbol}: ERROR: {message}")
    write_report(results, errors, ROOT / "reports", config["timeframe"])
    print(f"Informe generado: {ROOT / 'reports' / 'ULTIMO_INFORME.txt'}")
    return 0 if results else 1

if __name__ == "__main__":
    raise SystemExit(main())

