import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import matplotlib.dates as mdates
from  mpl_finance import candlestick_ohlc
import pandas as pd
import pandas_datareader.data as dr

style.use("ggplot")

start=dt.datetime(2000,1,1)
end=dt.datetime(2019,10,20)

# df=dr.DataReader('TSLA','yahoo',start,end)


# df.to_csv('tsla.csv')
df=pd.read_csv('tsla.csv',parse_dates=True,index_col=0)

# print(df.head())

df_ohlc_adjclose=df['Adj Close'].resample('10D').ohlc()
df_ohlc_adjclose.reset_index(inplace=True)
df_ohlc_adjclose['Date']=df_ohlc_adjclose['Date'].map(mdates.date2num)

df_vol=df['Adj Close'].resample('10D').sum()


# MatPlotLib Way
ax1 = plt.subplot2grid((6,1),(0,0),rowspan=5,colspan=1)
ax2 = plt.subplot2grid((6,1),(5,0),rowspan=1,colspan=1, sharex=ax1)

# ax1.plot(df.index,df['Adj Close'])
# ax1.plot(df.index,df['100ma'])
# ax2.bar(df.index,df['Volume'])

candlestick_ohlc(ax1,df_ohlc_adjclose.values,width=2,colorup='g')
ax2.fill_between(df_vol.index.map(mdates.date2num),df_vol.values,0,color='b')

plt.show()