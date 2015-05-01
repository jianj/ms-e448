'''
This is for running in Quantopian, running time is long
'''

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
randn = np.random.randn

constituents = local_csv('spConstituents.csv')
tickerSymbols = constituents.Symbol
tickerSymbols = tickerSymbols[(tickerSymbols!='BRK-B') & 
                                  (tickerSymbols!='CMCSA') & 
                                  (tickerSymbols!='DISCA') & 
                                  (tickerSymbols!='NU') & 
                                  (tickerSymbols!='BF-B') & 
                                  (tickerSymbols!='WAG')]
tickerSymbols = pandas.Series(tickerSymbols.values)

openClose = get_pricing(tickerSymbols, fields=['open_price', 'close_price'],
                          start_date='2004-01-01', end_date='2015-04-27')

openClose = openClose.transpose(2, 1, 0)

prices = {}
for ts in tickerSymbols:
    prices[ts] = openClose[symbols(ts)]
    
for ts in tickerSymbols:
    tsPrice = prices[ts]
    prev_close = pandas.Series(tsPrice.close_price[:-1].values, tsPrice.close_price.index[1:])
    
    prices[ts]['overnight'] = (tsPrice.open_price - prev_close) / prev_close
    prices[ts]['intraDaily'] = (tsPrice.close_price - tsPrice.open_price) / tsPrice.open_price
    prices[ts]['sameDirection'] = prices[ts].overnight * prices[ts].intraDaily > 0
    prices[ts]['existed'] = pandas.notnull(prices[ts].overnight)

'''
Below is for frequences chart

nDays = len(prices['AAPL'])
span = 251 #251
start = 0
while start < nDays:
    freq = []
    end = (start + span) if start + span < nDays else nDays
    for ts in tickerSymbols:
        frequences = sum(prices[ts].sameDirection[start:end])
        nTradingDays = sum(prices[ts].existed[start:end])
        if nTradingDays == 0:
            freq.append(0)
        else:
            freq.append(frequences * 1.0 / nTradingDays - 0.5)

    fig, ax = plt.subplots()
    ind = np.arange(len(tickerSymbols))
    rect1 = ax.bar(ind, np.array(freq), 0.35)
    start = end
    
'''

nDays = len(prices['AAPL'])
span = 251
nYears = nDays / span + 1
corrMat = []

for i in xrange(nYears):
    corrMat.append({})
    for ts in tickerSymbols:
        corrMat[i][ts] = prices[ts].overnight[span * i: span * (i + 1)].corr(prices[ts].intraDaily[span * i:span * (i + 1)])
        
    ind = np.arange(len(tickerSymbols))
    corrs = np.array(corrMat[i].values())
    
    fig, ax = plt.subplots()
    rect = ax.bar(ind, corrs, 0.35)
    
    plt.title('S&P constituents\' correlation between overnight and intradaily in ' + str(2004 + i))
    plt.xlabel('S&P constituents')
    plt.ylabel('Correlation')
