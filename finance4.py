import numpy as np
import pandas as pd
import pickle

def process_data_for_labels():
    hm_days=7
    df=pd.read_csv('ticker_data/all_ticks.csv')
    tickers=df.colums.values.to_list()


process_data_for_labels()