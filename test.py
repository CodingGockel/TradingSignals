import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import ta
import time
from Position import PositionHandlerLogicBean

ticker = 'AAPL'
interval = '1h'  # 1-Minuten-Intervall für Echtzeitdaten
leverage = 30
balance = 0
fees = 1
entry = 100
def get_live_data(ticker, period='1mo', interval='1h'):
    return yf.download(ticker, period=period, interval=interval)

# Daten abrufen (z.B. für den letzten Tag mit einem 1-Minuten-Intervall)
data = get_live_data(ticker, period='1mo', interval=interval)
data['SMA50'] = data['Close'].rolling(window=50).mean()
data['SMA200'] = data['Close'].rolling(window=200).mean()
data['RSI'] = ta.momentum.RSIIndicator(data['Close']).rsi()

buy_signals = data[data['RSI'] < 30]['Close']
sell_signals = data[data['RSI'] > 70]['Close']

openPositions = []
allSignals = []

for index, value in buy_signals.items():
    allSignals.append((index,value, "BUY"))

for index, value in sell_signals.items():
    allSignals.append((index,value, "SELL"))

allSignals = sorted(allSignals, key=lambda x: x[0])
for i in allSignals:
    print(i)
def getLongProfits():
    index = 0
    balance = 0
    for value in allSignals:
        if(value[2] == "SELL" and index > 0):
            sell_price = value[1]
            for i in range(index-1, -1, -1):
                if(allSignals[i][2] == "SELL"):
                    break
                buy_price = allSignals[i][1]
                increase = ((sell_price-buy_price) / buy_price) * leverage
                balance = balance + ((increase * entry) - (fees*2))
                print(f'Gekauft: {buy_price} \t verkauft: {sell_price} \t gewinn: {((increase * entry) - (fees*2))}')
        index+=1
    return balance
def getShortProfits():
    index = 0
    balance = 0
    for value in allSignals:
        if(value[2] == "BUY" and index > 0):
            sell_price = value[1]
            for i in range(index-1, -1, -1):
                if(allSignals[i][2] == "BUY"):
                    break
                buy_price = allSignals[i][1]
                increase = ((sell_price-buy_price) / buy_price) * leverage
                balance = balance + ((increase * entry) - (fees*2))
                print(f'Gekauft: {buy_price} \t verkauft: {sell_price} \t gewinn: {((increase * entry) - (fees*2))}')
        index+=1
    return balance
balance+=getLongProfits()
balance+=getShortProfits()
print(balance)

#print(allSignals)
