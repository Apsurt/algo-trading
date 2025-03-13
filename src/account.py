from typing import List

class Order:
    def __init__(self) -> None:
        pass

class Position:
    def __init__(self, ticker: str) -> None:
        pass

class Account:
    def __init__(self) -> None:
        self.cash: float = 0.0
        self.positions: List[Position] = []
        self.pending_orders: List[Order] = []
        self.order_history: List[Order] = []
