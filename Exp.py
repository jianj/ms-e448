
# coding: utf-8

# In[4]:

import numpy as np
from sklearn import linear_model

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

x1 = np.random.random(10)
x2 = np.random.random(10)
x3 = np.random.random(10)
X = [x1, x2, x3]
y = np.random.random(10)
coef = MultivariateLinearRegression(X, y)
    


# In[2]:

import pandas
tickerSymbols = pandas.Series(['SPY'])
spy = get_pricing(tickerSymbols, fields=['open_price', 'close_price'],
                          start_date='2004-01-01', end_date='2015-04-27')
spy = spy.transpose(2, 1, 0)
spy


# In[3]:

prices = {}
prices = spy[symbols('SPY')]
prev_close = pandas.Series(prices.close_price[:-1].values, prices.close_price.index[1:])

prices['overnight'] = (prices.open_price - prev_close) / prev_close
prices['intraDaily'] = (prices.close_price - prices.open_price) / prices.open_price
prices['sameDirection'] = (prices.overnight * prices.intraDaily > 0)
prices.dropna(how = 'any')
prices


# In[ ]:



