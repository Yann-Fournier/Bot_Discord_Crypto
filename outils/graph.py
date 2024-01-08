import ta
import mplfinance as mpf
import matplotlib.pyplot as plt

# Recupération de l'intervale de temps entré par l'utilisateur.
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

# Recupération de l'indicateur entré par l'utilisateur.
# N'hesiter pas à vous renseignez sur les calculs reliés aux differents indicateurs
def get_indicator(df, ind): # On ajoute les colonnes, correspondants à l'indicateur, dans le dataframe pandas
    match ind:
        case "rsi":
            df["rsi"] = ta.momentum.rsi(df['close'], 14) # rsi avec une periode de 14 unitées de temps
            df['rsima'] = df['rsi'].rolling(14).mean() # une moyenne des 14 dernières unitées de temps
        case "macd":
            # macd avec une période lente de 26 unitées de temps et une période rapide de 12 unitées de temps
            df["macd"] = ta.trend.macd(close=df["close"], window_slow=26, window_fast=12)
            # macd différence avec une période lente de 26 unitées de temps et une période rapide de 12 unitées de temps
            df["macd_diff"] = ta.trend.macd_diff(close=df["close"], window_slow=26, window_fast=12)
            # macd signal avec une période lente de 26 unitées de temps et une période rapide de 12 unitées de temps
            df["macd_signal"] = ta.trend.macd_signal(close=df["close"], window_slow=26, window_fast=12, window_sign=9, fillna=False)
        case "stoch":
            # Stochastique avec une periode de 14 unitées de temps 
            df["stoch_%K"] = ta.momentum.stoch(high=df["high"], low=df["low"], close=df["close"], window= 14,smooth_window=3, fillna=False)
            # moyenne des trois dernières unitées de temps du Stochastique
            df["stoch_%D"] = df['stoch_%K'].rolling(3).mean()
        case "boll": 
            # Bandes de Bollinger effectuer sur une période de 20 unitées de temps
            bol_band = ta.volatility.BollingerBands(close=df["close"], window=20, window_dev=2.25)
            df["lower_band"] = bol_band.bollinger_lband()
            df["higher_band"] = bol_band.bollinger_hband()
            df["ma_band"] = bol_band.bollinger_mavg()
        case "mm":
            df["sma9"] = df['close'].rolling(9).mean() # moyenne des 9 dernières unitées de temps du prix de fermeture de session
            df["sma21"] = df['close'].rolling(21).mean() # moyenne des 21 dernières unitées de temps du prix de fermeture de session
    return df

def simple_plot(df, pic_name, val): # création d'un graphique simple (que la valeur)
    df_plot = df.copy().iloc[-150:] # on prend les 150 dernières valeurs du dataset.
    s = mpf.make_mpf_style(base_mpf_style='charles', rc={'font.size': 6}) # on indique le style du graphique
    fig = mpf.figure(2, figsize=(20, 15), style=s) # création de la figure
    ax1 = fig.add_subplot(2,1,1, title=val) # ajout d'un graphique
    mpf.plot(df_plot, type='candle', ax=ax1) # ajout des données dans le graphique
    ax1.yaxis.set_label_position('left')  # positionnement du label des ordonnées à gauche (style)
    ax1.yaxis.tick_left() # positionnement de l'axe des ordonnées à gauche (style)
    plt.savefig(pic_name) # sauvegarde du graphique en tant que photo (png) 

def create_plot(df, ind, pic_name, val): # permet de choisir la bonne fonction par rapport à l'indicateur choisi
    match ind:
        case "rsi":
            plot_rsi(df=df, pic_name=pic_name, val=val)
        case "macd":
            plot_macd(df=df, pic_name=pic_name, val=val)
        case "stoch":
            plot_stoch(df=df, pic_name=pic_name, val=val)
        case "boll":
            plot_boll(df=df, pic_name=pic_name, val=val)
        case "mm":
            plot_mm(df=df, pic_name=pic_name, val=val)

def plot_rsi(df, pic_name, val):
    df_plot = df.copy().iloc[-150:] # on prend les 150 dernières valeurs du dataset.
    s = mpf.make_mpf_style(base_mpf_style='charles', rc={'font.size': 6}) # on indique le style du graphique
    fig1 = mpf.figure(1, figsize=(20, 15), style=s) # création de la figure
    ax1 = fig1.add_subplot(2,1,1,title=val) # ajout d'un graphique
    ax2 = fig1.add_subplot(2,1,2, sharex=ax1, title="RSI") # ajout d'un deuxieme graphique
    ap0 = [ # Les sous graphiques doivent être stockés dans un tableau. c'est le parametre 'ax' qui defini sur quelle graphique ils sont ajouter
        mpf.make_addplot(df_plot["rsi"], color='purple', panel=0, ylabel='Points', ax=ax2), # ajout d'un sous graphique sur le deuxieme graphique
        mpf.make_addplot(df_plot["rsima"], color='blue', panel=0,ax=ax2) # ajout d'un sous graphique sur le deuxieme graphique
    ]
    mpf.plot(df_plot, type='candle', ax=ax1, addplot=ap0) # ajout des données dans le graphique + ajout des sous graphiques
    ax1.yaxis.set_label_position('left') # positionnement du label des ordonnées à gauche (style)
    ax1.yaxis.tick_left() # positionnement de l'axe des ordonnées à gauche (style)
    ax2.axhline(30, color='black', linestyle='--') # ajout d'une ligne pointillé sur le deuxieme graphique sur l'ordonnée 30
    ax2.axhline(50, color='black', linestyle='--') # ajout d'une ligne pointillé sur le deuxieme graphique sur l'ordonnée 50
    ax2.axhline(70, color='black', linestyle='--') # ajout d'une ligne pointillé sur le deuxieme graphique sur l'ordonnée 70
    plt.savefig(pic_name) # sauvegarde du graphique en tant que photo (png) 
    
def plot_macd(df, pic_name, val):
    df_plot = df.copy().iloc[-150:] # on prend les 150 dernières valeurs du dataset.
    s = mpf.make_mpf_style(base_mpf_style='charles', rc={'font.size': 10})# on indique le style du graphique
    fig2 = mpf.figure(2, figsize=(20, 15), style=s) # création de la figure
    ax1 = fig2.add_subplot(2,1,1, title=val) # ajout d'un graphique
    ax2 = fig2.add_subplot(2,1,2, sharex=ax1, title="MACD") # ajout d'un deuxieme graphique
    ap0 = [ # Les sous graphiques doivent être stockés dans un tableau. c'est le parametre 'ax' qui defini sur quelle graphique ils sont ajouter
        mpf.make_addplot(df_plot["macd"]/10, color='blue', panel=0, ylabel='Points', ax=ax2), # ajout d'un sous graphique sur le deuxieme graphique
        mpf.make_addplot(df_plot["macd_signal"]/10, color='orange', panel=0, ax=ax2), # ajout d'un sous graphique sur le deuxieme graphique
        mpf.make_addplot(df_plot["macd_diff"]/10, panel=0, ax=ax2, type='bar', color='lightblue') # ajout d'un sous graphique sur le deuxieme graphique
    ]
    mpf.plot(df_plot, type='candle', ax=ax1, addplot=ap0) # ajout des données dans le graphique + ajout des sous graphiques
    ax1.yaxis.set_label_position('left') # positionnement du label des ordonnées à gauche (style)
    ax1.yaxis.tick_left() # positionnement de l'axe des ordonnées à gauche (style)
    ax2.axhline(0, color='black', linestyle='--') # ajout d'une ligne pointillé sur le deuxieme graphique sur l'ordonnée 0
    plt.savefig(pic_name) # sauvegarde du graphique en tant que photo (png) 
  
def plot_stoch(df, pic_name, val):
    df_plot = df.copy().iloc[-150:] # on prend les 150 dernières valeurs du dataset.
    s = mpf.make_mpf_style(base_mpf_style='charles', rc={'font.size': 10}) # on indique le style du graphique
    fig3 = mpf.figure(3, figsize=(20, 15), style=s) # création de la figure
    ax1 = fig3.add_subplot(2,1,1, title=val) # ajout d'un graphique
    ax2 = fig3.add_subplot(2,1,2, sharex=ax1, title="Stochastic") # ajout d'un deuxieme graphique
    ap0 = [ # Les sous graphiques doivent être stockés dans un tableau. c'est le parametre 'ax' qui defini sur quelle graphique ils sont ajouter
        mpf.make_addplot(df_plot["stoch_%K"], color='blue', panel=0, ylabel='Points', ax=ax2), # ajout d'un sous graphique sur le deuxieme graphique
        mpf.make_addplot(df_plot["stoch_%D"], color='orange', panel=0, ax=ax2) # ajout d'un sous graphique sur le deuxieme graphique
    ]
    mpf.plot(df_plot, type='candle', ax=ax1, addplot=ap0) # ajout des données dans le graphique + ajout des sous graphiques
    ax1.yaxis.set_label_position('left') # positionnement du label des ordonnées à gauche (style)
    ax1.yaxis.tick_left() # positionnement de l'axe des ordonnées à gauche (style)
    ax2.axhline(20, color='black', linestyle='--') # ajout d'une ligne pointillé sur le deuxieme graphique sur l'ordonnée 20
    ax2.axhline(50, color='black', linestyle='--') # ajout d'une ligne pointillé sur le deuxieme graphique sur l'ordonnée 30
    ax2.axhline(80, color='black', linestyle='--') # ajout d'une ligne pointillé sur le deuxieme graphique sur l'ordonnée 80
    plt.savefig(pic_name) # sauvegarde du graphique en tant que photo (png) 

def plot_boll(df, pic_name, val):
    df_plot = df.copy().iloc[-150:] # on prend les 150 dernières valeurs du dataset.
    s = mpf.make_mpf_style(base_mpf_style='charles', rc={'font.size': 10}) # on indique le style du graphique
    fig4 = mpf.figure(4, figsize=(20, 15), style=s) # création de la figure
    ax1 = fig4.add_subplot(2,1,1, title=val + " / Bollinger Bands") # ajout d'un graphique
    ap0 = [ # Les sous graphiques doivent être stockés dans un tableau. c'est le parametre 'ax' qui defini sur quelle graphique ils sont ajouter
        mpf.make_addplot(df_plot["lower_band"], color='blue', panel=0, ax=ax1), # ajout d'un sous graphique sur le graphique
        mpf.make_addplot(df_plot["higher_band"], color='blue', panel=0, ax=ax1), # ajout d'un sous graphique sur le graphique
        mpf.make_addplot(df_plot["ma_band"], color='orange', panel=0, ax=ax1) # ajout d'un sous graphique sur le graphique
    ]
    mpf.plot(df_plot, type='candle', ax=ax1, addplot=ap0) # ajout des données dans le graphique + ajout des sous graphiques
    ax1.yaxis.set_label_position('left') # positionnement du label des ordonnées à gauche (style)
    ax1.yaxis.tick_left() # positionnement de l'axe des ordonnées à gauche (style)
    plt.savefig(pic_name) # sauvegarde du graphique en tant que photo (png) 

def plot_mm(df, pic_name, val):
    df_plot = df.copy().iloc[-150:] # on prend les 150 dernières valeurs du dataset.
    s = mpf.make_mpf_style(base_mpf_style='charles', rc={'font.size': 10}) # on indique le style du graphique
    fig5 = mpf.figure(5, figsize=(20, 15), style=s) # création de la figure
    ax1 = fig5.add_subplot(2,1,1, title=val + " / Moyenne Mobile") # ajout d'un graphique
    ap0 = [ # Les sous graphiques doivent être stockés dans un tableau. c'est le parametre 'ax' qui defini sur quelle graphique ils sont ajouter
        mpf.make_addplot(df_plot["sma9"], color='blue', panel=0, ylabel='Points', ax=ax1), # ajout d'un sous graphique sur le graphique
        mpf.make_addplot(df_plot["sma21"], color='orange', panel=0, ax=ax1), # ajout d'un sous graphique sur le graphique
    ]     
    mpf.plot(df_plot, type='candle', ax=ax1, addplot=ap0) # ajout des données dans le graphique + ajout des sous graphiques
    ax1.yaxis.set_label_position('left') # positionnement du label des ordonnées à gauche (style)
    ax1.yaxis.tick_left() # positionnement de l'axe des ordonnées à gauche (style)
    plt.savefig(pic_name) # sauvegarde du graphique en tant que photo (png) 