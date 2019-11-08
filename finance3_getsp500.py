import bs4 as bs
import requests
import pickle
import os
from datetime import datetime
import pandas as pd
import pandas_datareader.data as dr
import tqdm
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np

style.use('ggplot')


def get_sp500(fresh=False):
    filename = 'tickers.pickle'
    if os.path.isfile(filename) and not fresh:
        with open(filename, 'rb') as f:
            return pickle.load(f)
    resp = requests.get("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
    soup = bs.BeautifulSoup(resp.text, features="lxml")
    table = soup.find('table', {'id': 'constituents'})

    tickers = []

    for tr in table.find_all('tr')[1:]:
        ticker = tr.find_all('td')[0].text.strip()
        tickers.append(ticker)

    with open(filename, "wb") as f:
        pickle.dump(tickers, f)

    return tickers


def get_ticker_data(dirname, tick, start, end, fresh=False, verbose=False):
    filename = '{}/{}.csv'.format(dirname, tick)
    tick_data = None
    if os.path.isfile(filename) and not fresh:
        if verbose:
            print(f'{tick} already exists')
        tick_data = pd.read_csv(filename, parse_dates=True, index_col=0)
    else:
        if verbose:
            print(f'{tick} downloading')
        try:
            tick_data = dr.DataReader(tick, 'yahoo', start, end)
            tick_data.to_csv(filename)
        except Exception as e:
            print(f'error getting {tick} {e}')
    return tick_data


def get_all_ticker_data(tickers, start, end, fresh=False):
    main_df = None
    dirname = 'ticker_data'
    if not os.path.exists(dirname):
        os.mkdir(dirname)

    for tick in tqdm.tqdm(tickers, unit='ticks'):
        data = get_ticker_data(dirname, tick, start, end, fresh)
        # data.set_index('Date', inplace=True)
        if data is not None:
            data.rename(columns={'Adj Close': tick}, inplace=True)
            data.drop(['Open', 'High', 'Low', 'Close', 'Volume'], 1, inplace=True)
            if main_df is None:
                main_df = data
            else:
                main_df = main_df.join(data, how='outer')

    main_df.to_csv(f'{dirname}/all_ticks.csv')
    return main_df


def load_all_ticker_data():
    dirname = 'ticker_data'
    df = pd.read_csv(f'{dirname}/all_ticks.csv', parse_dates=True, index_col=0)
    return df


def visualize(df):
    df_corr = df.corr()
    data = df_corr.values
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    heatmap = ax.pcolor(data, cmap=plt.cm.RdYlGn)
    fig.colorbar(heatmap)
    ax.set_xticks(np.arange(data.shape[1]) + 0.5, minor=False)
    ax.set_yticks(np.arange(data.shape[0]) + 0.5, minor=False)
    ax.invert_yaxis()
    ax.xaxis.tick_top()
    column_labels = df_corr.columns
    row_labels = df_corr.index
    ax.set_xticklabels(column_labels)
    ax.set_yticklabels(row_labels)
    plt.xticks(rotation=90)
    heatmap.set_clim(-1, 1)
    plt.tight_layout()
    plt.show()


sp500_ticks = get_sp500()
start = datetime(2000, 1, 1)
end = datetime(2019, 10, 20)

# all_data = get_all_ticker_data(sp500_ticks, start, end)
all_data = load_all_ticker_data()
print(all_data.head())
print(all_data.tail())
visualize(all_data)
