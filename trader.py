import config #imports python script with username and password
#kept in separate script for security reasons
import trade_strat

import robin_stocks.robinhood as rh
import datetime as dt
import time
#import pandas as pd

def login(days):
    time_logged_in = 60*60*24*days #60 secs * 60 mins * 24 hours * number of days logged in
    #days logged in is set to 1 day, show in "__main__" code
    rh.authentication.login(username=config.USERNAME, 
                            password=config.PASSWORD, 
                            expiresIn=time_logged_in, 
                            scope='internal', 
                            by_sms=True,
                            store_session=True)

def logout():
    rh.authentication.logout()

def get_stocks():
    stocks = list()
    #Program will only run with selected stocks. Will NOT touch the stocks owned if not listed here
    stocks.append("WBD")
    stocks.append("PARA")
    #stocks.append("KO")
    return(stocks)

def open_market():
    market = False #market is presumed to be closed
    #market = True #market is always open, only used for testing purposes
    time_now = dt.datetime.now().time() #now implies that the time is set to the current time
    
    market_open = dt.time(9,30,0) #market opens at 9:30AM
    market_close = dt.time(15,59,0) # market closes at 3:59PM
    
    if time_now > market_open and time_now < market_close:
        market = True #implies market is opened
        #print('market is open :)')
    else:
        print('market is closed :(')
        #pass #only used for testing purposes
        #pass is used sincemarket will always be open, no need for a statement saying its closed
    return(market)

def get_cash():
    rh_cash = rh.account.build_user_profile()
    #print("rh cash: ", rh_cash)
    
    cash = float(rh_cash['cash'])
    equity = float(rh_cash['equity'])
    return(cash, equity)

def get_holdings_and_bought_price(stocks):
    holdings = {stocks[i]: 0 for i in range(0, len(stocks))}
    bought_price = {stocks[i]: 0 for i in range(0, len(stocks))}
    rh_holdings = rh.account.build_holdings()
    
    for stock in stocks:
        try:
            holdings[stock] = int(float((rh_holdings[stock]['quantity'])))
            bought_price[stock] = float((rh_holdings[stock]['average_buy_price']))
        except:
            holdings[stock] = 0
            bought_price[stock] = 0
            
    return(holdings, bought_price)

def sell(stock, holdings, price):
    sell_price = round((price-0.10), 2) 
    #the 10 cents account for the price moving down
    '''
    sell_order = rh.orders.order_sell_limit(symbol=stock,
                                            quantitiy=holdings,
                                            limitPrice=sell_price,
                                            timeInForce='gfd')
    '''
    #gfd - good for a day (basically, keep order until all shares are sold)
    print('### Tring to SELL {} at ${}'.format(stock,price))
    
def buy(stock, allowable_holdings):
    buy_price = round((price+0.10), 2) 
    #the 10 cents account for the price moving up
    '''
    buy_order = rh.orders.order_buy_limit(symbol=stock,
                                            quantitiy=allowable_holdings,
                                            limitPrice=buy_price,
                                            timeInForce='gfd')
    '''
    print('### Tring to BUY {} at ${}'.format(stock,price))
    
if __name__ == "__main__": 
    login(days=1)
    
    stocks = get_stocks()
    print('stocks: ', stocks)
    
    cash, equity = get_cash()
    #equity doesn't match the equity present in my account
    
    ts = trade_strat.trader(stocks)
    
    while open_market():
        prices = rh.stocks.get_latest_price(stocks)
        holdings, bought_price = get_holdings_and_bought_price(stocks)
        print('holdings:' , holdings)
        # holdings is accurrate, however it doesn't account for partial shares which is lame
        

        for i, stock in enumerate(stocks): #enumerate takes a list and counts as it goes through the list
            price = float(prices[i])
            print('{} = ${}'.format(stock, price))
            
            trade = ts.trade_option(stock, price)
            print('trade:', trade)
            
            if trade == "BUY":
                allowable_holdings = int((cash/10)/price)
                # with code below, will ONLY buy if there are 0 shares owned
                if allowable_holdings > 5 and holdings[stock] == 0: 
                    buy(stock, allowable_holdings)
            elif trade == "SELL":
                if holdings[stock] > 0:
                    sell(stock, holdings[stock], price)
            '''
            df_prices = ts.get_historical_prices(stock, span='day')
            sma=ts.get_sma(stock, df_prices, window=12)
            p_sma = ts.get_price_sma(price, sma)
            print('sma: ', sma)
            print('p_sma: ', p_sma)
            '''
        time.sleep(30) #30 second interval between each time something is printed
        #everything within this function will print over and over again unless this is in place
        
    logout()


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
