import ta
import mplfinance as mpf
import matplotlib.pyplot as plt

def get_time_frame(tf, Interval):
    match tf:
        case "1m":
            return Interval.in_1_minute
        case "3m":
            return Interval.in_3_minute
        case "5m":
            return Interval.in_5_minute
        case "15m":
            return Interval.in_15_minute
        case "30m":
            return Interval.in_30_minute
        case "45m":
            return Interval.in_45_minute
        case "1h":
            return Interval.in_1_hour
        case "2h":
            return Interval.in_2_hour
        case "3h":
            return Interval.in_3_hour
        case "4h":
            return Interval.in_4_hour
        case "1d":
            return Interval.in_daily
        case "1w":
            return Interval.in_weekly
        case "1M":
            return Interval.in_monthly

def get_indicator(df, ind):
    match ind:
        case "rsi":
            df["rsi"] = ta.momentum.rsi(df['close'], 14)
            df['rsima'] = df['rsi'].rolling(14).mean()
        case "macd":
            df["macd"] = ta.trend.macd(close=df["close"], window_slow=26, window_fast=12)
            df["macd_diff"] = ta.trend.macd_diff(close=df["close"], window_slow=26, window_fast=12)
            df["macd_signal"] = ta.trend.macd_signal(close=df["close"], window_slow=26, window_fast=12, window_sign=9, fillna=False)
        case "stoch":
            df["stoch_%K"] = ta.momentum.stoch(high=df["high"], low=df["low"], close=df["close"], window= 14,smooth_window=3, fillna=False)
            df["stoch_%D"] = df['stoch_%K'].rolling(3).mean()
        case "boll":
            bol_band = ta.volatility.BollingerBands(close=df["close"], window=20, window_dev=2.25)
            df["lower_band"] = bol_band.bollinger_lband()
            df["higher_band"] = bol_band.bollinger_hband()
            df["ma_band"] = bol_band.bollinger_mavg()
        case "mm":
            df["sma9"] = df['close'].rolling(9).mean()
            df["sma21"] = df['close'].rolling(21).mean()
    return df

def create_plot(df, ind, pic_name):
    match ind:
        case "rsi":
            plot_rsi(df=df, pic_name=pic_name)
        case "macd":
            plot_macd(df=df, pic_name=pic_name)
        case "stoch":
            plot_stoch(df=df, pic_name=pic_name)
        case "boll":
            plot_boll(df=df, pic_name=pic_name)
        case "mm":
            plot_mm(df=df, pic_name=pic_name)

def plot_rsi(df, pic_name):
    df_plot = df.copy().iloc[-150:]
    s = mpf.make_mpf_style(base_mpf_style='charles', rc={'font.size': 6})
    fig1 = mpf.figure(1, figsize=(20, 15), style=s)
    ax1 = fig1.add_subplot(2,1,1)
    ax2 = fig1.add_subplot(2,1,2, sharex=ax1)
    ap0 = [
        mpf.make_addplot(df_plot["rsi"], color='purple', panel=0, title="rsi", ylabel='Points', ax=ax2),
        mpf.make_addplot(df_plot["rsima"], color='yellow', panel=0,ax=ax2)
    ]
    mpf.plot(df_plot, type='candle', ax=ax1, addplot=ap0)
    ax1.yaxis.set_label_position('left')
    ax1.yaxis.tick_left()
    ax2.axhline(30, color='black', linestyle='--')
    ax2.axhline(50, color='black', linestyle='--')
    ax2.axhline(70, color='black', linestyle='--')
    plt.savefig(pic_name)
    
def plot_macd(df, pic_name):
    df_plot = df.copy().iloc[-150:]
    s = mpf.make_mpf_style(base_mpf_style='charles', rc={'font.size': 10})
    fig2 = mpf.figure(2, figsize=(20, 15), style=s)
    ax1 = fig2.add_subplot(2,1,1)
    ax2 = fig2.add_subplot(2,1,2, sharex=ax1)
    ap0 = [
        mpf.make_addplot(df_plot["macd"]/10, color='blue', panel=0, title="MACD", ylabel='Points', ax=ax2),
        mpf.make_addplot(df_plot["macd_signal"]/10, color='orange', panel=0, ax=ax2),
        mpf.make_addplot(df_plot["macd_diff"]/10, panel=0, ax=ax2, type='bar', color='lightblue')
    ]
    mpf.plot(df_plot, type='candle', ax=ax1, addplot=ap0)
    ax1.yaxis.set_label_position('left')
    ax1.yaxis.tick_left()
    ax2.axhline(0, color='black', linestyle='--')
    plt.savefig(pic_name)
  
def plot_stoch(df, pic_name):
    df_plot = df.copy().iloc[-150:]
    s = mpf.make_mpf_style(base_mpf_style='charles', rc={'font.size': 10})
    fig3 = mpf.figure(3, figsize=(20, 15), style=s)
    ax1 = fig3.add_subplot(2,1,1)
    ax2 = fig3.add_subplot(2,1,2, sharex=ax1)
    ap0 = [
        mpf.make_addplot(df_plot["stoch_%K"], color='blue', panel=0, title="Stochastic", ylabel='Points', ax=ax2),
        mpf.make_addplot(df_plot["stoch_%D"], color='orange', panel=0, ax=ax2)
    ]
    mpf.plot(df_plot, type='candle', ax=ax1, addplot=ap0)
    ax1.yaxis.set_label_position('left')
    ax1.yaxis.tick_left()
    ax2.axhline(20, color='black', linestyle='--')
    ax2.axhline(50, color='black', linestyle='--')
    ax2.axhline(80, color='black', linestyle='--')
    plt.savefig(pic_name)

def plot_boll(df, pic_name):
    df_plot = df.copy().iloc[-150:]
    s = mpf.make_mpf_style(base_mpf_style='charles', rc={'font.size': 10})
    fig4 = mpf.figure(4, figsize=(20, 15), style=s)
    ax1 = fig4.add_subplot(2,1,1)
    ap0 = [
        mpf.make_addplot(df_plot["lower_band"], color='blue', panel=0, title="Bollinger Bands", ax=ax1),
        mpf.make_addplot(df_plot["higher_band"], color='blue', panel=0, ax=ax1),
        mpf.make_addplot(df_plot["ma_band"], color='orange', panel=0, ax=ax1)
    ]     
    mpf.plot(df_plot, type='candle', ax=ax1, addplot=ap0)
    ax1.yaxis.set_label_position('left')
    ax1.yaxis.tick_left()
    plt.savefig(pic_name)
    
def plot_mm(df, pic_name):
    df_plot = df.copy().iloc[-150:]
    s = mpf.make_mpf_style(base_mpf_style='charles', rc={'font.size': 10})
    fig5 = mpf.figure(5, figsize=(20, 15), style=s)
    ax1 = fig5.add_subplot(2,1,1)
    ap0 = [
        mpf.make_addplot(df_plot["sma9"], color='blue', panel=0, title="Moyenne Mobile", ylabel='Points', ax=ax1),
        mpf.make_addplot(df_plot["sma21"], color='orange', panel=0, ax=ax1),
    ]     
    mpf.plot(df_plot, type='candle', ax=ax1, addplot=ap0)
    ax1.yaxis.set_label_position('left')
    ax1.yaxis.tick_left()
    plt.savefig(pic_name)