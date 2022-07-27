import os,time
try:
    import ta
except:
    os.system("pip install ta")
try:
    import pandas as pd
except:
    os.system("pip install pandas")
try:
    import chime
except:
    os.system("pip install chime")
import numpy as np

from ta.trend import EMAIndicator

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
pd.options.mode.chained_assignment = None

###########################################
csvName = "BTCUSDT1h.csv"
fee = 0.04
emaFast = 2
emaFastMax = 150
emaSlow = 3
emaSlowMax = 250
bestResult = [0,0,0] # money, emaFast, emaSlow
###########################################

attributes = ["timestamp","open","high","low","close","volume","1","2","3","4","5","6"]
df = pd.read_csv(csvName, names = attributes)

loop = True
while loop:

    totalMoney = 1000
    inLongPosition = False
    longEnterPrice = 0
    longExitPrice = 0


    print("indikatörler hesaplanıyor")

    if emaFastMax == emaFast:
        emaFast = 2

    ema = EMAIndicator(df["close"],emaFast)
    df["emaFast"] = ema.ema_indicator()
    ema = EMAIndicator(df["close"],emaSlow)
    df["emaSlow"] = ema.ema_indicator()

    if emaFast + 1 == emaSlow:
        emaSlow = emaSlow + 1
        emaFast = 3
    else:
        emaFast = emaFast + 1

    for i in range(df.shape[0]):
        print(str(len(df.index)) + "/" + str(i) , " Doing backtest... Total Usdt: ", round(totalMoney,2),"|| Best Result:", bestResult,"|| EmaFast:",emaFast, "|| EmaSlow:", emaSlow)
        if i>emaSlow:
            # long enter
            if inLongPosition == False and df['emaFast'][i-2] < df['emaSlow'][i-2] and df['emaFast'][i-1] > df['emaSlow'][i-1]:
                longEnterPrice = float(df['open'][i])
                totalMoney = totalMoney - ((totalMoney / 100) * fee)
                likitPrice = longEnterPrice - (longEnterPrice / 100) * 100
                inLongPosition = True

            # long exit
            if inLongPosition and df['emaFast'][i-2] > df['emaSlow'][i-2] and df['emaFast'][i-1] < df['emaSlow'][i-1]:
                longExitPrice = df["open"][i]
                totalMoney = totalMoney + ((totalMoney / 100) * ((longExitPrice - longEnterPrice) / longEnterPrice) * 100)
                totalMoney = totalMoney - ((totalMoney / 100) * fee)
                inLongPosition = False

            # long likit olma
            if inLongPosition and float(df["low"][i]) < likitPrice:
                totalMoney = 0


    if totalMoney > bestResult[0]:
        bestResult[0] = round(totalMoney,2)
        bestResult[1] = emaFast
        bestResult[2] = emaSlow

    if emaSlow == emaSlowMax and emaFast == emaFastMax:
        loop = False

print("En iyi sonuç:", bestResult)
chime.success()