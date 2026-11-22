import unittest
from cryptoresearch.analysis import Candle, ema, rsi, analyze_symbol

PARAMS = {
    "ema_fast": 20, "ema_medium": 50, "ema_slow": 200,
    "rsi_period": 14, "atr_period": 14, "volume_period": 20,
    "volume_attention_ratio": 1.3, "level_lookback": 40,
    "breakout_atr_buffer": 0.15
}

class AnalysisTests(unittest.TestCase):
    def test_ema_increasing_series(self):
        self.assertGreater(ema([float(i) for i in range(1, 30)], 10), 0)

    def test_rsi_flat_series_is_neutral(self):
        self.assertEqual(rsi([10.0] * 20, 14), 50.0)

    def test_requires_enough_history(self):
        candles = [Candle(i, 1, 2, 0.5, 1, 10) for i in range(100)]
        with self.assertRaises(ValueError):
            analyze_symbol("TEST/USD", candles, PARAMS)

if __name__ == "__main__":
    unittest.main()

