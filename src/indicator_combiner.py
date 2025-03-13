from typing import Tuple, Dict
from structs import Indicator, Signal
from indicators import Indicators

weights = {
    Indicator.RSI: 1.0,
}

class IndicatorCombiner:
    def __init__(self, weights = weights) -> None:
        self.weights: Dict[Indicator, float] = weights

    def __call__(self, *args: Tuple[Indicator, float]) -> Signal:

        return Signal.BUY

if __name__ == "__main__":
    combiner = IndicatorCombiner()
    indicators = Indicators()

    final_signal = combiner(*indicators.list_all_tuples())
