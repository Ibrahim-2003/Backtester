from datetime import datetime
from matplotlib.pyplot import title
import pandas as pd
import yfinance as yf
# import plotly.graph_objects as go
# from plotly.subplots import make_subplots
# import mplfinance as mpf

interval = '1d'
ticker_list = ['AAPL', 'MSFT', 'QCOM', 'AMD', 'INTC', 'PEP','JNJ','KO',
                'TTWO','TXN', 'SNE','ABNB', 'T', 'CSCO', 'TMUS','MCD']#'NVDA', 'SNOW', 'PLTR'

# df = yf.download(ticker_list, start=std_date, end=nw_date, interval=interval, group_by='ticker')
# data = pd.DataFrame(df)
# data.reset_index(inplace=True)
# data.to_csv('historical_stock_data.csv')


def retrieve_prices(start_date, now_date):
    '''Retrieves prices as a pandas dataframe using Yahoo Finance:
        start_date => Starting date as a string in format YYYY-MM-dd
            example: '2006-12-26'
        now_date => End date, or default is the current date
            example: '2007-12-26'
        interval => MUST CHANGE THIS THROUGH THE PRICES MODULE
    '''
    interval = '1d'
    df = yf.download(ticker_list, start=start_date, end=now_date, interval=interval, group_by='ticker')
    data = pd.DataFrame(df)
    data.reset_index(inplace=True)
    data.to_csv('historical_stock_data.csv')
    return data

'''The commented code below gives the candlestick charts of the tickers in ticker_list using PLOTLY'''
# candle = pd.DataFrame(df)
# revert = candle
# i=0
# fignames = []
# for ticker in ticker_list:
#     candle = candle[ticker]
#     fig = go.Figure(data=[go.Candlestick(x=candle.index,
#                 open=candle['Open'],
#                 high=candle['High'],
#                 low=candle['Low'],
#                 close=candle['Close'])])
#     fig.update_layout(title=ticker)
#     fig.show()
#     candle=revert
'''The commented code below gives the candlestick charts of the tickers in ticker_list using MPF'''
# candle = pd.DataFrame(df)
# revert = candle
# for ticker in ticker_list:
#     candle = candle[ticker]
#     mpf.plot(candle, title=ticker, type='candle', style='yahoo', savefig=f'{ticker}_candlestick.png')
#     candle=revert

