import yfinance as yf
import pandas as pd
from typing import Dict, Optional

class DataHandler:
    def __init__(self, ticker: str, start: str, end: str, interval: str = '1d'):
        self.ticker = ticker
        self.start = start
        self.end = end
        self.interval = interval
        self.data = None

    def update_ticker(self, new_ticker: str) -> None:
        old_ticker = self.ticker
        self.ticker = new_ticker
        try:
            self.test()
        except ValueError as e:
            self.ticker = old_ticker
            raise e

    def fetch_data(self) -> pd.DataFrame:
        self.data = yf.download(
            self.ticker,
            start=self.start,
            end=self.end,
            interval=self.interval,
            auto_adjust=False,
            progress=False
        )
        self._clean_data()
        if self.data is None:
            raise ValueError("Data is None.")
        return self.data

    def _clean_data(self) -> None:
        if self.data is None:
            raise ValueError("Data is None.")
        self.data.dropna(inplace=True)
        self.data['Returns'] = self.data['Close'].pct_change()

    def test(self) -> None:
        self.data = yf.download(
            self.ticker,
            start=self.start,
            end=self.end,
            auto_adjust=False,
            progress=False
        )

if __name__ == "__main__":
    data_handler = DataHandler('AAPL', '2020-01-01', '2023-01-01')
    data_handler.test()
    data = data_handler.fetch_data()
    print(data)
