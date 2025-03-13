import pandas as pd
import numpy as np
from ta.trend import SMAIndicator, EMAIndicator, MACD, ADXIndicator
from ta.momentum import RSIIndicator, StochasticOscillator
from ta.volatility import BollingerBands, AverageTrueRange
from ta.volume import OnBalanceVolumeIndicator, VolumePriceTrendIndicator
from enum import Enum
from structs import Indicator
from typing import Tuple, Optional

class Indicators:
    def __init__(self, data: pd.DataFrame) -> None:
        self.data: pd.DataFrame = data
        self.period = 20  # Default period
        pass

    def _get_price_column(self, column_name: str) -> pd.Series:
        """Helper method to get price column regardless of ticker symbol"""
        if self.data is not pd.Series or self.data.columns :
            raise TypeError
        return self.data[next(col for col in self.data.columns if col[0] == column_name)]

    def SMA(self, period: Optional[int] = None) -> Tuple[Indicator, float]:
        """
        Calculate Simple Moving Average (SMA)
        Returns:
            Tuple[Indicator, float]: A tuple containing the indicator type and the calculated SMA value
        """
        if period is not None:
            self.period = period

        close_prices = self._get_price_column('Close')
        sma_indicator = SMAIndicator(close=close_prices, window=self.period)
        val = float(sma_indicator.sma_indicator().iloc[-1])
        return (Indicator.SMA, val)

    def EMA(self, period: Optional[int] = None) -> Tuple[Indicator, float]:
        """
        Calculate Exponential Moving Average (EMA)
        Returns:
            Tuple[Indicator, float]: A tuple containing the indicator type and the calculated EMA value
        """
        if period is not None:
            self.period = period

        close_prices = self._get_price_column('Close')
        ema_indicator = EMAIndicator(close=close_prices, window=self.period)
        val = float(ema_indicator.ema_indicator().iloc[-1])
        return (Indicator.EMA, val)

    def MACD(self, fast_period: int = 12, slow_period: int = 26, signal_period: int = 9) -> Tuple[Indicator, dict]:
        """
        Calculate Moving Average Convergence Divergence (MACD)
        Returns:
            Tuple[Indicator, dict]: A tuple containing the indicator type and a dictionary with MACD values
        """
        close_prices = self._get_price_column('Close')
        macd_indicator = MACD(
            close=close_prices,
            window_slow=slow_period,
            window_fast=fast_period,
            window_sign=signal_period
        )

        macd_values = {
            'macd': float(macd_indicator.macd().iloc[-1]),
            'signal': float(macd_indicator.macd_signal().iloc[-1]),
            'histogram': float(macd_indicator.macd_diff().iloc[-1])
        }
        return (Indicator.MACD, macd_values)

    def RSI(self, period: Optional[int] = None) -> Tuple[Indicator, float]:
        """
        Calculate Relative Strength Index (RSI)
        Returns:
            Tuple[Indicator, float]: A tuple containing the indicator type and the calculated RSI value
        """
        if period is not None:
            self.period = period

        close_prices = self._get_price_column('Close')
        rsi_indicator = RSIIndicator(close=close_prices, window=self.period)
        val = float(rsi_indicator.rsi().iloc[-1])
        return (Indicator.RSI, val)

    def BBANDS(self, period: Optional[int] = None, std_dev: float = 2.0) -> Tuple[Indicator, dict]:
        """
        Calculate Bollinger Bands
        Returns:
            Tuple[Indicator, dict]: A tuple containing the indicator type and a dictionary with Bollinger Bands values
        """
        if period is not None:
            self.period = period

        close_prices = self._get_price_column('Close')
        bb_indicator = BollingerBands(close=close_prices, window=self.period, window_dev=std_dev)

        bb_values = {
            'upper': float(bb_indicator.bollinger_hband().iloc[-1]),
            'middle': float(bb_indicator.bollinger_mavg().iloc[-1]),
            'lower': float(bb_indicator.bollinger_lband().iloc[-1])
        }
        return (Indicator.BBANDS, bb_values)

    def ATR(self, period: Optional[int] = None) -> Tuple[Indicator, float]:
        """
        Calculate Average True Range (ATR)
        Returns:
            Tuple[Indicator, float]: A tuple containing the indicator type and the calculated ATR value
        """
        if period is not None:
            self.period = period

        high_prices = self._get_price_column('High')
        low_prices = self._get_price_column('Low')
        close_prices = self._get_price_column('Close')

        atr_indicator = AverageTrueRange(
            high=high_prices,
            low=low_prices,
            close=close_prices,
            window=self.period
        )
        val = float(atr_indicator.average_true_range().iloc[-1])
        return (Indicator.ATR, val)

    def ADX(self, period: Optional[int] = None) -> Tuple[Indicator, dict]:
        """
        Calculate Average Directional Index (ADX)
        Returns:
            Tuple[Indicator, dict]: A tuple containing the indicator type and a dictionary with ADX values
        """
        if period is not None:
            self.period = period

        high_prices = self._get_price_column('High')
        low_prices = self._get_price_column('Low')
        close_prices = self._get_price_column('Close')

        adx_indicator = ADXIndicator(
            high=high_prices,
            low=low_prices,
            close=close_prices,
            window=self.period
        )

        adx_values = {
            'adx': float(adx_indicator.adx().iloc[-1]),
            'pdi': float(adx_indicator.adx_pos().iloc[-1]),
            'ndi': float(adx_indicator.adx_neg().iloc[-1])
        }
        return (Indicator.ADX, adx_values)

    def STOCH(self, k_period: int = 14, d_period: int = 3, smooth_k: int = 3) -> Tuple[Indicator, dict]:
        """
        Calculate Stochastic Oscillator
        Returns:
            Tuple[Indicator, dict]: A tuple containing the indicator type and a dictionary with Stochastic values
        """
        high_prices = self._get_price_column('High')
        low_prices = self._get_price_column('Low')
        close_prices = self._get_price_column('Close')

        stoch_indicator = StochasticOscillator(
            high=high_prices,
            low=low_prices,
            close=close_prices,
            window=k_period,
            smooth_window=smooth_k
        )

        stoch_values = {
            '%K': float(stoch_indicator.stoch().iloc[-1]),
            '%D': float(stoch_indicator.stoch_signal().iloc[-1])
        }
        return (Indicator.STOCH, stoch_values)

    def OBV(self) -> Tuple[Indicator, float]:
        """
        Calculate On Balance Volume (OBV)
        Returns:
            Tuple[Indicator, float]: A tuple containing the indicator type and the calculated OBV value
        """
        close_prices = self._get_price_column('Close')
        volume = self._get_price_column('Volume')

        obv_indicator = OnBalanceVolumeIndicator(close=close_prices, volume=volume)
        val = float(obv_indicator.on_balance_volume().iloc[-1])
        return (Indicator.OBV, val)

    def VPT(self) -> Tuple[Indicator, float]:
        """
        Calculate Volume Price Trend (VPT)
        Returns:
            Tuple[Indicator, float]: A tuple containing the indicator type and the calculated VPT value
        """
        close_prices = self._get_price_column('Close')
        volume = self._get_price_column('Volume')

        vpt_indicator = VolumePriceTrendIndicator(close=close_prices, volume=volume)
        val = float(vpt_indicator.volume_price_trend().iloc[-1])
        return (Indicator.VPT, val)
