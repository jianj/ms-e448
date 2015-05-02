
# coding: utf-8

# In[90]:

'''
This is for running in Quantopian, running time is long
'''

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


# In[ ]:




# In[18]:

clearCorrMat = []
for i in xrange(nYears):
    clearCorrMat.append(pandas.DataFrame(corrMat[i].items()).dropna())


# In[33]:

orderedCorrMat = []
for i in xrange(nYears):
    yearCorr = [tuple(x) for x in clearCorrMat[i].values]
    yearCorr = sorted(yearCorr, key = lambda tup: tup[1])
    orderedCorrMat.append(yearCorr)


# In[62]:

[len(x) for x in orderedCorrMat]


# In[63]:

topNegN = 200
topPosN = 200
trainingYears = 8
topNegCorrSet = set([tup[0] for tup in orderedCorrMat[0][:topNegN + 1]])
topPosCorrSet = set([tup[0] for tup in orderedCorrMat[0][-topPosN:]])
for i in xrange(1, trainingYears + 1):
    candidateNegSet = set([tup[0] for tup in orderedCorrMat[i][:topNegN + 1]])
    candidatePosSet = set([tup[0] for tup in orderedCorrMat[i][-topPosN:]])
    topNegCorrSet &= candidateNegSet
    topPosCorrSet &= candidatePosSet


# In[53]:

topNegCorrSet


# In[80]:

overnights = []
intradaily = []
for ts in tickerSymbols:
    overnights += list(prices[ts].overnight)
    intradaily += list(prices[ts].intraDaily)
print len(overnights), len(intradaily)


# In[88]:

plt.scatter(overnights[:10000], intradaily[:10000], alpha=0.3)
plt.show()


# In[89]:

orderedCorrMat[0]


# In[95]:

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


# In[ ]:




# In[ ]:




# In[ ]:




# In[109]:

cleanPrices = {}
for ts in tickerSymbols:
    cleanPrices[ts] = openClose[symbols(ts)]


# In[ ]:




# In[106]:


    
for ts in tickerSymbols:
    tsPrice = cleanPrices[ts].dropna()
    prev_close = pandas.Series(tsPrice.close_price[:-1].values, tsPrice.close_price.index[1:])
    
    cleanPrices[ts]['overnight'] = (tsPrice.open_price - prev_close) / prev_close
    cleanPrices[ts]['intraDaily'] = (tsPrice.close_price - tsPrice.open_price) / tsPrice.open_price


# In[107]:

regStartDay = 6 * span
regEndDay = regStartDay + 2 * span + 1
regList = tickerSymbols

for ts in regList:
    X = [cleanPrices[ts].overnight[regStartDay:regEndDay], cleanPrices[ts].intraDaily[regStartDay - 1: regEndDay - 1], cleanPrices[ts].overnight[regStartDay - 1:regEndDay - 1]]
    y = cleanPrices[ts].intraDaily[regStartDay:regEndDay]
    print ts + ' result:'
    print MultivariateLinearRegression(X, y)
    print


# In[108]:

cleanPrices['ABBV']


# In[ ]:



