import yfinance as yf
import numpy as np
import pandas as pd
from typing import Dict, Optional

class DataHandler:
    """Handles data retrieval and preprocessing"""
    def __init__(self, ticker: str, start: str, end: str, interval: str = '2m'):
        self.ticker = ticker
        self.start = start
        self.end = end
        self.interval = interval
        self.data = None

    def fetch_data(self):
        """Fetch historical data with explicit auto_adjust=False"""
        self.data = yf.download(
            self.ticker,
            start=self.start,
            end=self.end,
            interval=self.interval,
            auto_adjust=False
        )
        self._clean_data()
        return self.data

    def _clean_data(self):
        """Clean and preprocess data"""
        self.data.dropna(inplace=True)
        self.data['Returns'] = self.data['Close'].pct_change()


class IndicatorCalculator:
    """Calculates technical indicators"""

    @staticmethod
    def sma(series: pd.Series, window: int) -> pd.Series:
        return series.rolling(window).mean()

    @staticmethod
    def ema(series: pd.Series, window: int) -> pd.Series:
        return series.ewm(span=window, adjust=False).mean()

    @staticmethod
    def rsi(series: pd.Series, window: int = 14) -> pd.Series:
        delta = series.diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)

        avg_gain = gain.rolling(window).mean()
        avg_loss = loss.rolling(window).mean()

        rs = avg_gain / avg_loss
        return 100 - (100 / (1 + rs))

    @staticmethod
    def macd(series: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> pd.DataFrame:
        """Modified MACD calculation with explicit index handling"""
        fast_ema = series.ewm(span=fast, adjust=False).mean()
        slow_ema = series.ewm(span=slow, adjust=False).mean()
        macd_line = fast_ema - slow_ema
        signal_line = macd_line.ewm(span=signal, adjust=False).mean()

        # Ensure we return DataFrame with proper index
        return pd.DataFrame({
            'MACD': macd_line,
            'Signal': signal_line
        }, index=series.index)

    @staticmethod
    def bollinger_bands(series: pd.Series, window: int = 20, num_std: int = 2):
        sma = series.rolling(window).mean()
        std = series.rolling(window).std()
        upper = sma + (std * num_std)
        lower = sma - (std * num_std)
        return pd.DataFrame({'Upper': upper, 'Lower': lower})

    @staticmethod
    def stochastic_oscillator(df: pd.DataFrame, window: int = 14, k_window: int = 3):
        low_min = df['Low'].rolling(window).min()
        high_max = df['High'].rolling(window).max()
        k = 100 * ((df['Close'] - low_min) / (high_max - low_min))
        d = k.rolling(k_window).mean()
        return pd.DataFrame({'%K': k, '%D': d})


class TradingStrategy:
    """Implements trading strategy using multiple indicators"""
    def __init__(self, data: pd.DataFrame):
        self.data = data
        self.signals = pd.DataFrame(index=data.index)

    def generate_signals(self):
        """Generate trading signals based on multiple indicators"""
        # Calculate indicators
        self.data['SMA_50'] = IndicatorCalculator.sma(self.data['Close'], 50)
        self.data['SMA_200'] = IndicatorCalculator.sma(self.data['Close'], 200)
        self.data['RSI'] = IndicatorCalculator.rsi(self.data['Close'])
        macd = IndicatorCalculator.macd(self.data['Close'])
        self.data = pd.concat([self.data, macd], axis=1)

        # Generate signals
        self.signals['price_relation'] = np.where(
            self.data['SMA_50'] > self.data['SMA_200'], 1, -1)
        self.signals['rsi_overbought'] = np.where(self.data['RSI'] > 70, -1, 0)
        self.signals['rsi_oversold'] = np.where(self.data['RSI'] < 30, 1, 0)
        self.signals['macd_crossover'] = np.where(
            self.data['MACD'] > self.data['Signal'], 1, -1)

        # Combine signals
        self.signals['total_signal'] = (
            self.signals['price_relation'] +
            self.signals['rsi_overbought'] +
            self.signals['rsi_oversold'] +
            self.signals['macd_crossover']
        )

        # Final decision
        self.signals['position'] = np.where(
            self.signals['total_signal'] > 2, 1,
            np.where(self.signals['total_signal'] < -2, -1, 0))

        return self.signals


class RiskManager:
    """Manages position sizing and risk"""
    def __init__(self, capital: float, risk_per_trade: float = 0.01):
        self.capital = capital
        self.risk_per_trade = risk_per_trade

    def calculate_position_size(self, entry_price: float, stop_loss: float) -> float:
        """Calculate position size based on risk parameters"""
        risk_amount = self.capital * self.risk_per_trade
        price_risk = abs(entry_price - stop_loss)
        return risk_amount / price_risk if price_risk != 0 else 0


class Portfolio:
    """Tracks portfolio state"""
    def __init__(self, initial_capital: float):
        self.initial_capital = initial_capital
        self.current_balance = initial_capital
        self.positions = 0
        self.position_value = 0
        self.total_value = []

    def update_portfolio(self, price: float, position: int, position_size: float):
        """Update portfolio based on new position"""
        if position == 1:  # Buy
            investment = self.current_balance * position_size
            self.positions += investment / price
            self.current_balance -= investment
        elif position == -1:  # Sell
            self.current_balance += self.positions * price
            self.positions = 0
        self.position_value = self.positions * price
        self.total_value.append(self.current_balance + self.position_value)


class Backtester:
    """Backtesting engine"""
    def __init__(self, data: pd.DataFrame, initial_capital: float = 100000):
        self.data = data
        self.initial_capital = initial_capital
        self.portfolio = Portfolio(initial_capital)
        self.risk_manager = RiskManager(initial_capital)

    def run_backtest(self, signals: pd.Series):
        """Run backtest on historical data"""
        for i in range(len(self.data)):
            current_price = self.data.iloc[i]['Close']
            signal = signals.iloc[i]

            # Simple position sizing - risk 1% per trade
            position_size = 0.01  # Can be enhanced with stop-loss calculation

            if signal != 0:
                self.portfolio.update_portfolio(
                    price=current_price,
                    position=signal,
                    position_size=position_size
                )
            else:
                # Update portfolio value even when not trading
                self.portfolio.total_value.append(
                    self.portfolio.current_balance +
                    self.portfolio.position_value
                )

        return self.portfolio.total_value


# Example Usage
if __name__ == "__main__":
    # Data Retrieval
    data_handler = DataHandler('AAPL', '2025-02-01', '2025-03-12')
    data = data_handler.fetch_data()

    # Generate Signals
    strategy = TradingStrategy(data)
    signals = strategy.generate_signals()

    # Backtest Strategy
    backtester = Backtester(data)
    portfolio_values = backtester.run_backtest(signals['position'])

    # Show Results
    print(f"Initial Capital: ${backtester.initial_capital:,.2f}")
    print(f"Final Portfolio Value: ${portfolio_values[-1]:,.2f}")
    print(f"Return: {(portfolio_values[-1]/backtester.initial_capital-1)*100:.2f}%")
