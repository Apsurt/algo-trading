from combiner import Combiner
from data import DataHandler
from datetime import date, timedelta

class Agent:
    def __init__(self, ticker: str,) -> None:
        self.ticker: str = ticker
        self.end_date: date = date.today()
        self.start_date: date = self.end_date - timedelta(1.0)
        self.interval: str = "1m"

        self.data_handler: DataHandler = DataHandler()
        self.data_handler.add_ticker(self.ticker)

        self.combiner: Combiner = Combiner()

        self.running: bool = True

    def start(self):
        while True:
            if self.running:
                self.run()

    def run(self):
        while self.running:
            data = self.data_handler.fetch_data()
            signal = self.combiner(data)
            print(signal)
