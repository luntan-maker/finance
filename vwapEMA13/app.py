import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
import time
import termcolor

def vwap(df):
    q = df.Volume
    p = df.Close
    return df.assign(vwap=(p * q).cumsum() / q.cumsum())

def ema13(df):
    # df['ema13'] = df.Close.ewm(span=13, adjust=False).mean()
    return df.Close.ewm(span=13, adjust=False).mean()

def checkCrossover(tick):
    tsla = yf.download(tick, period="1d", interval="1m", progress=False)
    tsla["ema13"] = ema13(tsla)
    tsla = vwap(tsla)
    # print(tsla)
    # ema = ema13(tsla)
    # vw = vwap(tsla)

    tsla['position'] = tsla["ema13"] > tsla["vwap"]
    tsla['pre_position'] = tsla['position'].shift(1)
    tsla.dropna(inplace=True)
    tsla['crossover'] = np.where(tsla['position'] == tsla['pre_position'], False, True)


    # fig = plt.figure()
    # ax1 = fig.add_subplot()
    # ax1.plot(tsla["ema13"])
    # ax1.plot(tsla["vwap"])
    # ax1.plot(tsla.loc[tsla["crossover"]]["vwap"], "*")
    # plt.show()
    
    # print(tsla.loc[tsla["crossover"]]["vwap"].index)
    # print(tsla.index.get_loc(tsla.loc[tsla["crossover"]]["vwap"].index[0]))
    return tsla.index.get_loc(tsla.loc[tsla["crossover"]]["vwap"].index[0])

if __name__ == "__main__":
    # Put your tickers that you want into the array
    tickers = ["AMD", "SPY", "PLAY","DKS","TLT","TGT","RDBX","WMT","ETSY","PYPL"]

    while True:
        for i in tickers:
            print(i + " has been checked!")
            res = checkCrossover(i)
            if res ==  0:
                print(termcolor.colored(i + " has crossed, time: " + time.ctime(), "red"))
        time.sleep(60)