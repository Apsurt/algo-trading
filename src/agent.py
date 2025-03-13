from combiner import Combiner
from data import DataHandler
from datetime import date, timedelta

class Agent:
    def __init__(self, ticker: str,) -> None:
        self.ticker: str = ticker
        self.end_date: date = date.today()
        self.start_date: date = self.end_date - timedelta(1.0)
        self.interval: str = "1d"

        self.data_handler: DataHandler = DataHandler(
            ticker,
            self.start_date.strftime("%Y-%m-%d"),
            self.end_date.strftime("%Y-%m-%d"),
            self.interval
        )

        self.combiner: Combiner = Combiner()

        self.running: bool = True

    def update_ticker(self, new_ticker: str) -> None:
        self.data_handler.update_ticker(new_ticker)
        self.ticker = new_ticker

    def start(self):
        while True:
            if self.running:
                self.run()

    def run(self):
        while self.running:
            pass
