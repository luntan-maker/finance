import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
import time
import termcolor
import os
os.system('color')

def vwap(df):
    q = df.Volume
    p = df.Close
    return df.assign(vwap=(p * q).cumsum() / q.cumsum())

def ema13(df):
    return df.Close.ewm(span=13, adjust=False).mean()

def checkCrossover(tick):
    tsla = yf.download(tick, period="1d", interval="1m", progress=False)
    tsla["ema13"] = ema13(tsla)
    tsla = vwap(tsla)
    

    tsla['position'] = tsla["ema13"] > tsla["vwap"]
    tsla['pre_position'] = tsla['position'].shift(1)
    tsla.dropna(inplace=True)
    tsla['crossover'] = np.where(tsla['position'] == tsla['pre_position'], False, True)
    # print(tsla['crossover']==True)
    # print(tsla['crossover'])
    return np.where(tsla['crossover']==True), len(tsla['crossover'])


if __name__ == "__main__":
    # Put your tickers that you want into the array
    tickers = ["AMD", "SPY", "PLAY","DKS","TLT","TGT","RDBX","WMT","ETSY","PYPL"]

    while True:
        for i in tickers:
            res, size = checkCrossover(i)
            print(i + " has been checked!")
            # print(res)
            # print(size)
            if len(res[0]) > 0:
                if res[0][-1] == size-1:
                    print(termcolor.colored(i + " has been crossed at time: "+ time.ctime(), "yellow"))
        time.sleep(60)