from typing import Tuple, Dict
from structs import Indicator
from indicators import Indicators

weights = {
    Indicator.RSI: 1.0,
}

class IndicatorCombiner:
    def __init__(self, weights = weights) -> None:
        self.weights: Dict[Indicator, float] = weights

    def __call__(self, data) -> float:
        self.indicators = Indicators(data)
        return self.indicators.RSI()
