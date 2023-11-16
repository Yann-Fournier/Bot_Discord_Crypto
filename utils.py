import ta

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
        case "macd":
            df["macd"] = ta.trend.macd(close=df["close"], window_slow=26, window_fast=12)
            df["macd_diff"] = ta.trend.macd_diff(close=df["close"], window_slow=26, window_fast=12)
            df["macd_signal"] = ta.trend.macd_signal(close=df["close"], window_slow=26, window_fast=12, window_sign=9, fillna=False)
        case "stoch":
            df["stoch_%K"] = ta.momentum.stoch(high=df["high"], low=df["low"], close=df["close"], window= 14,smooth_window=3, fillna=False)
            df["stoch_%D"] = df['Stoch_%K'].rolling(3).mean()
        case "bol":
            bol_band = ta.volatility.BollingerBands(close=df["close"], window=100, window_dev=2.25)
            df["lower_band"] = bol_band.bollinger_lband()
            df["higher_band"] = bol_band.bollinger_hband()
            df["ma_band"] = bol_band.bollinger_mavg()
    return df

def create_plot(df):
    print("create plot")