import pandas as pd
from nsepy import get_history
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--last_days_count', action="store", help="Last Number of Days to get data", type=int)
parser.add_argument('--symbol', action="store", help="Stock Symbol", type=str)


args = parser.parse_args()

number_of_days = args.last_days_count
end_date = datetime.now().date()
start_date = end_date - timedelta(number_of_days)

df = get_history(symbol=args.symbol, start=start_date, end=end_date)

# SMA For Delivery
df['delivery_SMA_3'] = df.iloc[:,12].rolling(window=3).mean()
df['delivery_SMA_5'] = df.iloc[:,12].rolling(window=5).mean()
df['delivery_SMA_10'] = df.iloc[:,12].rolling(window=10).mean()

# SMA for Turnover
df['delivery_turnover_3'] = df.iloc[:,10].rolling(window=3).mean()
df['delivery_turnover_5'] = df.iloc[:,10].rolling(window=5).mean()
df['delivery_turnover_10'] = df.iloc[:,10].rolling(window=10).mean()

# SMA for Turnover
df['close_3'] = df.iloc[:,7].rolling(window=3).mean()
df['close_5'] = df.iloc[:,7].rolling(window=5).mean()
df['close_10'] = df.iloc[:,7].rolling(window=10).mean()


# Plot Graph
fig, axs = plt.subplots(3)
#plt.figure(figsize=[15,10])
df.dropna(inplace=True)
plt.grid(True)
#df.index = df.Date
#plt.xticks(df['Date'])
axs[0].plot(df['delivery_SMA_3'],label='SMA 3 days delivery')
axs[0].plot(df['delivery_SMA_5'],label='SMA 5 days delivery')
axs[0].plot(df['delivery_SMA_10'],label='SMA 10 days delivery')
axs[0].legend(loc=2)

# Plot Turnover data
axs[1].plot(df['delivery_turnover_3'],label='SMA 3 days turnover')
axs[1].plot(df['delivery_turnover_5'],label='SMA 5 days turnover')
axs[1].plot(df['delivery_turnover_10'],label='SMA 10 days turnover')
axs[1].legend(loc=2)

# Plot Turnover data
axs[2].plot(df['close_3'],label='SMA 3 days close')
axs[2].plot(df['close_5'],label='SMA 5 days close')
axs[2].plot(df['close_10'],label='SMA 10 days close')
axs[2].legend(loc=2)

plt.show()
