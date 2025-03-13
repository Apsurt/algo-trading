import pandas as pd
import numpy as np
from ta.trend import SMAIndicator, EMAIndicator, MACD, ADXIndicator
from ta.momentum import RSIIndicator, StochasticOscillator
from ta.volatility import BollingerBands, AverageTrueRange
from ta.volume import OnBalanceVolumeIndicator, VolumePriceTrendIndicator
from enum import Enum
from structs import Indicator
from typing import Tuple, Optional, Dict, Union

class Indicators:
    def __init__(self, data: pd.DataFrame, period: int = 20,
                 fast_period: int = 12, slow_period: int = 26, signal_period: int = 9,
                 std_dev: float = 2.0, k_period: int = 14, d_period: int = 3, smooth_k: int = 3) -> None:
        self.data = data
        self.period = period
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.signal_period = signal_period
        self.std_dev = std_dev
        self.k_period = k_period
        self.d_period = d_period
        self.smooth_k = smooth_k

    def _get_price_column(self, column_name: str) -> pd.Series:
        # Ensure we're returning a proper Series (1D) not a DataFrame
        if column_name in self.data.columns:
            return self.data[column_name].squeeze()
        # In case we need to search for columns
        possible_column = next((col for col in self.data.columns if col.endswith(column_name)), None)
        if possible_column:
            return self.data[possible_column].squeeze()
        raise ValueError(f"Column {column_name} not found in data")

    def SMA(self) -> float:
        close_prices = self._get_price_column('Close')
        sma_indicator = SMAIndicator(close=close_prices, window=self.period)
        sma_values = sma_indicator.sma_indicator()
        return float(sma_values.iloc[-1])

    def EMA(self) -> float:
        close_prices = self._get_price_column('Close')
        ema_indicator = EMAIndicator(close=close_prices, window=self.period)
        ema_values = ema_indicator.ema_indicator()
        return float(ema_values.iloc[-1])

    def MACD(self) -> Dict[str, float]:
        # Returns dictionary of MACD values since it produces multiple values
        close_prices = self._get_price_column('Close')
        macd_indicator = MACD(
            close=close_prices,
            window_slow=self.slow_period,
            window_fast=self.fast_period,
            window_sign=self.signal_period
        )

        return {
            'macd': float(macd_indicator.macd().iloc[-1]),
            'signal': float(macd_indicator.macd_signal().iloc[-1]),
            'histogram': float(macd_indicator.macd_diff().iloc[-1])
        }

    def RSI(self) -> float:
        close_prices = self._get_price_column('Close')
        rsi_indicator = RSIIndicator(close=close_prices, window=self.period)
        return float(rsi_indicator.rsi().iloc[-1])

    def BBANDS(self) -> Dict[str, float]:
        # Returns dictionary of Bollinger Band values since it produces multiple values
        close_prices = self._get_price_column('Close')
        bb_indicator = BollingerBands(close=close_prices, window=self.period, window_dev=self.std_dev)

        return {
            'upper': float(bb_indicator.bollinger_hband().iloc[-1]),
            'middle': float(bb_indicator.bollinger_mavg().iloc[-1]),
            'lower': float(bb_indicator.bollinger_lband().iloc[-1])
        }

    def ATR(self) -> float:
        high_prices = self._get_price_column('High')
        low_prices = self._get_price_column('Low')
        close_prices = self._get_price_column('Close')

        atr_indicator = AverageTrueRange(
            high=high_prices,
            low=low_prices,
            close=close_prices,
            window=self.period
        )
        return float(atr_indicator.average_true_range().iloc[-1])

    def ADX(self) -> Dict[str, float]:
        # Returns dictionary of ADX values since it produces multiple values
        high_prices = self._get_price_column('High')
        low_prices = self._get_price_column('Low')
        close_prices = self._get_price_column('Close')

        adx_indicator = ADXIndicator(
            high=high_prices,
            low=low_prices,
            close=close_prices,
            window=self.period
        )

        return {
            'adx': float(adx_indicator.adx().iloc[-1]),
            'pdi': float(adx_indicator.adx_pos().iloc[-1]),
            'ndi': float(adx_indicator.adx_neg().iloc[-1])
        }

    def STOCH(self) -> Dict[str, float]:
        # Returns dictionary of stochastic oscillator values since it produces multiple values
        high_prices = self._get_price_column('High')
        low_prices = self._get_price_column('Low')
        close_prices = self._get_price_column('Close')

        stoch_indicator = StochasticOscillator(
            high=high_prices,
            low=low_prices,
            close=close_prices,
            window=self.k_period,
            smooth_window=self.smooth_k
        )

        return {
            '%K': float(stoch_indicator.stoch().iloc[-1]),
            '%D': float(stoch_indicator.stoch_signal().iloc[-1])
        }

    def OBV(self) -> float:
        close_prices = self._get_price_column('Close')
        volume = self._get_price_column('Volume')

        obv_indicator = OnBalanceVolumeIndicator(close=close_prices, volume=volume)
        return float(obv_indicator.on_balance_volume().iloc[-1])

    def VPT(self) -> float:
        close_prices = self._get_price_column('Close')
        volume = self._get_price_column('Volume')

        vpt_indicator = VolumePriceTrendIndicator(close=close_prices, volume=volume)
        return float(vpt_indicator.volume_price_trend().iloc[-1])
