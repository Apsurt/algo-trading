from calendar import c
import yfinance as yf
import pandas as pd
from typing import List
from datetime import timedelta
from time import time

class DataHandler:
    def __init__(self):
        self.tickers: List[str] = []
        
        self.rate_limit: int = 2000
        self.requests = 0
        self.period = timedelta(hours=1)
        self.last_request = 0
        
        self.data = None

    def add_ticker(self, ticker: str) -> None:
        self.tickers.append(ticker)
    
    def remove_ticker(self, ticker: str) -> None:
        self.tickers.remove(ticker)
    
    def can_request(self) -> bool:
        s_per_req = (self.period.total_seconds() / self.rate_limit)*3
        return time() - self.last_request > s_per_req

    def fetch_data(self) -> pd.DataFrame:
        if self.tickers is None:
            raise ValueError("No tickers")
        
        if not self.can_request():
            if self.data is None:
                raise ValueError("Can't request and data is None")
            return self.data
        
        self.last_request = time()
        self.data = yf.download(
            self.tickers,
            interval = "1m",
            period = "1d",
            auto_adjust=False,
            progress=False,
            prepost=True
        )
        if self.data is None:
            raise ValueError("Data is None.")
        self.data = self.data.sort_values("Datetime")
        return self.data

if __name__ == "__main__":
    data_handler = DataHandler()
    data_handler.add_ticker("AAPL")
    data_handler.add_ticker("NVDA")
    data_handler.add_ticker("RHM.DE")
    while True:
        out = False
        if data_handler.can_request():
            out = True
        data = data_handler.fetch_data()
        if out:
            print(data)
            out = False
