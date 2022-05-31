def vwap(df):
    q = df.Volume
    p = df.Close
    return df.assign(vwap=(p * q).cumsum() / q.cumsum())

def ema13(df):
    # df['ema13'] = df.Close.ewm(span=13, adjust=False).mean()
    return df.Close.ewm(span=13, adjust=False).mean()

import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
tsla = yf.download("TSLA", period="1d", interval="1m", progress=False)
tsla["ema13"] = ema13(tsla)
tsla = vwap(tsla)
print(tsla)
# ema = ema13(tsla)
# vw = vwap(tsla)

tsla['position'] = tsla["ema13"] > tsla["vwap"]
tsla['pre_position'] = tsla['position'].shift(1)
tsla.dropna(inplace=True)
tsla['crossover'] = np.where(tsla['position'] == tsla['pre_position'], False, True)


fig = plt.figure()
ax1 = fig.add_subplot()
ax1.plot(tsla["ema13"])
ax1.plot(tsla["vwap"])
ax1.plot(tsla.loc[tsla["crossover"]]["vwap"], "*")
# plt.show()
import time
print(tsla.loc[tsla["crossover"]]["vwap"].index)
print(tsla.index.get_loc(tsla.loc[tsla["crossover"]]["vwap"].index[0]))