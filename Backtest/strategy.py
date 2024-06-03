from numpy.core.numeric import NaN
import pandas as pd
import math
import shutil
import os

import candlesticks
from yfinance import ticker
from prices import interval,ticker_list, retrieve_prices
import prices as pc
from datetime import datetime
import numpy as np


nw = datetime.now()
nw_date = nw.strftime('%Y-%m-%d')
std_date = '2019-01-01'

data = retrieve_prices(std_date, nw_date)
print(data)



#Must change between 'Date' and 'Datetime'
if interval == '1h' or interval == '1d':
    nomenclature_for_datetime = 'Date'
else:
    nomenclature_for_datetime = 'Datetime'



class Trader():
    '''Trader creates a trading object which can buy and sell stocks.
    It tracks the price at which the stock was purchased, and the price
    at which it was sold. It initiates an account starting value. It keeps track
    of wins and losses. '''
    
    #Strategy Specifications
    exit_max_time = 1 ##
    exit_max_loss = 1 ##
    exit_win = 1 ##
    hist_data = [] ##
    annual_return = [] ##
    tickers_traded = [] ##
    prices = [] ##
    initial_cash = 0
    cash = 100000
    
    non_rep_tickers = [] ##
    #stock, current_open, shares, price_diff, price_diff_perc
    ticker_sales = [] ##
    stock_buys = [] ##
    #stock_buys[] --> 0 = stock, 1 = shares, 2 = price, 3 = timestamp, 4 = transaction
    current_holding = [] ##
    stock_sells = [] ##
    #stock_sells[] --> 0 = stock, 1 = shares, 2 = price, 3 = timestamp, 4 = transaction
    timestamps = [] ##
    sell_timestamps = [] ##
    buy_timestamps = [] ##
    last_transaction = '' ##
    ticker_stocks = [] ##
    wins = 0 ##
    loss = 0 ##
    strats = [] ##

    def __init__(self,  stocks, exit_max_time, exit_max_loss, exit_win,strategy_name, cash=10000):
        """Initiate trading account.
                cash = int 
                    (default = 10000),

                stocks = list of tickers strings 
                    (use ticker_list to pull from prices.py),

                strategy_name = string with strategy names separated with periods 
                    (example = 'Golden Cross. Shooting Star'),

                exit_win = float -> when the stock reaches x% higher, sell for profit 
                    (example = 1.001 -> Exit at 0.1% profit),

                exit_max_loss = float -> when the stock reaches x% lower, sell to cut losses 
                    (example = 0.999 -> Exit at 0.1% loss),

                exit_max_time = int -> max amount of time before selling no matter what 
                    (days, hours, or minutes, depending on interval in prices.py)
        """
        #RESET TRADER VARS
        Trader.tickers_traded = []
        Trader.annual_return = []
        Trader.timestamps = []
        Trader.sell_timestamps = []
        Trader.buy_timestamps = []
        Trader.last_transaction = ''
        Trader.ticker_stocks = []
        Trader.wins = 0
        Trader.loss = 0
        Trader.strats = []
        Trader.prices = []
        Trader.non_rep_tickers = []
        Trader.ticker_sales = []
        Trader.stock_buys = []
        Trader.current_holding = []
        Trader.stock_sells = []
        Trader.hist_data = []



        self.strategy_name = strategy_name
        self.tracker = 0
        self.buy_tracker = 0
        self.sell_tracker = 0
        self.cash = cash
        split_strategies = strategy_name.split('.')
        split_strategies = [x.strip() for x in split_strategies]
        Trader.strats = split_strategies
        #print(Trader.strats)
        Trader.cash = cash
        Trader.initial_cash = cash
        Trader.exit_max_loss = exit_max_loss
        Trader.exit_max_time = exit_max_time
        Trader.exit_win = exit_win
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
        
        filename = f'trading_history_{now}.csv'
        result.to_csv(filename)
        try:
            shutil.move(('D:/Desktop Backup/School/Homework/Statistics/Python Stuff/Backtest/' + filename), 'D:/Desktop Backup/School/Homework/Statistics/Python Stuff/Backtest/Trade Sessions')
        except:
            print('Cannot move, file exists in Trade Sessions folder.')
            pass
        #print(result)

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
        # day_count = data[nomenclature_for_datetime][len(data)-1] - data[nomenclature_for_datetime][0]
        day_count = self.tracker
        # yearly_growth = (((self.cash-Trader.initial_cash)/((self.cash-Trader.initial_cash)/2))/(day_count/253))*100
        yearly_growth = np.mean(Trader.annual_return)
        if Trader.last_transaction == 'BUY':
            holding_ticker = Trader.current_holding[-1][0]
            holding_shares = Trader.current_holding[-1][1]
            bought_price = Trader.current_holding[-1][2]
            holding_price = data[holding_ticker]['Open'][self.tracker - 1]
            hold_diff = (holding_price - bought_price) / bought_price * 100
            self.summary = f'\n\n\nYou have ${self.cash:,.2f} value in your account.\nThat is a {profit_perc:.2f}% change from your initial account value, or ${profit:,.2f}.\nYour current position is a {last_tran} of {holding_shares} {holding_ticker} shares at a price of ${bought_price:,.2f}.\nYou are currently holding it at a price of ${holding_price:,.2f}, which is a difference of {hold_diff:.2f}%.\nYou made {self.buy_tracker} buys and {self.sell_tracker} sells.\nYour win rate is {win_rate:.2f}%.\nYou have been trading for {day_count} days.\nYour yearly growth is {yearly_growth:.2f}%.'
        elif Trader.last_transaction == 'SELL':
            self.summary = f'\n\n\nYou have ${self.cash:,.2f} value in your account.\nThat is a {profit_perc:.2f}% change from your initial account value, or ${profit:,.2f}.\nYour current position is a {last_tran}.\nYou made {self.buy_tracker} buys and {self.sell_tracker} sells.\nYour win rate is %{win_rate:.2f}.\nYou have been trading for {day_count} days.\nYour yearly growth is {yearly_growth:.2f}%.'
        summary_table = pd.DataFrame()
        now_date = pd.to_datetime(data[nomenclature_for_datetime][len(data)-1])
        start_date = pd.to_datetime(data[nomenclature_for_datetime][0])
        summary_table['Tickers Traded'] = [trick[0] for trick in Trader.tickers_traded]
        summary_table['Shortlist'] = pd.Series([trick for trick in Trader.non_rep_tickers])
        summary_table['Entry Point Price'] = [trick[1] for trick in Trader.tickers_traded]
        summary_table['Exit Point Price'] = pd.Series([trick[1] for trick in Trader.ticker_sales])
        summary_table['Shares Traded'] = pd.Series([trick[2] for trick in Trader.ticker_sales])
        summary_table['Earnings ($)'] = pd.Series([trick[3] for trick in Trader.ticker_sales])
        summary_table['Earnings (%)'] = pd.Series([trick[4] for trick in Trader.ticker_sales])
        summary_table['Exit Strategy (Loss %)'] = pd.Series([100 * (1 - Trader.exit_max_loss)] * 1)
        summary_table['Exit Strategy (Win %)'] = pd.Series([100 * (Trader.exit_win - 1)] * 1)
        summary_table['Exit Strategy (Time)'] = pd.Series([Trader.exit_max_time] * 1)

        if 'Shooting Star' in Trader.strats:
            summary_table['Shooting Star'] = pd.Series(1)
        elif 'Shooting Star' not in Trader.strats:
            summary_table['Shooting Star'] = pd.Series(0)

        if 'Death Cross' in Trader.strats:
            summary_table['Death Cross'] = pd.Series(1)
        elif 'Death Cross' not in Trader.strats:
            summary_table['Death Cross'] = pd.Series(0)

        if 'Golden Cross' in Trader.strats:
            summary_table['Golden Cross'] = pd.Series(1)
        elif 'Golden Cross' not in Trader.strats:
            summary_table['Golden Cross'] = pd.Series(0)

        summary_table['Trading Period'] = pd.Series([day_count] * 1)
        summary_table['Trading Start Date'] = pd.Series([start_date] * 1)
        summary_table['Trading End Date'] = pd.Series([now_date] * 1)
        summary_table['Trading Intervals'] = pd.Series([interval] * 1)
        summary_table['Account Value'] = pd.Series([self.cash] * 1)
        summary_table['Number of Stocks Traded'] = pd.Series(self.sell_tracker)
        summary_table['Profit (%)'] = pd.Series(profit_perc)
        summary_table['Annual Return (%)'] = pd.Series(Trader.annual_return)
        summary_table['Mean Annual Return (%)'] = pd.Series(yearly_growth)
        summary_table['Profit ($)'] = pd.Series(profit)
        summary_table['Win Rate'] = pd.Series(win_rate)
        # summary_record = f'trading_summary_{strat_num}.csv'
        now_date = nw_date
        start_date = std_date
        #now_date = now_date.replace('-', '_')
        #start_date = start_date.replace('-', '_')
        stratnum_saver = f'trading_summary_win{Trader.exit_win}_loss_{Trader.exit_max_loss}_time_{Trader.exit_max_time}_period_{now_date}_{start_date}.txt'
        if os.path.exists(stratnum_saver):
            f = open(stratnum_saver, "r")
            strat_num = f.read()
            strat_num = int(strat_num)
            f.close()
            f = open(stratnum_saver, "w")
            suma = 1 + strat_num
            f.write(str(suma))
            f.close()
        elif os.path.exists(stratnum_saver) == False:
            print('Path doesn\'t exist')
            f = open(stratnum_saver, "w")
            strat_num = 1
            f.write(str(1))
            f.close()
        summary_record = f'trading_summary_win_{Trader.exit_win}_loss_{Trader.exit_max_loss}_time_{Trader.exit_max_time}_period_{now_date}_{start_date}_versi_{strat_num}.csv'
        cols = summary_table.columns.tolist()
        summary_table = summary_table[['Shortlist', 'Tickers Traded'] + cols[2:]]
        summary_table.to_csv(summary_record)
        # f = open(f'trading_summary_{strat_num}.csv', 'r')
        f = open(summary_record, 'r')
        text_csv = f.read()
        f.close()
        f = open(summary_record, 'w')
        f.write(f',,,,,,,,{self.strategy_name.title()} Strategy Results,,,,,,,,,,,\n'+text_csv)
        f.close()
        try:
            shutil.move(('D:/Desktop Backup/School/Homework/Statistics/Python Stuff/Backtest/' + summary_record), 'D:/Desktop Backup/School/Homework/Statistics/Python Stuff/Backtest/Results')
        except:
            print('Cannot move, file exists in Results folder.')
            pass
        print(self.summary)
        # summary_table.head()


    def buy(self, stock, strategy='All In'):
        shares = 0
        self.current_price = data[stock]['Close'][self.tracker]
        if strategy == 'All In':
            if math.isnan(self.current_price) == False and math.isnan(self.cash) == False:
                shares = math.floor(self.cash / self.current_price)
            else:
                pass
        self.buy_timestamps.append((data[nomenclature_for_datetime][self.tracker]).strftime('%B %d, %Y at %r'))
        if shares != 0:
            self.buy_tracker += 1
            Trader.stock_buys.append([stock, shares, self.current_price, self.buy_timestamps[self.buy_tracker - 1]])
            Trader.current_holding.clear()
            Trader.current_holding.append([stock, shares, self.current_price,data[nomenclature_for_datetime][self.tracker].strftime('%B %d, %Y at %r'), self.tracker])
            if stock not in Trader.tickers_traded:
                Trader.tickers_traded.append([stock, self.current_price, shares])
            if stock not in Trader.non_rep_tickers:
                Trader.non_rep_tickers.append(stock)
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
        if self.tracker % 253 == 0 and self.tracker != 0:
            current_value = self.cash
            if Trader.last_transaction == 'BUY':
                entry_price = Trader.current_holding[-1][2]
                shares = Trader.current_holding[-1][1]
                current_value += shares * entry_price
            percent_growth = (current_value - Trader.initial_cash) / Trader.initial_cash * 100
            Trader.annual_return.append(percent_growth)


        #When to sell
        if len(Trader.current_holding) == 1 and (data[nomenclature_for_datetime][self.tracker]).strftime('%B %d, %Y at %r') != self.buy_timestamps[self.buy_tracker - 1]:
            holding_stock_price = Trader.current_holding[-1][2]
            holding_ticker = Trader.current_holding[-1][0]
            holding_tracer = Trader.current_holding[-1][4]
            if data[holding_ticker]['Open'][self.tracker] >= Trader.exit_win * holding_stock_price or (data[holding_ticker]['Open'][self.tracker] >= Trader.exit_max_loss * holding_stock_price and data[holding_ticker]['Open'][self.tracker] <= holding_stock_price) or self.tracker > Trader.exit_max_time + holding_tracer:#or (data[holding_ticker]['Open'][self.tracker] >= holding_stock_price and candlesticks.death_cross(Trader.hist_data)):
                self.sell()
            else:
                return -1

        #Loop through real-time price data to determine when to buy or skip on an opening price
        for stock in stocks:
            c_open = data[stock]['Open'][self.tracker]
            #c_high = data[stock]['High'][self.tracker]
            #c_low = data[stock]['Low'][self.tracker]
            c_close = data[stock]['Close'][self.tracker]
            #c_diff = c_close - c_open
            #c_range = c_high - c_low
            self.current_price = c_open
            if self.tracker >= 3:
                p_open = data[stock]['Open'][self.tracker - 1]
                p_high = data[stock]['High'][self.tracker - 1]
                p_low = data[stock]['Low'][self.tracker - 1]
                p_close = data[stock]['Close'][self.tracker - 1]
                Trader.hist_data.append(p_close)
                p_day = [p_open, p_high, p_low, p_close]

                # pp_open = data[stock]['Open'][self.tracker - 2]
                # pp_high = data[stock]['High'][self.tracker - 2]
                # pp_low = data[stock]['Low'][self.tracker - 2]
                # pp_close = data[stock]['Close'][self.tracker - 2]
                # pp_day = [pp_open, pp_high, pp_low, pp_close]

                # ppp_open = data[stock]['Open'][self.tracker - 3]
                # ppp_high = data[stock]['High'][self.tracker - 3]
                # ppp_low = data[stock]['Low'][self.tracker - 3]
                # ppp_close = data[stock]['Close'][self.tracker - 3]
                # ppp_day = [ppp_open, ppp_high, ppp_low, ppp_close]


                #if p_close > p_open and pp_close <= pp_open and len(Trader.current_holding) < 1:
                if (candlesticks.golden_cross(Trader.hist_data) or candlesticks.shooting_star(p_day)) and len(Trader.current_holding) < 1:
                    self.buy(stock)
                    return -1
                else:
                    current_time = (data[nomenclature_for_datetime][self.tracker]).strftime('%B %d, %Y at %r')
                    print(f'{current_time} {stock} Close: ${c_close:,.2f}')
                    pass



            
        

    def sell(self, strategy='All Out'):
        self.sell_timestamps.append((data[nomenclature_for_datetime][self.tracker]).strftime('%B %d, %Y at %r'))
        #self.tracker += 1
        if strategy == 'All Out':
            if len(Trader.current_holding) == 1:
                shares = Trader.current_holding[-1][1]
                stock = Trader.current_holding[-1][0]
                buy_price = Trader.current_holding[-1][2]
                current_open = data[stock]['Open'][self.tracker]
                price_diff_perc = (current_open - buy_price) / buy_price * 100
                price_diff = current_open - buy_price
                self.cash += shares * current_open
                Trader.current_holding.clear()
                self.sell_tracker += 1
                Trader.stock_sells.append([stock, shares, current_open, self.sell_timestamps[self.sell_tracker - 1]])
                if stock not in Trader.tickers_traded:
                    Trader.ticker_sales.append([stock, current_open, shares, price_diff, price_diff_perc])
                if Trader.stock_sells[-1][2] > Trader.stock_buys[-1][2]:
                    Trader.wins += 1
                elif Trader.stock_sells[-1][2] <= Trader.stock_buys[-1][2]:
                    Trader.loss += 1
                result = f'''You sold {Trader.stock_sells[self.sell_tracker - 1][1]} shares of {Trader.stock_sells[self.sell_tracker - 1][0]} at ${current_open:,.2f} on {self.sell_timestamps[self.sell_tracker - 1]}\nYou have ${self.cash:,.2f} remaining in your account balance.'''
                print(result)
                Trader.last_transaction = 'SELL'

        return -1