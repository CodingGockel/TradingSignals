import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import ta
import time
from Position import PositionHandlerLogicBean

ticker = 'NVDA'
interval = '1h'  # 1-Minuten-Intervall für Echtzeitdaten
balance = 0
def get_live_data(ticker, period='1mo', interval='1h'):
    return yf.download(ticker, period=period, interval=interval)

def plot_live(i):
    # Daten abrufen (z.B. für den letzten Tag mit einem 1-Minuten-Intervall)
    data = get_live_data(ticker, period='1mo', interval=interval)
    data['SMA50'] = data['Close'].rolling(window=50).mean()
    data['SMA200'] = data['Close'].rolling(window=200).mean()
    data['RSI'] = ta.momentum.RSIIndicator(data['Close']).rsi()

    # Lösche das vorherige Diagramm
    plt.cla()

    # Zeichne den Aktienkurs
    plt.plot(data.index, data['Close'], label='Close Price', alpha=0.75)
    plt.plot(data.index, data['SMA50'], label='SMA50', alpha=0.75)
    plt.plot(data.index, data['SMA200'], label='SMA200', alpha=0.75)

    # Signale berechnen und zeichnen
    buy_signals = data[data['RSI'] < 30]['Close']
    sell_signals = data[data['RSI'] > 70]['Close']

    # Kaufsignale anzeigen
    plt.scatter(buy_signals.index, buy_signals, marker='^', color='g', label='Buy Signal', alpha=1)
    # Verkaufssignale anzeigen
    plt.scatter(sell_signals.index, sell_signals, marker='v', color='r', label='Sell Signal', alpha=1)

    # Labels und Legende hinzufügen
    plt.title(f'Live-Daten: {ticker}')
    plt.xlabel('Zeit')
    plt.ylabel('Preis')
    plt.legend()

fig = plt.figure(figsize=(14, 7))
ani = FuncAnimation(plt.gcf(), plot_live, interval=60000)  # Aktualisiere alle 60 Sekunden

plt.show()
