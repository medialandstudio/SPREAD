#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  7 12:02:50 2021

@author: ministudio
"""

from datetime import datetime, timezone, timedelta
import pandas as pd
import numpy as np
import statistics


def get_top_volume(start_trade, end_trade, ftx_client, num_coins):
    perp = get_all_futures(ftx_client)
    start_timestamp = start_trade.replace(tzinfo=timezone.utc).timestamp()
    end_timestamp = end_trade.replace(tzinfo=timezone.utc).timestamp()
    
    volumes = pd.DataFrame(columns=['VOLUME'])
    
    print(f'\nSTARTING -VOLUMES- process from {start_trade}: ')
    with alive_bar(len(perp), length=20) as bar:
        for ticker in perp.index:
            candles = ftx_client.fetchOHLCV(ticker, timeframe='1h', limit=5000, params={'start_time': start_timestamp,
                                                                                        'end_time': end_timestamp})
            candles_df = pd.DataFrame(candles, columns=['MTS', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'VOLUME'])
            volumes.loc[ticker] = candles_df.VOLUME.sum()
            bar()
    
    volumes.sort_values(by=['VOLUME'], inplace=True, ascending=False)
    
    return volumes.iloc[:num_coins][:num_coins]


def get_all_futures(ftx_client):
    """
    

    Parameters
    ----------
    ftx_client : an authenticated FTX client

    Returns
    -------
    futures_df : DATAFRAME
        a dataframe with ALL the FUTURES on FTX, PRECISION and minimal size trading.

    """

    tickers = ftx_client.fetchMarkets()
    futures_df = pd.DataFrame(columns=['PRECISION', 'MIN', 'VOLUME'])
    
    for ticker in tickers:
        if 'PERP' in ticker['id']: 
            futures_df.loc[ticker['id']] = [ticker['precision']['amount'], 
                                            ticker['precision']['price'], 
                                            int(float(ticker['info']['volumeUsd24h']))]

    return futures_df



