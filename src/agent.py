from combiner import Combiner
from data import DataHandler
from datetime import date

class Agent:
    def __init__(self, ticker: str, start_date: date, end_date: date) -> None:
        self.ticker: str = ticker
        self.start_date: date = start_date
        self.end_date: date = end_date
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
        pass

    def start(self):
        while True:
            if self.running:
                self.run()

    def run(self):
        while self.running:
            pass
