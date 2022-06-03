import ccxt
import pandas as pd
import ta
from datetime import datetime


COLUMNS = ['MTS', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'VOLUME']


def get_spread(sym_a, sym_b):
    ftx = ccxt.ftx()
    tf = '1d'
    num_candles = 90
    
    # retriving ohlcv dat from exchange
    long_df = pd.DataFrame(ftx.fetch_ohlcv(symbol=sym_a, timeframe=tf, limit=num_candles), 
                           columns=COLUMNS)
    short_df = pd.DataFrame(ftx.fetch_ohlcv(symbol=sym_b, timeframe=tf, limit=num_candles), 
                            columns=COLUMNS)
    
    # creating a new DF with DATA SPREAD
    spread_df = pd.DataFrame()

    spread_open = long_df.OPEN / short_df.OPEN
    spread_df['OPEN'] = spread_open

    spread_high = long_df.HIGH / short_df.HIGH
    spread_df['HIGH'] = spread_high

    spread_low = long_df.LOW / short_df.LOW
    spread_df['LOW'] = spread_low

    spread_close = long_df.CLOSE / short_df.CLOSE
    spread_df['CLOSE'] = spread_close
    
    spread_vol = long_df.VOLUME + short_df.VOLUME
    spread_df['VOLUME'] = spread_vol
    
    #convert and insert a DATE from MTS format to STRING format
    dates = []
    for mts in long_df.index:
        dates.append(datetime.utcfromtimestamp(long_df.iloc[mts].MTS/1000).strftime("%d/%m/%Y"))
    spread_df['DATE'] = dates
    spread_df.set_index('DATE', inplace=True)

    return spread_df


