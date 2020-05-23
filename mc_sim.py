mcimport numpy as np
import pandas as pd
from pandas_datareader import data as dt
import matplotlib.pyplot as plt
from scipy.stats import norm
#%matplotlib inline

intervals = input('How long from now you want to predict (in year): ')
t_intervals = int(intervals) * 250
iterations = int(input("How many possible outcome you want to get: "))

while True:
    ticker = input("Please enter a symbol('q' to quit):")
    if ticker == 'q':
        break

    yr = input("Please enter starting year: ")
    yr = ''.join([yr, '-1-1']) 

    data = pd.DataFrame()
    data[ticker] = dt.DataReader(ticker.upper(), 
                                data_source='yahoo', 
                                start=yr)['Adj Close']

    log_returns = np.log(1 + data.pct_change())
    drift = log_returns.mean() - (0.5 * log_returns.var())
    stdev = log_returns.std()


    daily_returns = np.exp(drift.values + 
                        stdev.values *
                        norm.ppf(
                        np.random.rand(t_intervals, iterations)))

    price_list = np.zeros_like(daily_returns)

    S0 = data.iloc[-1]
    price_list[0] = S0
    for i in range(1, t_intervals):
        price_list[i] = price_list[i - 1] * daily_returns[i]

    print(f"The price right now: {S0[0]:.3f}")
    print(f"The minimum predicted price: {price_list[t_intervals - 1].min():.3f}")
    print(f"The maximum predicted price: {price_list[t_intervals - 1].max():.3f}")
    print(f"The mean price: {price_list[t_intervals - 1].mean():.3f}")
    
    ctr = input("Enter 'g' for the graph, 'q' to quit, anything to continue: ")
    if (ctr == 'g'):
        print(price_list[t_intervals - 1])
        plt.figure(figsize=(20, 10))
        plt.plot(price_list)
        plt.show()
    elif (ctr == 'q'):
        break
    
