import pandas as pd
import numpy as np
from indicator_combiner import IndicatorCombiner

class Combiner:
    def __init__(self) -> None:
        # Indicators
        self.indicator_combiner = IndicatorCombiner()

        # Chart Patterns
        # ML
        # ML Sentiment

    def __call__(self, data: pd.DataFrame) -> float:
        return float(np.mean([
            self.indicator_combiner(data),
        ]))
