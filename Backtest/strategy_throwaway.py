import pandas as pd
import math

from yfinance import ticker
from prices import data
from datetime import datetime


'''Trader creates a trading object which can buy and sell stocks.
It tracks the price at which the stock was purchased, and the price
at which it was sold. It initiates an account starting value. It keeps track
of wins and losses. '''

class Trader():
    prices = []
    initial_cash = 0
    cash = 100000
    stock_buys = []
    #stock_buys[] --> 0 = stock, 1 = shares, 2 = price, 3 = timestamp, 4 = transaction
    current_holding = []
    stock_sells = []
    #stock_sells[] --> 0 = stock, 1 = shares, 2 = price, 3 = timestamp, 4 = transaction
    timestamps = []
    sell_timestamps = []
    buy_timestamps = []
    last_transaction = ''
    ticker_stocks = []
    wins = 0
    loss = 0

    def __init__(self,  stocks, cash=100000):
        self.tracker = 0
        self.buy_tracker = 0
        self.sell_tracker = 0
        self.cash = cash
        Trader.cash = cash
        Trader.initial_cash = cash
        self.stocks = stocks
        Trader.ticker_stocks = [stock for stock in self.stocks]
        #while self.tracker < len(data)-1:
        #    self.strategy(stock)

    @classmethod
    def history(self):
        b_table = pd.DataFrame(Trader.stock_buys, columns=['STOCK', 'SHARES', 'PRICE', 'TIME'])
        s_table = pd.DataFrame(Trader.stock_sells, columns=['STOCK', 'SHARES', 'PRICE', 'TIME'])
        keys = ['BUYS', 'SELLS']
        result = pd.concat([b_table, s_table], axis=1, keys=keys)
        pd.set_option('colheader_justify', 'center')
        now = datetime.now()
        now = now.strftime('%m_%d_%Y_%H_%M_%S')
        result.to_csv(f'\\trades\\trading_history_{now}.csv')
        print(result)

    @staticmethod
    def run(self):
        while self.tracker < len(data):
            self.strategy(self.stocks)
            self.tracker += 1
            
        
        
        
        last_tran = Trader.last_transaction.lower()
        if Trader.last_transaction == 'BUY':
            entry_price = Trader.current_holding[-1][2]
            shares = Trader.current_holding[-1][1]
            self.cash += shares * entry_price
        profit_perc = (self.cash - Trader.initial_cash) / Trader.initial_cash * 100
        profit = self.cash - Trader.initial_cash
        win_rate = Trader.wins / (Trader.wins + Trader.loss) * 100
        if Trader.last_transaction == 'BUY':
            holding_ticker = Trader.current_holding[-1][0]
            holding_shares = Trader.current_holding[-1][1]
            bought_price = Trader.current_holding[-1][2]
            holding_price = data[holding_ticker]['Open'][self.tracker - 1]
            hold_diff = (holding_price - bought_price) / bought_price * 100
            self.summary = f'\n\n\nYou have ${self.cash:,.2f} value in your account.\nThat is a %{profit_perc:.2f} change from your initial account value, or ${profit:,.2f}.\nYour current position is a {last_tran} of {holding_shares} {holding_ticker} shares at a price of ${bought_price:,.2f}.\nYou are currently holding it at a price of ${holding_price:,.2f}, which is a difference of %{hold_diff:.2f}.\nYou made {self.buy_tracker} buys and {self.sell_tracker} sells.\nYour win rate is %{win_rate:.2f}.'
        elif Trader.last_transaction == 'SELL':
            self.summary = f'\n\n\nYou have ${self.cash:,.2f} value in your account.\nThat is a %{profit_perc:.2f} change from your initial account value, or ${profit:,.2f}.\nYour current position is a {last_tran}.\nYou made {self.buy_tracker} buys and {self.sell_tracker} sells.\nYour win rate is %{win_rate:.2f}.'
        print(self.summary)


    def buy(self, stock, strategy='All In'):
        cash = self.cash
        self.current_price = data[stock]['Close'][self.tracker]
        if strategy == 'All In':
            shares = math.floor(cash / self.current_price)
        self.buy_timestamps.append((data['Datetime'][self.tracker]).strftime('%B %d, %Y at %r'))
        if shares != 0:
            self.buy_tracker += 1
            Trader.stock_buys.append([stock, shares, self.current_price, self.buy_timestamps[self.buy_tracker - 1]])
            Trader.current_holding.clear()
            Trader.current_holding.append([stock, shares, self.current_price,data['Datetime'][self.tracker].strftime('%B %d, %Y at %r')])
            self.cash -= self.current_price * shares
            result = f'''You bought {Trader.stock_buys[self.buy_tracker - 1][1]} shares of {Trader.stock_buys[self.buy_tracker - 1][0]} at ${self.current_price:,.2f} on {self.buy_timestamps[self.buy_tracker - 1]}\nYou have ${self.cash:,.2f} remaining in your account balance'''
            print(result)
            Trader.last_transaction = 'BUY'
        if shares == 0:
            #reject = 'Your order was rejected for {}\nYou have ${:,.2f} still in your account balance'.format(stock,self.cash)
            #result = reject
            pass
        
        return -1

    def strategy(self, stocks):
        potential_buys = []
        if len(potential_buys) >= 1:
            prices = pd.DataFrame(list(zip([potential_buy for potential_buy in potential_buys],
                                            [data[potential_buy]['Close'][self.tracker] for potential_buy in potential_buys])),
                                            columns=['SYMBOL', 'PRICE'])
            prices.sort_values(by=['PRICE'], ascending=True)
            final_decision = prices.iloc[0]['SYMBOL']
            self.buy(final_decision)
        potential_buys.clear()        
        if len(Trader.current_holding) == 1 and (data['Datetime'][self.tracker]).strftime('%B %d, %Y at %r') != self.buy_timestamps[self.buy_tracker - 1]:
            holding_stock_price = Trader.current_holding[-1][2]
            holding_ticker = Trader.current_holding[-1][0]
            if data[holding_ticker]['Open'][self.tracker - 1] >= 1.001 * holding_stock_price:
                self.sell()

        for stock in stocks:
            c_open = data[stock]['Open'][self.tracker]
            #c_high = data[stock]['High'][self.tracker]
            #c_low = data[stock]['Low'][self.tracker]
            c_close = data[stock]['Close'][self.tracker]
            #c_diff = c_close - c_open
            #c_range = c_high - c_low
            self.current_price = c_open
            if self.tracker >= 2:
                p_open = data[stock]['Open'][self.tracker - 1]
                p_high = data[stock]['High'][self.tracker - 1]
                p_low = data[stock]['Low'][self.tracker - 1]
                p_close = data[stock]['Close'][self.tracker - 1]
                #p_diff = p_close - p_open
                p_range = p_high - p_low
                p_range = p_range

                pp_open = data[stock]['Open'][self.tracker - 2]
                pp_high = data[stock]['High'][self.tracker - 2]
                pp_low = data[stock]['Low'][self.tracker - 2]
                pp_close = data[stock]['Close'][self.tracker - 2]
                #p_diff = p_close - p_open
                pp_range = pp_high - pp_low
                pp_range = pp_range


                if p_close > p_open and pp_close <= pp_open and len(Trader.current_holding) < 1:
                    potential_buys.append(stock)
                else:
                    current_time = (data['Datetime'][self.tracker]).strftime('%B %d, %Y at %r')
                    print(f'{current_time} {stock} Close: ${c_close:,.2f}')



            
        

    def sell(self, strategy='All Out'):
        self.sell_timestamps.append((data['Datetime'][self.tracker]).strftime('%B %d, %Y at %r'))
        #self.tracker += 1
        if strategy == 'All Out':
            if len(Trader.current_holding) == 1:
                shares = Trader.current_holding[-1][1]
                stock = Trader.current_holding[-1][0]
                current_open = data[stock]['Open'][self.tracker]
                self.cash += shares * current_open
                Trader.current_holding.clear()
                self.sell_tracker += 1
                Trader.stock_sells.append([stock, shares, current_open, self.sell_timestamps[self.sell_tracker - 1]])
                if Trader.stock_sells[-1][2] > Trader.stock_buys[-1][2]:
                    Trader.wins += 1
                elif Trader.stock_sells[-1][2] <= Trader.stock_buys[-1][2]:
                    Trader.loss += 1
                result = f'''You sold {Trader.stock_sells[self.sell_tracker - 1][1]} shares of {Trader.stock_sells[self.sell_tracker - 1][0]} at ${current_open:,.2f} on {self.sell_timestamps[self.sell_tracker - 1]}\nYou have ${self.cash:,.2f} remaining in your account balance.'''
                print(result)
                Trader.last_transaction = 'SELL'

        return -1