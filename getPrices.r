library(zoo)
library(tseries)

rm(list=ls())
###GET HISTORICAL OPEN AND CLOSE PRICES
###Read in quandl file with current S&P constituents https://www.quandl.com/resources/useful-lists
spMemb = read.csv("H:/32BitFiles/Admin/Class/MSE448/SP500Constituents.csv")

###Set start and end dates for data pull
dateStart="2013-12-31"
dateEnd="2014-12-31"

tkrs=spMemb[,1]
nMemb=length(tkrs)

###read in first set of historical close prices
closeP=get.hist.quote(instrument=tkrs[1], start=dateStart, end =dateEnd, quote="Close",retclass="zoo", quiet=TRUE)
dimnames(closeP)[[2]]=as.character(tkrs[1])

###attempt to read in data for all other tickers. Catch exceptions and merge new data if successful
###close price does not adjust for divs and splits. AdjClose does but there is not an equivalent AdjOpen.  Probably get around this eventually by using quantopian data
for(i in 2:nMemb){
	cat("downloading ", i," of ", nMemb, "\n")
	
	result <- try(temp <- get.hist.quote(instrument = tkrs[i], start = dateStart, end = dateEnd, quote = "Close", retclass = "zoo", quiet = T))
	#result=try(temp=get.hist.quote(instrument=tkrs[i], start=dateStart, end =dateEnd, quote="AdjClose",retclass="zoo", quiet=TRUE))
	if(class(result) == "try-error"){
		#print(tkrs[i])
		next
	}
	else{
		dimnames(temp)[[2]]=as.character(tkrs[i])
		closeP=merge(closeP,temp)
	}
}

###read in first set of historical open prices. Should at some point go back and resolve adjclose / open issue
openP=get.hist.quote(instrument=tkrs[1], start=dateStart, end =dateEnd, quote="Open",retclass="zoo", quiet=TRUE)
dimnames(openP)[[2]]=as.character(tkrs[1])

###attempt to read in data for all other tickers. Catch exceptions and merge new data if successful
for(i in 2:nMemb){
	cat("downloading ", i," of open", nMemb, "\n")
	
	result <- try(temp <- get.hist.quote(instrument = tkrs[i], start = dateStart, end = dateEnd, quote = "Open", retclass = "zoo", quiet = T))
	if(class(result) == "try-error"){
		#print(tkrs[i])
		next
	}
	else{
		dimnames(temp)[[2]]=as.character(tkrs[i])
		openP=merge(openP,temp)
	}
}

###CREATE RELEVANT RETURN SERIES
###intra day returns
intraR=closeP/openP-1
intraRC=intraR[,!is.na(colSums(intraR))]
###overnight returns
overnightR=openP/lag(closeP,-1)-1
overnightRC=overnightR[,!is.na(colSums(overnightR))]

days=dim(intraR)[1]
myCorrs=array()
for(i in 1:(length(dimnames(intraRC)[[2]]))){
	myCorrs[i]=cor(intraRC[(1:(days-1)),i],overnightRC[,i])
}

###plot correlations
hist(myCorrs,xlab="Observed Overnight/Intraday Correlation")
###results here are not encouraging there does not seem to be any abnormal tendancy to mean reversion.  Just as many positive correlations as negative correlations

###try looking at correlations by decile of overnight return as suggested by the model

lagOvernightRC=lag(overnightRC,-1)
intradayMeans=array()
for (i in 1:10){
	intradayMeans[i]=mean(as.matrix(intraRC)[(overnightRC>=quantile(overnightRC,(i-1)/10))&(overnightRC<quantile(overnightRC,i/10))])
}
plot(intradayMeans,xlab="Decile")
	
