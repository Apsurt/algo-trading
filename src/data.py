import yfinance as yf
import pandas as pd
from typing import Dict, Optional

class DataHandler:
    """Handles data retrieval and preprocessing"""
    def __init__(self, ticker: str, start: str, end: str, interval: str = '1d'):
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
        if self.data is None:
            raise ValueError("Data is None.")
        self.data.dropna(inplace=True)
        self.data['Returns'] = self.data['Close'].pct_change()

if __name__ == "__main__":
    data_handler = DataHandler('AAPL', '2020-01-01', '2023-01-01')
    data = data_handler.fetch_data()
    print(data)
