#!/usr/bin/python
import btceapi
from collections import deque
import csv
import time
import pickle

def mean(x):
    return sum(x)/len(x)

class trades:
    def __init__(self,coin,updated,server_time,ask_prices,ask_volumes,bid_prices,bid_volumes,buy,sell):
        self.coin=coin
        self.updated=updated
        self.server_time=server_time
        self.time=time.strftime('%X')
        self.date=time.strftime('%x')
        self.time_object = time.localtime()
        
        self.ask_prices = ask_prices
        self.ask_volumes = ask_volumes
        self.bid_pries = bid_prices
        self.bid_volumes = bid_volumes
        
        self.buy = buy
        self.sell = sell
        

def main():
    attrs = ('high', 'low', 'avg', 'vol', 'vol_cur', 'last',
             'buy', 'sell', 'updated', 'server_time')
    
    #initialize connection
    connection = btceapi.BTCEConnection()
    
    f = open('/media/Big Daddy/New_Documents/python_data/btc_usd_depth.pkl', 'ab')     
    while 1:
       
        #sleep for .5 seconds, i.e. collect at 2Hz
        time.sleep(1)
    
        try:
            #get ticker
            ticker = btceapi.getTicker("btc_usd", connection)
            #get asks/bids
            asks, bids = btceapi.getDepth("btc_usd")
            ask_prices, ask_volumes = zip(*asks)
            bid_prices, bid_volumes = zip(*bids)
        
            #start list with all of the ticker info
            curTrades = trades(coin='ltc',updated=ticker.updated,server_time=ticker.server_time,ask_prices=ask_prices,ask_volumes=ask_volumes,bid_prices=bid_prices,bid_volumes=bid_volumes,buy=ticker.buy,sell=ticker.sell)
            #print out_list
            #now we have a huge list with all the info, write to a single line in the csv file
            
            # Pickle class using protocol 0.
            pickle.dump(curTrades,f)    
        
            #if connection is lost, just try to reconnect (this does seem to happen, so this line is actually pretty important for long data collects)
        except:
            connection = btceapi.BTCEConnection()
            pass
    
if __name__ == '__main__':
    main()