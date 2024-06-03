import pandas as pd
import math

def shooting_star(p_day=[]):
    """This checks for shooting star bullish pattern to buy.
    The parameter should be given as a list in the form:
        x_day = [open, high, low, close]"""
    
    oppen = p_day[0]
    high = p_day[1]
    low = p_day[2]
    close = p_day[3]
    body = close - oppen
    tot_stick = high - low
    top_wick = high - close
    bot_wick = oppen - low
    
    if body > 0 and body <= 0.4 * tot_stick:
        if bot_wick >= 1.4 * top_wick:
            return True
        else:
            return False

def golden_cross(hist_data=[]):
    """This checks for Golden Cross moving average pattern.
        The parameter should be given as the list of closing prices of
        the days that have passed in the simulation."""
    
    clean_hist_data = [x for x in hist_data if math.isnan(x) == False]

    if len(clean_hist_data) >= 202:
        #Previous Day
        # p_200 = sma_200(hist_data[-200:])
        p_50 = sma_50(clean_hist_data[-50:])

        #Day Before Previous Day
        clean_hist_data.remove(clean_hist_data[-1])
        pp_hist_data = clean_hist_data
        pp_200 = sma_200(pp_hist_data[-200:])
        pp_50 = sma_50(pp_hist_data[-50:])

        #2 Days Before Previous Day
        pp_hist_data.remove(pp_hist_data[-1])
        ppp_hist_data = pp_hist_data
        ppp_200 = sma_200(ppp_hist_data[-200:])
        # ppp_50 = sma_50(ppp_hist_data[-50:])

        #If the 50 sma crosses from below pd_200 to above it, return True
        if p_50 > pp_200 and pp_50 >= ppp_200:
            return True
        else:
            return False

def death_cross(hist_data=[]):
    """This checks for Death Cross moving average pattern.
        The parameter should be given as the list of closing prices of
        the days that have passed in the simulation."""
    
    clean_hist_data = [x for x in hist_data if math.isnan(x) == False]

    if len(clean_hist_data) >= 202:
        #Previous Day
        p_200 = sma_200(hist_data[-200:])
        # p_50 = sma_50(clean_hist_data[-50:])

        #Day Before Previous Day
        clean_hist_data.remove(clean_hist_data[-1])
        pp_hist_data = clean_hist_data
        pp_200 = sma_200(pp_hist_data[-200:])
        pp_50 = sma_50(pp_hist_data[-50:])

        #2 Days Before Previous Day
        pp_hist_data.remove(pp_hist_data[-1])
        ppp_hist_data = pp_hist_data
        # ppp_200 = sma_200(ppp_hist_data[-200:])
        ppp_50 = sma_50(ppp_hist_data[-50:])

        #If the 50 sma crosses from below pd_200 to above it, return True
        if p_200 > pp_50 and pp_200 >= ppp_50:
            return True
        else:
            return False

    else:
        return False


def sma_200(hist_data=[]):
    """This finds the simple moving average over
    200 day period.
        The parameter should be given as the list of closing prices of
        the days that have passed in the simulation. 
            'hist_data=[-200:]'"""
    
    sma = sum(hist_data) / 200
    return sma

def sma_50(hist_data=[]):
    """This finds the simple moving average over
    50 day period.
        The parameter should be given as the list of closing prices of
        the days that have passed in the simulation.
            'hist_data=[-50:]'"""
    
    sma = sum(hist_data) / 50
    return sma