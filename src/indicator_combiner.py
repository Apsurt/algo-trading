from typing import Tuple
from structs import Indicator, Signal

weights = {
    Indicator.RSI: 1,
}

class IndicatorCombiner:
    def __init__(self, weights = weights) -> None:
        self.weights = weights

    def __call__(self, *args: Tuple[Indicator, float]) -> Signal:

        return Signal.BUY

if __name__ == "__main__":
    combiner = IndicatorCombiner()
    indicator_list = [(Indicator.RSI, 0.0)]

    final_signal = combiner(*indicator_list)
