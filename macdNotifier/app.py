import yfinance as yf
import pandas as pd
import numpy as np
import time

# Source: https://medium.com/codex/algorithmic-trading-with-macd-in-python-1c2769a6ad1b

def get_macd(price, slow, fast, smooth):
    exp1 = price.ewm(span = fast, adjust = False).mean()
    exp2 = price.ewm(span = slow, adjust = False).mean()
    macd = pd.DataFrame(exp1 - exp2).rename(columns = {'Close':'macd'})
    signal = pd.DataFrame(macd.ewm(span = smooth, adjust = False).mean()).rename(columns = {'macd':'signal'})
    hist = pd.DataFrame(macd['macd'] - signal['signal']).rename(columns = {0:'hist'})
    frames =  [macd, signal, hist]
    df = pd.concat(frames, join = 'inner', axis = 1)
    return df

def implement_macd_strategy(prices, data):    
    buy_price = []
    sell_price = []
    macd_signal = []
    signal = 0

    for i in range(len(data)):
        if data['macd'][i] > data['signal'][i]:
            if signal != 1:
                buy_price.append(prices[i])
                sell_price.append(np.nan)
                signal = 1
                macd_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                macd_signal.append(0)
        elif data['macd'][i] < data['signal'][i]:
            if signal != -1:
                buy_price.append(np.nan)
                sell_price.append(prices[i])
                signal = -1
                macd_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                macd_signal.append(0)
        else:
            buy_price.append(np.nan)
            sell_price.append(np.nan)
            macd_signal.append(0)
            
    return buy_price, sell_price, macd_signal

def checkTick(tick):
    googl = yf.download(tickers=tick, period="1d", interval="1m", progress=False)
    googl_macd = get_macd(googl['Close'], 26, 12, 9)
    googl_macd.tail()
    buy_price, sell_price, macd_signal = implement_macd_strategy(googl['Close'], googl_macd)
    return macd_signal[-1]!=0

if __name__ == "__main__":
    # Put your tickers that you want into the array
    tickers = ["AMD", "SPY", "PLAY","DKS","TLT","TGT","RDBX","WMT","ETSY","PYPL"]

    while True:
        for i in tickers:
            print(i + " has been checked!")
            if checkTick(i):
                print(i + " has crossed, time: " + time.ctime())
        time.sleep(60)