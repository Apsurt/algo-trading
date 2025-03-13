# abc
import pandas as pd
import numpy as np
from structs import Indicator
from typing import Tuple


class Indicators:
    def __init__(self, data: pd.DataFrame ) -> None:
        self.data = data
        pass

    def SMA(self) -> Tuple[Indicator, float]:
        """
        Calculate Simple Moving Average (SMA)

        Returns:
            Tuple[Indicator, float]: A tuple containing the indicator type and the calculated SMA value
        """
        prices = self.data['Close']

        self.period = len(prices)

        val = float(np.mean(prices))

        return (Indicator.SMA, val)


    def list_all_tuples():
        return
