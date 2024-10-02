import uuid
import datetime
import Position
from typing import List
from enum import Enum
from enum import auto


class PositionHandlerLogicBean:
    openPositions: List[Position]
    closedPositions: List[Position]
    buySignals: any
    sellSignals: any
    balance: float
    ticker: str

    def __init__(self, buySignals, sellSignals, ticker: str):
        self.buySignals = buySignals
        self.sellSignals = sellSignals
        self.balance = 0.0
        self.ticker = ticker
    
    def simulateOnOldData(self):
        for i,bs in self.buySignals:
            self.openPositions.append(Position(bs.value[i], self.ticker, "LONG", date= bs.index[i]))
        print(self.openPositions)




class Position:
    #This represence a Position on the market
    openPrice: float = 0
    closePrice: float = 0
    id: str
    date: datetime
    ticker: str
    positionType: str

    def __init__(self, openPrice: float, ticker: str, positionType:str, id: str = uuid.uuid1(), date: datetime = datetime.datetime.now()):
        self.openPrice = openPrice
        self.id = id
        self.date = date
        self.ticker = ticker
        self.positionType = positionType
    
    def closePosition(self, closePrice: float) -> float:
        self.closePrice = closePrice
        if(self.positionType == "LONG"):
            return self.openPrice - self.closePrice
        return  self.closePrice - self.openPrice
    