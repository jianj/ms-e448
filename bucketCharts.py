
# coding: utf-8

# In[4]:

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# In[5]:

constituents = local_csv('spConstituents.csv')
tickerSymbols = constituents.Symbol
tickerSymbols = tickerSymbols[(tickerSymbols!='BRK-B') & 
                                  (tickerSymbols!='CMCSA') & 
                                  (tickerSymbols!='DISCA') & 
                                  (tickerSymbols!='NU') & 
                                  (tickerSymbols!='BF-B') & 
                                  (tickerSymbols!='WAG')]
tickerSymbols = pd.Series(tickerSymbols.values)


openClose = get_pricing(tickerSymbols, fields=['open_price', 'close_price'],
                          start_date='2004-01-01', end_date='2015-04-27')

openClose = openClose.transpose(2, 1, 0)


# In[9]:

prices = {}
for ts in tickerSymbols:
    prices[ts] = openClose[symbols(ts)]
    
for ts in tickerSymbols:
    tsPrice = prices[ts]
    prev_close = pd.Series(tsPrice.close_price[:-1].values, tsPrice.close_price.index[1:])
    prices[ts]['overnight'] = (tsPrice.open_price - prev_close) / prev_close
    prices[ts]['intraDaily'] = (tsPrice.close_price - tsPrice.open_price) / tsPrice.open_price


# In[39]:

nDays = len(prices['AAPL'])
overnights = []
for i in xrange(nDays):
    overnights.append([])
    for ts in tickerSymbols:
        overnights[i].append((ts, np.nan_to_num(prices[ts].overnight[i]), np.nan_to_num(prices[ts].intraDaily[i])))
    
    overnights[i] = sorted(overnights[i], key=lambda tup:tup[1])


# In[69]:

def getDecile(overnight, bucketSize):
    n = len(overnight) / bucketSize + 1
    decile = [0] * n
    
    for i in xrange(n):
        end = min((i + 1) * bucketSize, len(overnight))
        for j in xrange(i * bucketSize, end):
            decile[i] += overnight[j][2]
            
        decile[i] = decile[i] / (end - i * bucketSize)
    
    return decile

def plotBucketCharts(sumDeciles, year):
    plt.bar(range(1, len(sumDeciles) + 1), sumDeciles, alpha = 0.35)
    plt.title("Relationship between S&P 500 overnight return and intraDaily return for  " + 
             ("2004-2015" if year < 0 else str(2004 + year)))
    plt.xlabel("Overnight return from low to high in deciles")
    plt.ylabel("Average intraDaily return")
    plt.show()
    
def averaged(vec, n):
    for i in xrange(len(vec)):
        vec[i] /= n * 1.0


# In[70]:

deciles = []
bucketSize = 50
nBuckets = len(tickerSymbols) / bucketSize + 1
sumDeciles = [0] * nBuckets
span = 251
sumDecileSpan = [0] * nBuckets

for i in xrange(nDays):
    deciles.append(list(getDecile(overnights[i], bucketSize)))
    for j in xrange(nBuckets):
        sumDecileSpan[j] += deciles[i][j]
        sumDeciles[j] += deciles[i][j]
        
    if (i + 1) % span == 0:
        averaged(sumDecileSpan, span)
        plotBucketCharts(sumDecileSpan, i / span)
        sumDecileSpan = [0] * nBuckets

averaged(sumDecileSpan, nDays % span)
plotBucketCharts(sumDecileSpan, nDays / span)
        
averaged(sumDeciles, nDays)
plotBucketCharts(sumDeciles, -1)


# In[ ]:



