from __future__ import annotations
from pathlib import Path
import csv
from .analysis import fmt
from .data import utc_now

def write_report(results: list[dict], errors: list[tuple[str, str]], out_dir: Path, timeframe: str) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    generated = utc_now()
    lines = [
        "CRYPTORESEARCH AI — INFORME DE OBSERVACIÓN",
        "=" * 58,
        f"Generado: {generated}",
        f"Marco temporal: {timeframe}",
        "Modo: EDUCATIVO / SOLO DATOS PÚBLICOS / SIN ÓRDENES",
        "",
        "AVISO: Esto no es asesoramiento financiero ni una recomendación.",
        "Los estados describen condiciones técnicas experimentales; no predicen",
        "el precio ni garantizan resultados. No se ejecutan operaciones.",
        "",
        "RESUMEN",
        "-" * 58,
        f"Activos analizados correctamente: {len(results)}",
        f"Activos con error o datos insuficientes: {len(errors)}",
        f"Posibles rupturas con volumen: {sum(r['state'] == 'POSIBLE RUPTURA' for r in results)}",
        "",
        "DETALLE POR ACTIVO",
        "-" * 58
    ]
    for r in results:
        lines.extend([
            "",
            f"[{r['symbol']}]  {r['state']}",
            f"Último cierre de vela cerrada: {fmt(r['close'], 8)}",
            f"Tendencia EMA20/50/200: {r['trend']}",
            f"EMA20: {fmt(r['ema20'], 8)} | EMA50: {fmt(r['ema50'], 8)} | EMA200: {fmt(r['ema200'], 8)}",
            f"RSI(14): {fmt(r['rsi14'], 2)} | ATR(14): {fmt(r['atr14'], 8)}",
            f"Volumen relativo: {fmt(r['volume_ratio'], 2)}x",
            f"Soporte de referencia: {fmt(r['support'], 8)}",
            f"Resistencia de referencia: {fmt(r['resistance'], 8)}",
            f"Lectura: {r['reason']}",
        ])
    if errors:
        lines.extend(["", "ERRORES / DATOS NO DISPONIBLES", "-" * 58])
        for symbol, message in errors:
            lines.append(f"{symbol}: {message}")
    lines.extend([
        "", "NOTAS METODOLÓGICAS",
        "-" * 58,
        "- Los niveles son máximos/mínimos de una ventana reciente; no son niveles infalibles.",
        "- La última vela devuelta por la API se descarta para evitar usar una vela en curso.",
        "- Un cierre por encima de resistencia no garantiza que el movimiento continúe.",
        "- Los umbrales son parámetros experimentales configurables en config.json.",
        "- GitHub Actions puede retrasar las ejecuciones programadas.",
        ""
    ])
    (out_dir / "ULTIMO_INFORME.txt").write_text("\n".join(lines), encoding="utf-8")

    csv_path = out_dir / "historico.csv"
    fields = ["generated_utc", "symbol", "close", "trend", "rsi14", "atr14",
              "volume_ratio", "support", "resistance", "state"]
    exists = csv_path.exists()
    with csv_path.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        if not exists:
            writer.writeheader()
        for r in results:
            row = {"generated_utc": generated, **{k: r.get(k) for k in fields if k != "generated_utc"}}
            writer.writerow(row)
