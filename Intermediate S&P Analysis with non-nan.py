
# coding: utf-8

# In[6]:

import numpy as np
import pandas
import matplotlib.pyplot as plt
from sklearn import linear_model
randn = np.random.randn


# In[14]:

def MultivariateLinearRegression(X, y):
    nVariable = len(X)
    nPeriod = len(y)
    intercept = [1] * nPeriod
    X.insert(0, intercept)
    transposedX = zip(*X)
    clf = linear_model.LinearRegression()
    clf.fit(transposedX, y)
    coef = clf.coef_
    print "The intercept is " + str(coef[0])
    for i in range(nVariable):
        print "The coefficient of variable #" + str(i + 1) + " is: " + str(coef[i + 1])
    return coef


# In[2]:

constituents = local_csv('constituents.csv')
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


# In[ ]:




# In[42]:

prices = {}

for ts in tickerSymbols:
    tsPrice = openClose[symbols(ts)].dropna()
    prev_close = pandas.Series(tsPrice.close_price[:-1].values, tsPrice.close_price.index[1:])
    prices[ts] = pandas.DataFrame(tsPrice)
    prices[ts]['overnight'] = (tsPrice.open_price - prev_close) / prev_close
    prices[ts]['intradaily'] = (tsPrice.close_price - tsPrice.open_price) / tsPrice.open_price
    prices[ts] = prices[ts].dropna()


# In[ ]:




# In[48]:

nDays = len(prices['AAPL'])
span = 251
nYears = nDays / span + 1

regEndDay = nDays
regStartDay = regEndDay - span

regList = tickerSymbols

vec = [[],[],[],[]]

for ts in regList:
    if regEndDay > len(prices[ts]):
        continue
        
    X = [prices[ts].overnight[regStartDay:regEndDay], prices[ts].intraDaily[regStartDay - 1: regEndDay - 1], prices[ts].overnight[regStartDay - 1:regEndDay - 1]]
    y = prices[ts].intraDaily[regStartDay:regEndDay]
    print ts + ' result:'
    var = MultivariateLinearRegression(X, y)
    for i in xrange(4):
        vec[i].append(var[i])
        
    print


# In[52]:

for i in xrange(4):
    plt.bar(range(len(vec[i])), vec[i])
    plt.show()


# In[ ]:



