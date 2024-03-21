import pandas as pd

import robin_stocks.robinhood as rh

#sma - simple movie average

class trader():
    def __init__(self, stocks): #self references within the same class
        self.stocks = stocks
        
        self.sma_hour = {stocks[i]: 0 for i in range(0, len(stocks))}
        self.run_time = 0
        
        self.buffer = 0.005 #0.5% buffer
   
        self.price_sma_hour = {stocks[i]: 0 for i in range(0, len(stocks))}

    def get_historical_prices(self, stock, span):
        '''
        !!!!
        based on the dataframe, the historical data prices seems to be updated every
        five minutes over the course of a 24 hour period, with the most current price being
        two multiples of 5 (minutes) beforehand. This is a really bad explanation.
        (for example, since I find this hard to explain, if the time is 22:33PM, 
         then the price will be taken from 22:25PM). The time zone is in UTC.
        
        I am assuming this means, the interval of time is based on the span_interval
        'day': '5minutes' and it sets to this automatically.
        
        I will physically have to changes what the interval and span is equal to
        within the historical_data variable if I would like the data to be
        within a larger time frame.
        
        Idk if this makes sense and im not exacty sure how to do that
        at this very moment, but I will play around with it later.
        !!!!
        '''
        span_interval = {'day': '5minute', 'week': '10minute', 'month': 'hour', '3month': 'hour', 'year': 'day', '5year': 'week'}
        interval = span_interval[span]
  
        historical_data = rh.stocks.get_stock_historicals(stock, interval=interval, span=span, bounds='extended')
        
        #the following is the section of code not needed from
        #this section is out dated and will cause a 404 error when the code is ran.
        #this is noted so I am aware of what sections of code to avoid when creating the trading bot.
     
        #symbols=help.inputs_to_set(stock)
        #...
        #historical_data.append(subitem)


        df = pd.DataFrame(historical_data)
        #df columns seems to have changed from tutorial
        #df columns not shown(presumed in ...) high_price and low_price
        #volume was replaced with symbol   

        dates_times = pd.to_datetime(df.loc[:, 'begins_at'])
        close_prices = df.loc[:, 'close_price'].astype('float')
        
        df_price = pd.concat([close_prices, dates_times], axis=1)
        df_price = df_price.rename(columns={'close_price': stock})
        df_price = df_price.set_index('begins_at')
        #removes most columns from original data fram
        #only keeps two columns: the date and the price of the stock
        #prices of the stock is what builds the sma
        
        return(df_price)
        
        #print('data: \n', df) #prints out the historical df set of the listed stocks 
        #print('data: \n', df_price) #prints same df with only two columns
        
    '''
    sma is the simple moving average
    calculated by adding the closing price of a stock or other security over a 
    specific period of time and dividing the total by the appropriate number of 
    trading days
    ex. a 20-day SMA is the average closing price over the previous 20 days
    '''
    def get_sma(self, stock, df_prices, window=12): 
        '''
        window will display the x most recent stock prices
        
        since the window is set to 12, it will show the 12 most recent prices
        '''
        sma = df_prices.rolling(window=window, min_periods=window).mean()
        '''
        calculates the mean for the past x (12) prices, going to be a moivng 
        average every time it updates
        '''
        sma = round(float(sma[stock].iloc[-1]), 4)
        return(sma)
        '''
        sma explained!
        sell when sma > price
        buy when sma < price
        hold when sma = price
        *note*
        i am going to add a buffer in somewhere to avoid selling/buying IMMEDIATWELY
        during a small/insignificant price change.
        '''
        
    def get_price_sma(self, price, sma):
        price_sma = round(price/sma, 4)
        return(price_sma)
        '''
        p_sma is the ratio of the price/sma
        similar mindset to sma
        sell when p_sma > 1
        buy when p_sma < 1
        hold when p_sma = 1
        '''
    
    def trade_option(self, stock, price):
        # gets new sma_hour every 5min
        if self.run_time % (5) == 0:
            df_historical_prices = self.get_historical_prices(stock, span = 'day')
            self.sma_hour[stock] = self.get_sma(stock, df_historical_prices[-12:], window=12)
      
        self.price_sma_hour[stock] = self.get_price_sma(price, self.sma_hour[stock])
        p_sma = self.price_sma_hour[stock]   
       
        i1 = 'BUY' if self.price_sma_hour[stock]<(1.0-self.buffer) else "SELL" if self.price_sma_hour[stock]>(1.0+self.buffer) else "NONE"
        if i1 == "BUY":
            trade = "BUY"
        elif i1 == "SELL":
            trade = "SELL"
        else:
            trade = "HOLD"
            
        return(trade)
      

