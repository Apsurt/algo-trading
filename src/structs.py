from enum import Enum

class Signal(Enum):
    BUY = 0
    SELL = 1

class Indicator(Enum):
    SMA = 0
    EMA = 1
    MACD = 2
    RSI = 3
    BBANDS = 4
    ATR = 5
    ADX = 6
    STOCH = 7
    OBV = 8
    VPT = 9
    # etc...
