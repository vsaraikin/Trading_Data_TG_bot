from tvDatafeed import TvDatafeed, Interval
import matplotlib.pyplot as plt

tv = TvDatafeed()

def get_data_TV(ticker, interval, exchange):
    tv = TvDatafeed()
    data = tv.get_hist(ticker, exchange=exchange, interval=interval, n_bars=5000)['close']
    return data

def last_price(ticker, exchange):
    data = get_data_TV(ticker, exchange=exchange, interval=Interval.in_1_minute)
    fecha = data.index[-1]
    value = data[-1]
    return fecha, value

def plot_data_1_minute(ticker, exchange):
    data = get_data_TV(ticker, interval=Interval.in_1_minute, exchange=exchange)
    data.plot(figsize=(14, 8))
    plt.title(f'{ticker} - 1 min timeframe')
    fig = plt.savefig('proxy_image.png')
    print(f'Plot {ticker} saved')
    return fig

def plot_data_15_minute(ticker, exchange):
    data = get_data_TV(ticker, interval=Interval.in_15_minute, exchange=exchange)
    data.plot(figsize=(14, 8))
    plt.title(f'{ticker} - 15 min timeframe')
    fig = plt.savefig('proxy_image.png')
    print(f'Plot {ticker} saved')
    return fig

def plot_data_1_hour(ticker, exchange):
    data = get_data_TV(ticker, interval=Interval.in_1_hour, exchange=exchange)
    data.plot(figsize=(14, 8))
    plt.title(f'{ticker} - 1 hour timeframe')
    fig = plt.savefig('proxy_image.png')
    print(f'Plot {ticker} saved')
    return fig

def plot_data_1_day(ticker, exchange):
    data = get_data_TV(ticker, interval=Interval.in_daily, exchange=exchange)
    data.plot(figsize=(14, 8))
    plt.title(f'{ticker} - 1 day timeframe')
    fig = plt.savefig('proxy_image.png')
    print(f'Plot {ticker} saved')
    return fig